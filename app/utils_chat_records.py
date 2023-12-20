# basic libs
from datetime import datetime
from io import StringIO 
import os
from pathlib import Path
from uuid import uuid4

# special libs
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import sqlite3

# streamlit libs
import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import (
    AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, DataReturnMode
)

#############################
# Config params (1st)
#############################
CFG = {
    "DEBUG_FLAG" : False, # True, # 
    
    "SUPPORTED_CHAT_BOTS" : ["Claude - v2"],
    "NOISE_WORDS" : ['Copy code','Copy'],
    "MAX_NUM_ROWS" : 100000,  # limit number of rows

    "DB_FILENAME" : Path(__file__).parent / "chats.sqlite",
    # assign table names
    "TABLE_CHATS" : "t_chats",
    "TABLE_MODEL" : "t_llm_model",

}

# use dict update so Table name can be reused
CFG.update({
    # define table columns in a list (same SQL syntax)
    "TABLES" : 
        {
            CFG["TABLE_CHATS"] : [
                'id text NOT NULL',
                'session_title text NOT NULL',
                'bot_name text NOT NULL',
                'seq_num text',
                'question text',
                'answer text',
                'topic text',
                'tags text',
                'ts text',
                'uid text'
            ],
            CFG["TABLE_MODEL"] : [
                'id text NOT NULL',
                'name text NOT NULL',
                'url text',
                'description text',
                'tags text',
                'ts text',
                'uid text'
            ],
        },
})


#############################
#  DB related  (2nd)
#############################
class DBConn(object):
    def __init__(self, db_file=CFG["DB_FILENAME"]):
        self.conn = sqlite3.connect(db_file)

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()


def db_run_sql(sql_stmt, conn=None):
    """handles both select and insert/update/delete
    """
    if not sql_stmt or conn is None:
        return None
    
    if sql_stmt.lower().strip().startswith("select"):
        return pd.read_sql(sql_stmt, conn)
    
    cur = conn.cursor()
    cur.executescript(sql_stmt)
    conn.commit()
    # conn.close()
    return None


def db_execute(sql_statement, debug=CFG["DEBUG_FLAG"]):
    """handles insert/update/delete
    """
    with DBConn() as _conn:
        debug_print(sql_statement, debug=debug)
        _conn.execute(sql_statement)
        _conn.commit()      

def db_get_row_count(table_name):
    with DBConn() as _conn:
        sql_stmt = f"""
            select count(*)
            from {table_name};
        """
        df = pd.read_sql(sql_stmt, _conn)
        return df.iat[0,0]

def db_select_by_id(table_name, id_value=""):
    """Select row by primary key: id
    """
    if not id_value: return []

    with DBConn() as _conn:
        sql_stmt = f"""
            select *
            from {table_name} 
            where id = '{id_value}' ;
        """
        return pd.read_sql(sql_stmt, _conn).fillna("").to_dict('records')

def db_upsert(data, user_key_cols=["id"]):
    if not data: 
        return None
    
    table_name = data.get("table_name", "")
    if not table_name:
        raise Exception(f"[ERROR] Missing table_name: {data}")
    
    # skip if key columns are missing
    required_val = ""
    if table_name == CFG["TABLE_CHATS"]:
        required_val = data.get("answer", "")
    elif table_name == CFG["TABLE_MODEL"]:
        required_val = data.get("name", "")
    if not required_val: return

    if not "uid" in data or not data.get("uid", ""):
        data.update({"uid":get_uid()})

    # build SQL
    visible_columns = get_columns(table_name, prop_name="is_visible")

    # query by user-key to avoid duplicates
    uk_where_clause = []
    for col,val in data.items():
        if col in user_key_cols:
            if val != "":
                uk_where_clause.append(f" {col} = '{escape_single_quote(val)}' ")

    if not uk_where_clause:
        return None # skip if user key cols not populated

    with DBConn() as _conn:
        where_clause = " and ".join(uk_where_clause)
        sql_stmt = f"""
            select id
            from {table_name} 
            where {where_clause};
        """
        rows = pd.read_sql(sql_stmt, _conn).to_dict('records')

    if not len(rows):
        sql_type = "INSERT" 
    else: 
        sql_type = "UPDATE"  
        old_row = rows[0]

    
    if sql_type == "INSERT":


        col_clause = []
        val_clause = []
        for col,val in data.items():
            if col not in visible_columns:
                continue
            col_clause.append(col)
            col_val = escape_single_quote(val)
            val_clause.append(f"'{col_val}'")

        upsert_sql = f"""
            insert into {table_name} (
                {", ".join(col_clause)}
            )
            values (
                {", ".join(val_clause)}
            );
        """

    else:
        set_clause = []
        for col,val in data.items():
            if col not in visible_columns or col in user_key_cols:
                continue

            # skip if no change
            old_val = old_row.get(col, "")
            if old_val is None:
                old_val = ""
            if val == old_val:
                continue

            col_val = escape_single_quote(val)

            set_clause.append(f" {col} = '{col_val}'")

        if set_clause:
            id_ = old_row.get("id")
            upsert_sql = f"""
                update {table_name} 
                set 
                    {", ".join(set_clause)}
                where id = '{id_}';
            """

    db_execute(upsert_sql)

