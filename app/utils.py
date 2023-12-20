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
    
    "DB_FILENAME" : Path(__file__).parent / "zinets.sqlite",

    # assign table names
    "TABLE_ZI" : "t_zi",            # all Zi 字
    "TABLE_PART" : "t_zi_part",     # decomposed Zi 字子
    "TABLE_SHUFA" : "t_zi_shufa",   # ShuFa 书法
    "TABLE_WORD" : "t_zi_word",     # phrase/word 词语
    "TABLE_TEXT" : "t_zi_text",     # text 文章 
    "TABLE_MEDIA" : "t_zi_media",   # audio/video 录音，视频

    "SHUFA_TYPE": ["甲骨", "金", "篆", "隶", "楷", "行", "草"]
}

# use dict update so Table name can be reused
CFG.update({
    # define table columns in a list (same SQL syntax)
    "TABLES" : {
        # main table to store Zi unicode and ENU translation
        CFG["TABLE_ZI"] : [
            'zi text NOT NULL',

            'desc text',
            'pinyin text',
            'nstrokes int',
            'alias text',

            'is_radical int',
            'is_zi int',
            'is_traditional int',

            'zi_en text',
            'desc_en text',

            'id text NOT NULL',
            'ts text',
            'uid text',
            'is_active int default 0'
        ],

        # Zi parts
        CFG["TABLE_PART"] : [
            'zi text NOT NULL',

            'zi_left_up text',      # left-up
            'zi_left text',         # left
            'zi_left_down text',    # left-down

            'zi_up text',           # up
            'zi_mid text',          # mid
            'zi_down text',         # down

            'zi_right_up text',     # right-up
            'zi_right text',        # right
            'zi_right_down text',   # right-down

            'zi_mid_front text',    # mid-front
            'zi_mid_back text',     # mid-back

            'id text NOT NULL',
            'ts text',
            'uid text',
            'is_active int default 0'
        ],

        # Zi Shufa
        CFG["TABLE_SHUFA"] : [
            'zi text NOT NULL',

            'seq_num int',
            'shufa_type text', 
            'url_img text', 

            'id text NOT NULL',
            'ts text',
            'uid text',
            'is_active int default 0'
        ],

        # word
        CFG["TABLE_WORD"] : [
            'zi text NOT NULL',

            'zi_0 text', 
            'zi_1 text', 
            'zi_2 text', 
            'zi_3 text', 
            'zi_4 text', 
            'zi_5 text', 
            'zi_6 text',             
            'zi_7 text', 
            'zi_8 text', 
            'zi_9 text', 

            'desc text', 

            'word_en text', 
            'desc_en text', 

            'id text NOT NULL',
            'ts text',
            'uid text',
            'is_active int default 0'
        ],

        # text
        CFG["TABLE_TEXT"] : [
            'zi text NOT NULL',

            'zi_text text', 
            'desc text', 

            'zi_text_en text', 
            'desc_en text', 

            'id text NOT NULL',
            'ts text',
            'uid text',
            'is_active int default 0'
        ],
        # media
        CFG["TABLE_MEDIA"] : [
            'zi text NOT NULL',

            'seq_num int',
            'media_type text',  #  url, image, audio, video, book 
            'desc text', 

            'desc_en text', 

            'id text NOT NULL',
            'ts text',
            'uid text',
            'is_active int default 0'
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

def db_create_table(table_name, conn, drop_table=False):
    cols = CFG["TABLES"][table_name]
    t_cols = ",\n\t".join(cols) 
    drop_create_table_sql = "" if not drop_table else f"drop table if exists {table_name};"
    drop_create_table_sql += f"""
        create table if not exists {table_name} 
        (
                {t_cols}
        );
    """
    # print(drop_create_table_sql)
    db_run_sql(drop_create_table_sql, conn)

def db_get_llm_models():
    return []
    # table_name = CFG["TABLE_MODEL"]
    # with DBConn() as _conn:
    #     sql_stmt = f"""
    #         select name from {table_name}
    #         order by name
    #     """
    #     df = pd.read_sql(sql_stmt, _conn)
    #     return [""] + df["name"].to_list()  # prepend blank
    
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
    "shufa_type": CFG["SHUFA_TYPE"],
}

# config UI layout for form-view
COLUMN_PROPS = {

    CFG["TABLE_ZI"]: {

        "zi": {
            "is_system_col": False,
            "is_user_key": True,
            "is_required": True,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-1",
            "widget_type": "text_input",
            "label_text": "字"
        },
        "desc": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-2",
            "widget_type": "text_area",
            "label_text": "解释"
        },
        "pinyin": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-3",
            "widget_type": "text_input",
            "label_text": "拼音"
        },
        "nstrokes": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_1-4",
            "widget_type": "number_input",
            "label_text": "笔画数"
        },

        "alias": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-1",
            "widget_type": "text_input",
            "label_text": "Alias"
        },
        "is_radical": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-2",
            "widget_type": "number_input",
            "label_text": "部首？"
        },
        "is_zi": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-3",
            "widget_type": "number_input",
            "label_text": "字？"
        },
        "is_traditional": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_2-4",
            "widget_type": "number_input",
            "label_text": "繁体？"
        },

        # col
        "zi_en": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_3-1",
            "widget_type": "text_area",
            "label_text": "English"
        },
        "desc_en": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_3-2",
            "widget_type": "text_area",
            "label_text": "Meaning"
        },

        # Column
        "id": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": True,
            "is_visible": True,
            "is_editable": False,
            "is_clickable": False,
            "form_column": "COL_4-1",
            "widget_type": "text_input",
            "label_text": "Id"
        },

        "ts": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": False,
            "is_clickable": False,
            "form_column": "COL_4-2",
            "widget_type": "text_input",
            "label_text": "Timestamp"
        },

        "uid": {
            "is_system_col": True,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": False,
            "is_clickable": False,
            "form_column": "COL_4-3",
            "widget_type": "text_input",
            "label_text": "UID"
        },

        "is_active": {
            "is_system_col": False,
            "is_user_key": False,
            "is_required": False,
            "is_visible": True,
            "is_editable": True,
            "is_clickable": False,
            "form_column": "COL_4-4",
            "widget_type": "number_input",
            "label_text": "Active?"
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
    col_col = {}
    col_prefix = [f"COL_{n}" for n in range(1,5)]  # max 4 columns
    for pfx in col_prefix:
        col_columns = col_col.get(pfx, [])
        for c in visible_columns:
            if form_columns.get(c, "").startswith(pfx):
                col_columns.append(c)
                col_col[pfx] = col_columns
    N_COLS = len(col_col.keys())

    with st.form(form_name, clear_on_submit=True):
        st_cols = st.columns(N_COLS)
        id_col = 0
        if len(st_cols) > id_col:
            with st_cols[id_col]:
                for col in col_col[col_prefix[id_col]]:
                    data = ui_layout_form_fields(data,form_name,old_row,col,
                                widget_types,col_labels,system_columns)

                if id_col == len(st_cols)-1:
                    # add checkbox for deleting this record
                    col = "delelte_record"
                    delete_flag = st.checkbox("Delelte Record?", value=False)
                    data.update({col: delete_flag})

        id_col = 1
        if len(st_cols) > id_col:
            with st_cols[id_col]:
                for col in col_col[col_prefix[id_col]]:
                    data = ui_layout_form_fields(data,form_name,old_row,col,
                                widget_types,col_labels,system_columns)

                if id_col == len(st_cols)-1:
                    # add checkbox for deleting this record
                    col = "delelte_record"
                    delete_flag = st.checkbox("Delelte Record?", value=False)
                    data.update({col: delete_flag})

        id_col = 2
        if len(st_cols) > id_col:
            with st_cols[id_col]:
                for col in col_col[col_prefix[id_col]]:
                    data = ui_layout_form_fields(data,form_name,old_row,col,
                                widget_types,col_labels,system_columns)

                if id_col == len(st_cols)-1:
                    # add checkbox for deleting this record
                    col = "delelte_record"
                    delete_flag = st.checkbox("Delelte Record?", value=False)
                    data.update({col: delete_flag})

        id_col = 3
        if len(st_cols) > id_col:
            with st_cols[id_col]:
                for col in col_col[col_prefix[id_col]]:
                    data = ui_layout_form_fields(data,form_name,old_row,col,
                                widget_types,col_labels,system_columns)

                if id_col == len(st_cols)-1:
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