def db_delete_by_id(data):
    if not data: 
        return None
    
    table_name = data.get("table_name", "")
    if not table_name:
        raise Exception(f"[ERROR] Missing table_name: {data}")

    id_val = data.get("id", "")
    if not id_val:
        return None
    
    delete_sql = f"""
        delete from {table_name}
        where id = '{id_val}';
    """
    db_execute(delete_sql)

def db_update_by_id(data, update_changed=True):
    if not data: 
        return
    
    table_name = data.get("table_name", "")
    if not table_name:
        raise Exception(f"[ERROR] Missing table_name: {data}")

    id_val = data.get("id", "")
    if not id_val:
        return

    if not "uid" in data or not data.get("uid", ""):
        data.update({"uid":get_uid()})

    if update_changed:
        rows = db_select_by_id(table_name=table_name, id_value=id_val)
        if len(rows) < 1:
            return
        old_row = rows[0]

    editable_columns = get_columns(table_name, prop_name="is_editable")

    # build SQL
    set_clause = []
    for col,val in data.items():
        if col not in editable_columns: 
            continue

        if update_changed:
            # skip if no change
            old_val = old_row.get(col, "")
            if val != old_val:
                set_clause.append(f"{col} = '{escape_single_quote(val)}'")
        else:
            set_clause.append(f"{col} = '{escape_single_quote(val)}'")

    if set_clause:
        update_sql = f"""
            update {table_name}
            set {', '.join(set_clause)}
            where id = '{id_val}';
        """
        db_execute(update_sql)  

def db_create_table(table_name, conn):
    cols = CFG["TABLES"][table_name]
    t_cols = ",\n\t".join(cols) 
    create_table_sql = f"""
    create table if not exists {table_name} 
    (
            {t_cols}
    );
    """
    # print(create_table_sql)
    try:
        sql_stmt = f"""
            select count(*) from {table_name};
        """
        pd.read_sql(sql_stmt, conn)
    except Exception as ex:
        db_run_sql(create_table_sql, conn)


def db_get_llm_models():
    table_name = CFG["TABLE_MODEL"]
    with DBConn() as _conn:
        sql_stmt = f"""
            select name from {table_name}
            order by name
        """
        df = pd.read_sql(sql_stmt, _conn)
        return [""] + df["name"].to_list()  # prepend blank
    
#############################
#  Misc
#############################
def debug_print(msg, debug=CFG["DEBUG_FLAG"]):
    if debug and msg:
        # st.write(f"[DEBUG] {str(msg)}")
        print(f"[DEBUG] {str(msg)}")

def convert_df2csv(df, index=True):
    return df.to_csv(index=index).encode('utf-8')

def convert_htm2txt(html_txt):
    return html.fromstring(html_txt).text_content().strip()

def is_noise_word(html_txt):
    return convert_htm2txt(html_txt) in CFG["NOISE_WORDS"]

def parse_bot_ver(bot_ver, sep="__"):
    return [x.strip() for x in bot_ver.split(sep) if x.strip()]

def parse_html_txt_claude(html_txt):
    """
    Extract question/answer from HTML text

    Returns:
        list of dialog content
    """
    cells = []
    if not html_txt: return cells

    soup = BeautifulSoup(html_txt, "html.parser")
    results = soup.findAll("div", class_="contents")
    for i in range(len(results)):
        v = results[i].prettify()
        if is_noise_word(v): continue
        # important to preserve HTML string because python code snippets are formatted
        cells.append(v)
    return cells

def escape_single_quote(s):
    if s is None or s == 'None':
        return ''
    if not "'" in s:
        return s
    return s.replace("\'", "\'\'")

def list2sql_str(l):
    """convert a list into SQL in string
    """
    return str(l).replace("[", "(").replace("]", ")")

def get_uid():
    return os.getlogin()

def get_ts_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_uuid():
    return str(uuid4())

#############################
#  UI related
#############################
# Aggrid options
# how to set column width
# https://stackoverflow.com/questions/72624323/how-to-set-a-max-column-length-for-streamlit-aggrid
AGGRID_OPTIONS = {
    "paginationPageSize": 10,
    "grid_height": 360,
    "return_mode_value": DataReturnMode.__members__["FILTERED"],
    "update_mode_value": GridUpdateMode.__members__["MODEL_CHANGED"],
    "fit_columns_on_grid_load": True,
    "min_column_width": 4,
    "selection_mode": "single",  #  "multiple",  # 
    "allow_unsafe_jscode": True,
    "groupSelectsChildren": True,
    "groupSelectsFiltered": True,
    "enable_pagination": True,
}

# list of system columns in all tables
SYS_COLS = ["id","ts","uid"]

# column UI-properties
PROPS = [
    'is_system_col',
    'is_user_key',
    'is_required',
    'is_visible',
    'is_editable',
    'is_clickable',
    'form_column',
    'widget_type',
    'label_text',
    'kwargs'
]

# define options for selectbox column type, keyed on column name
# placed after db_get_llm_models() is defined
SELECTBOX_OPTIONS = {
    "bot_name": db_get_llm_models(),
}

# config UI layout for form-view
COLUMN_PROPS = {

    CFG["TABLE_CHATS"]: {

        "session_title": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-1",
            "widget_type": "text_input",
            "label_text": "Titile"
        },
        "seq_num": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-2",
            "widget_type": "text_input",
            "label_text": "SeqNum"
        },
        "topic": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-3",
            "widget_type": "text_input",
            "label_text": "Topic"
        },
        "question": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-4",
            "widget_type": "text_area",
            "label_text": "Question"
        },
        "answer": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-5",
            "widget_type": "text_area",
            "label_text": "Answer"
        },
        "id": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": False,
            "is_clickable": False,
            "form_column": "COL_2-1",
            "widget_type": "text_input",
            "label_text": "Id"
        },
        "bot_name": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-2",
            "widget_type": "selectbox",
            "label_text": "Bot Name"
        },
        "tags": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-3",
            "widget_type": "text_area",
            "label_text": "Tags"
        },
        "ts": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-4",
            "widget_type": "text_input",
            "label_text": "Timestamp"
        },
        "uid": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-5",
            "widget_type": "text_input",
            "label_text": "UID"
        },

    },

    CFG["TABLE_MODEL"]: {
        "name": {
            "is_system_col": False,
            "is_user_key": True,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-1",
            "widget_type": "text_input",
            "label_text": "Name"
        },
        "url": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": True,
            "form_column": "COL_1-2",
            "widget_type": "text_input",
            "label_text": "URL"
        },
        "description": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-3",
            "widget_type": "text_area",
            "label_text": "Description"
        },

        "id": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": False,
            "is_clickable": False,
            "form_column": "COL_2-1",
            "widget_type": "text_input",
            "label_text": "Id"
        },

        "tags": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-2",
            "widget_type": "text_area",
            "label_text": "Tags"
        },
        "ts": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-3",
            "widget_type": "text_input",
            "label_text": "Timestamp"
        },
        "uid": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-4",
            "widget_type": "text_input",
            "label_text": "UID"
        },


    },
}

def gen_label(col):
    "Convert table column into form label"
    if col == 'ts_created': return "Created At"
    if "_" not in col:
        if col.upper() in ["URL","ID"]:
            return col.upper()
        elif col.upper() == "TS":
            return "Timestamp"
        return col.capitalize()

    cols = []
    for c in col.split("_"):
        c  = c.strip()
        if not c: continue
        cols.append(c.capitalize())
    return " ".join(cols)

def get_columns(table_name, prop_name="is_visible"):
    cols_bool = []
    cols_text = {}
    for k,v in COLUMN_PROPS[table_name].items():
        if prop_name.startswith("is_") and v.get(prop_name, False):
            cols_bool.append(k)
            
        if not prop_name.startswith("is_"):
            val = v.get(prop_name, "")
            if val:
                cols_text.update({k: val})
    
    return cols_bool or cols_text


def parse_column_props():
    """parse COLUMN_PROPS map
    """
    col_defs = {}
    for table_name in COLUMN_PROPS.keys():
        defs = {}
        cols_widget_type = {}
        cols_label_text = {}
        for p in PROPS:
            res = get_columns(table_name, prop_name=p)
            # print(f"{p}: {res}")
            if p == 'widget_type':
                cols_widget_type = res
            elif p == 'label_text':
                cols_label_text = res
            defs[p] = res
            
        # reset label
        for col in cols_widget_type.keys():
            label = cols_label_text.get(col, "")
            if not label:
                label = gen_label(col)
            cols_label_text.update({col : label})
        # print(cols_label_text)
        defs['label_text'] = cols_label_text
        defs['all_columns'] = list(cols_widget_type.keys())

        # sort form_column alpha-numerically
        # max number of form columns = 3
        # add them
        tmp = {}
        for i in range(1,4):
            m = {k:v for k,v in defs['form_column'].items() if v.startswith(f"col{i}-")}
            tmp[f"col{str(i)}_columns"] = sorted(m, key=m.__getitem__)        
        defs.update(tmp)
        col_defs[table_name] = defs
        
    return col_defs

def ui_layout_form_fields(data,form_name,old_row,col,
                        widget_types,col_labels,system_columns):
    DISABLED = col in system_columns
    if old_row:
        old_val = old_row.get(col, "")
        widget_type = widget_types.get(col, "text_input")
        if widget_type == "text_area":
            kwargs = {"height":125}
            val = st.text_area(col_labels.get(col), value=old_val, disabled=DISABLED, key=f"col_{form_name}_{col}", kwargs=kwargs)
        elif widget_type == "date_input":
            old_date_input = old_val.split("T")[0]
            if old_date_input:
                val_date = datetime.strptime(old_date_input, "%Y-%m-%d")
            else:
                val_date = datetime.now().date()
            val = st.date_input(col_labels.get(col), value=val_date, disabled=DISABLED, key=f"col_{form_name}_{col}")
            val = datetime.strftime(val, "%Y-%m-%d")
        elif widget_type == "time_input":
            old_time_input = old_val
            if old_time_input:
                val_time = datetime.strptime(old_time_input.split(".")[0], "%H:%M:%S").time()
            else:
                val_time = datetime.now().time()
            val = st.time_input(col_labels.get(col), value=val_time, disabled=DISABLED, key=f"col_{form_name}_{col}")
        elif widget_type == "selectbox":
            # check if options is avail, otherwise display as text_input
            if col in SELECTBOX_OPTIONS:
                try:
                    if col == "ref_val":
                        _options = SELECTBOX_OPTIONS[col]()
                    else:
                        _options = SELECTBOX_OPTIONS.get(col,[])

                    old_val = old_row.get(col, "")
                    _idx = _options.index(old_val)
                    val = st.selectbox(col_labels.get(col), _options, index=_idx, key=f"col_{form_name}_{col}")
                except ValueError:
                    val = old_row.get(col, "")
            else:
                val = st.text_input(col_labels.get(col), value=old_val, disabled=DISABLED, key=f"col_{form_name}_{col}")

        else:
            val = st.text_input(col_labels.get(col), value=old_val, disabled=DISABLED, key=f"col_{form_name}_{col}")

        if val != old_val:
            data.update({col : val})

    return data


def ui_layout_form(selected_row, table_name):

    form_name = table_name
    COLUMN_DEFS = parse_column_props()
    COL_DEFS = COLUMN_DEFS[table_name]
    visible_columns = COL_DEFS["is_visible"]
    system_columns = COL_DEFS["is_system_col"]
    form_columns = COL_DEFS["form_column"]
    col_labels = COL_DEFS["label_text"]
    widget_types = COL_DEFS["widget_type"]

    old_row = {}
    for col in visible_columns:
        old_row[col] = selected_row.get(col, "") if selected_row is not None else ""

    data = {"table_name": table_name}

    # copy id if present
    id_val = old_row.get("id", "")
    if id_val:
        data.update({"id" : id_val})

    # display form and populate data dict
    col1_columns = []
    col2_columns = []
    for c in visible_columns:
        if form_columns.get(c, "").startswith("COL_1-"):
            col1_columns.append(c)
        elif form_columns.get(c, "").startswith("COL_2-"):
            col2_columns.append(c)

    with st.form(form_name, clear_on_submit=True):
        col1,col2 = st.columns([6,3])
        with col1:
            for col in col1_columns:
                data = ui_layout_form_fields(data,form_name,old_row,col,
                            widget_types,col_labels,system_columns)
        with col2:
            for col in col2_columns:
                data = ui_layout_form_fields(data,form_name,old_row,col,
                            widget_types,col_labels,system_columns)

            # add checkbox for deleting this record
            col = "delelte_record"
            delete_flag = st.checkbox("Delelte Record?", value=False)
            data.update({col: delete_flag})

        save_btn = st.form_submit_button("💾 Save")
        if save_btn:
            try:
                delete_flag = data.get("delelte_record", False)
                if delete_flag:
                    if data.get("id"):
                        db_delete_by_id(data)
                else:
                    if data.get("id"):
                        data.update({"ts": get_ts_now(),
                                    "uid": get_uid(), })
                        db_update_by_id(data)
                    else:
                        data.update({"id": get_uuid(), 
                                    "ts": get_ts_now(),
                                    "uid": get_uid(), })
                        db_upsert(data)

            except Exception as ex:
                st.error(f"{str(ex)}")



def ui_display_df_grid(df, 
        selection_mode="single",  # "multiple", 
        fit_columns_on_grid_load=AGGRID_OPTIONS["fit_columns_on_grid_load"],
        min_column_width=AGGRID_OPTIONS["min_column_width"],
        page_size=AGGRID_OPTIONS["paginationPageSize"],
        grid_height=AGGRID_OPTIONS["grid_height"],
        clickable_columns=[],
        editable_columns=[],
        colored_columns={}
    ):
    """show input df in a grid and return selected row
    """

    gb = GridOptionsBuilder.from_dataframe(df, min_column_width=min_column_width)
    gb.configure_selection(selection_mode,
            use_checkbox=True,
            groupSelectsChildren=AGGRID_OPTIONS["groupSelectsChildren"], 
            groupSelectsFiltered=AGGRID_OPTIONS["groupSelectsFiltered"]
        )
    gb.configure_pagination(paginationAutoPageSize=False, 
        paginationPageSize=page_size)
    
    gb.configure_columns(editable_columns, editable=True)

    # color column
    for k,v in colored_columns.items():
        gb.configure_column(k, cellStyle=v)

    if clickable_columns:       # config clickable columns
        cell_renderer_url =  JsCode("""
            function(params) {return `<a href=${params.value} target="_blank">${params.value}</a>`}
        """)
        for col_name in clickable_columns:
            gb.configure_column(col_name, cellRenderer=cell_renderer_url)


    gb.configure_grid_options(domLayout='normal')
    grid_response = AgGrid(
        df, 
        gridOptions=gb.build(),
        data_return_mode=AGGRID_OPTIONS["return_mode_value"],
        update_mode=AGGRID_OPTIONS["update_mode_value"],
        height=grid_height, 
        # width='100%',
        fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    )
 
    return grid_response

