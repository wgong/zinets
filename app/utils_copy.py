"""
# ToDo
- [2024-01-20]

# Done
- [2024-01-20]
    - fixed issue in db_execute() to allow matching by `zi`
"""

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
    AgGrid, GridOptionsBuilder, GridUpdateMode
    , JsCode, DataReturnMode
)

from ui_layout import *


#############################
# Config params (1st)
#############################
BLANK_STR_VALUE = ""   # place-holder blank LOV value

STR_SAVE = "✅ Save" # 💾
CFG = {
    "DEBUG_FLAG" : True, # False, # 
    "SQL_EXECUTION_FLAG" : True, #  False, #   control SQL
    
    # "DB_FILENAME" : Path(__file__).parent / "zinets.sqlite",
    "DB_FILENAME" : Path(__file__).parent / "ui" / "zizi.sqlite",

    # assign table names
    "TABLE_ZI" : "t_zi",            # all Zi 字
    "TABLE_PART" : "t_part",        # parts - not exposed in UI
    "TABLE_ZI_PART" : "t_zi_part",  # decomposed Zi 字子
    "TABLE_SHUFA" : "t_shufa",      # ShuFa 书法
    "TABLE_WORD" : "t_phrase",      # phrase/word 词语
    "TABLE_TEXT" : "t_text",        # text 文章 
    "TABLE_MEDIA" : "t_resource",   # audio/video 录音，视频
    "TABLE_NOTE" : "t_note",        # Note on Journal/Resource

    "SHUFA_TYPE": [BLANK_STR_VALUE, "甲骨", "金", "篆", "隶", "楷", "行", "草"],
    "NOTE_TYPE": [BLANK_STR_VALUE, "RESOURCE", "JOURNAL", "APP","PROJECT", "TASK",],
    "STATUS_CODE": [BLANK_STR_VALUE, "ToDo","WIP", "Complete", "Blocked","De-Scoped",],
}

# define options for selectbox column type, keyed on column name
ACTIVE_STATES = ["Y", BLANK_STR_VALUE, ]   # add empty-str as placeholder
SELECTBOX_OPTIONS = {
    "is_active": ACTIVE_STATES,
    "is_radical": ACTIVE_STATES,
    "as_part": ACTIVE_STATES,
    "shufa_type": CFG["SHUFA_TYPE"],
    "note_type": CFG["NOTE_TYPE"],
    "status_code": CFG["STATUS_CODE"],
}

# temp workaround
ZI_PART_COLS = [
    "zi",
    "zi_left_up", "zi_up", "zi_right_up",
    "zi_left", "zi_mid", "zi_right",
    "zi_left_down", "zi_down", "zi_right_down",
    "zi_mid_in", "zi_mid_out",
    "is_active",
    "desc_cn",
    "desc_en",
    "hsk_note",
    "u_id",
    "ts",
    "caizi",
]

def fix_None_val(v):
    return "" if v is None else v

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


def db_run_sql(sql_stmt, conn=None, debug=CFG["DEBUG_FLAG"]):
    """handles both select and insert/update/delete
    """
    if not sql_stmt or conn is None:
        return None
    
    debug_print(sql_stmt, debug=debug)

    if sql_stmt.lower().strip().startswith("select"):
        return pd.read_sql(sql_stmt, conn)
    
    cur = conn.cursor()
    cur.executescript(sql_stmt)
    conn.commit()
    # conn.close()
    return None


def db_execute(sql_statement, 
               debug=CFG["DEBUG_FLAG"], 
               execute_flag=CFG["SQL_EXECUTION_FLAG"],):
    """handles insert/update/delete
    """
    with DBConn() as _conn:
        debug_print(sql_statement, debug=debug)
        if execute_flag:
            _conn.execute(sql_statement)
            _conn.commit()
        else:
            print("[WARN] SQL Execution is off ! ")   

def db_query_layer():
    sql_stmt = f"""
        select distinct layer 
        from {CFG["TABLE_ZI"]}
        order by layer;
    """
    with DBConn() as _conn:
        df = pd.read_sql(sql_stmt, _conn)
    return [""] + df["layer"].to_list()

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
            where u_id = '{id_value}' ;
        """
        return pd.read_sql(sql_stmt, _conn).fillna("").to_dict('records')


def trim_str_col_val(data):
    data_new = {}
    for k,v in data.items():
        if isinstance(v, str):
            v = v.strip()
        data_new.update({k:v})
    return data_new

def db_upsert(data, user_key_cols="u_id", call_meta_func=False):
    """ u_id = '-1' are marked for deletion
    """
    if not data: 
        return None

    table_name = data.get("table_name", "")
    if not table_name:
        raise Exception(f"[ERROR] Missing table_name: {data}")
    
    # build SQL
    if call_meta_func:
        visible_columns = get_columns(table_name, prop_name="is_visible")
    else:
        # temp workaround
        visible_columns = get_all_columns(table_name)
    # print(f"visible_columns = {visible_columns}")

    data = trim_str_col_val(data)

    sql_type = "INSERT"
    id_ = data.get(user_key_cols, "None")
    if id_ is None or id_ == "None":
        id_ = ""
        sql_type = "INSERT"

    zi_ = data.get("zi", "").strip()
    if id_ and id_ not in ['-1']:
        with DBConn() as _conn:
            sql_stmt = f"""
                select *
                from {table_name} 
                where {user_key_cols} = '{id_}';
            """
            rows = pd.read_sql(sql_stmt, _conn).to_dict('records')

            if len(rows):
                sql_type = "UPDATE"  
                old_row = rows[0]
                id_ = old_row.get(user_key_cols)         
           
    elif zi_:
        # query by Zi
        with DBConn() as _conn:
            sql_stmt = f"""
                select *
                from {table_name} 
                where trim(zi) = '{zi_}' and u_id not in ('-1');
            """
            rows = pd.read_sql(sql_stmt, _conn).to_dict('records')

            if len(rows):
                sql_type = "UPDATE"  
                old_row = rows[0]
                id_ = old_row.get("u_id")         

    if id_ is None or id_ in ["None", "-1"]:
        id_ = ""
        sql_type = "INSERT"

    upsert_sql = ""
    if sql_type == "INSERT":

        col_clause = []
        val_clause = []
        for col,val in data.items():
            if col not in visible_columns:
                continue
            if col == user_key_cols and not val:
                continue
            col_clause.append(col)
            col_val = escape_single_quote(val)
            val_clause.append(f"'{col_val}'")
        col_clause.append(user_key_cols)
        val_clause.append("id")

        upsert_sql = f"""
            with uid as (
                select 
                case 
                    when max({user_key_cols}) is NULL then '10' 
                    else cast(max(cast({user_key_cols} as int))+1 as text) 
                end as id
                from {table_name}
                where {user_key_cols} not in ('-1')
            )
            insert into {table_name} (
                {", ".join(col_clause)}
            )
            select {", ".join(val_clause)} 
            from uid;
        """
            # values (
            #     {", ".join(val_clause)}
            # );

    else:
        set_clause = []
        for col in visible_columns:
            if col == user_key_cols: continue

            if col == "is_active":
                val = data.get(col, "")
                old_val = old_row.get(col, "")
                if old_val is None:
                    old_val = ""
            else:
                val = data.get(col, 1)
                old_val = old_row.get(col, 1)
            if isinstance(val, str):
                val = val.strip()
            if (val and old_val and val == old_val) or (not val and not old_val):
                continue

            col_val = escape_single_quote(val)
            set_clause.append(f" {col} = '{col_val}'")

        if set_clause:
            upsert_sql = f"""
                update {table_name} 
                set 
                    {", ".join(set_clause)}
                where {user_key_cols} = '{id_}';
            """

    if upsert_sql:
        try:
            db_execute(upsert_sql, 
                    debug=CFG["DEBUG_FLAG"], 
                    execute_flag=CFG["SQL_EXECUTION_FLAG"], 
                )
        except Exception as ex:
            print(f"[ERROR] db_upsert():\n\t{str(ex)}")

def db_delete_by_id(data):
    if not data: 
        return None
    
    table_name = data.get("table_name", "")
    if not table_name:
        raise Exception(f"[ERROR] Missing table_name: {data}")

    id_val = data.get("u_id", "")
    if not id_val:
        return None
    
    delete_sql = f"""
        delete from {table_name}
        where u_id = '{id_val}';
    """
    db_execute(delete_sql, 
                debug=CFG["DEBUG_FLAG"], 
                execute_flag=CFG["SQL_EXECUTION_FLAG"], 
        )    

def db_update_by_id(data, update_changed=True):
    if not data: 
        return
    
    table_name = data.get("table_name", "")
    if not table_name:
        raise Exception(f"[ERROR] Missing table_name: {data}")

    id_val = data.get("u_id", "")
    if not id_val:
        return


    if update_changed:
        rows = db_select_by_id(table_name=table_name, id_value=id_val)
        if len(rows) < 1:
            return
        old_row = rows[0]

    editable_columns = get_columns(table_name, prop_name="is_editable")

    # build SQL
    set_clause = []
    for col,val in data.items():
        if col not in (editable_columns + ["ts"]): 
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
            where u_id = '{id_val}';
        """
        db_execute(update_sql, 
                    debug=CFG["DEBUG_FLAG"], 
                    execute_flag=CFG["SQL_EXECUTION_FLAG"], 
            )

# deprecated
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
    results=soup.findAll("div", class_="contents")
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
    return s.strip().replace("\'", "\'\'")

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
    "grid_height": 370,
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
SYS_COLS = ["id","ts","u_id"]

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



def map_streamlit_widget_type(col_name, data_type):
    if data_type in ("real", "integer"):
        return "number_input"
    else:
        if (col_name.startswith("is_") or col_name.startswith("has_") or col_name.startswith("as_")):
            return "selectbox"
        else:
            return "text_input"

def init_cap(col_name):
    return " ".join([c.capitalize() for c in col_name.split("_")])

def parse_ddl_reserved(x):
    x = x.strip()
    for kw in ["--", "primary ", "not ", "default "]:
        if kw in x: 
            x = x.split(kw)[0].strip()
    return x

def parse_ddl_line(line):
    """handle , and --, returns a list of column definition
    """
    res = []
    x = line.strip()
    if x.startswith("--"):
        return res
    
    for j in [i.strip() for i in x.split(",") if i.strip()]:
        j = parse_ddl_reserved(j)
        if j:
            res.append(j)
    return res

def parse_ddl(ddl_str, filtered_types=[]):
    """Parse DDL text string into col_datatype map
    
    filtered_types = []: return all, else only specified types
    """
    out = []
    for i in ddl_str.lower().split("create "):
        if not i.startswith("table "): continue 
        out.append(i.split("\n"))
        
    # table_names = []
    col_datatypes = {}
    for t in out:
        if "table" in t[0]:
            table_name = t[0].split()[-1]
        # table_names.append(table_name)
        else:
            print(f"[ERROR] Table name not found: {t}")
            continue
            
        t2 = t[1:]
        i_st = i_sp = -2
        for i in range(len(t2)):
            x = t2[i].strip()
            if x.startswith("("):
                i_st = i
            elif x.startswith(")"):
                i_sp = i
        if i_st == -2 or i_sp == -2:
            print(f"[ERROR] Missing parathesis: {t2}")
            continue 

        t3 = []
        for i in t2[i_st+1:i_sp]:
            line = i.strip()
            res = parse_ddl_line(line)
            if res: 
                t3.extend(res)

        m = {}
        for x in t3:
            y = x.strip().split()
            if len(y) == 0: 
                continue
            col_name = y[0]
            datatype = "text" if len(y) < 2 else y[1]
            if not filtered_types or datatype in filtered_types:
                m[col_name] = datatype
                
        col_datatypes[table_name] = m
    
    return col_datatypes

def prepare_column_props(col_defn):
    """Prepare UI config
    """
    col_props = {}
    for table_name in col_defn.keys():
        col_types = col_defn[table_name]
        col_props[table_name] = {}
        for col_name, data_type in col_types.items():
            widget_type = map_streamlit_widget_type(col_name, data_type)
            label_text = init_cap(col_name)
            col_props[table_name].update({
                col_name : dict(
                    is_system_col=False,
                    is_user_key=False,
                    is_required=False,
                    is_visible=True,
                    is_editable=True,
                    is_clickable=False,
                    datatype=data_type,
                    form_column="COL_1-1",
                    widget_type=widget_type,
                    label_text=label_text,
                )})
    return col_props

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



def get_all_columns(table_name):
    cols = COLUMN_PROPS[table_name].keys()
    out = [c.split()[0] for c in cols]
    if table_name == "t_zi_part":
        out = ZI_PART_COLS
    return out

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
    key_name_field = f"col_{form_name}_{col}"
    if old_row:
        old_val = old_row.get(col, "")
        widget_type = widget_types.get(col, "text_input")
        if widget_type == "text_area":
            kwargs = {"height":125}
            val = st.text_area(col_labels.get(col), value=old_val, disabled=DISABLED, key=key_name_field, kwargs=kwargs)
        elif widget_type == "date_input":
            old_date_input = old_val.split("T")[0]
            if old_date_input:
                val_date = datetime.strptime(old_date_input, "%Y-%m-%d")
            else:
                val_date = datetime.now().date()
            val = st.date_input(col_labels.get(col), value=val_date, disabled=DISABLED, key=key_name_field)
            val = datetime.strftime(val, "%Y-%m-%d")
        elif widget_type == "time_input":
            old_time_input = old_val
            if old_time_input:
                val_time = datetime.strptime(old_time_input.split(".")[0], "%H:%M:%S").time()
            else:
                val_time = datetime.now().time()
            val = st.time_input(col_labels.get(col), value=val_time, disabled=DISABLED, key=key_name_field)
        elif widget_type == "selectbox":
            # check if options is avail, otherwise display as text_input
            if col in SELECTBOX_OPTIONS:
                try:
                    _options = SELECTBOX_OPTIONS.get(col,[])
                    old_val = old_row.get(col, BLANK_STR_VALUE)
                    _idx = _options.index(old_val)
                    val = st.selectbox(col_labels.get(col), _options, index=_idx, key=key_name_field)
                except ValueError:
                    val = old_row.get(col, "")
            else:
                val = st.text_input(col_labels.get(col), value=old_val, disabled=DISABLED, key=key_name_field)

        else:
            val = st.text_input(col_labels.get(col), value=old_val, disabled=DISABLED, key=key_name_field)

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
    id_val = old_row.get("u_id", "")
    if id_val:
        data.update({"u_id" : id_val})

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

    key_names = []
    with st.form(form_name, clear_on_submit=True):
        st_cols = st.columns(N_COLS)
        id_col = 0
        if len(st_cols) > id_col:
            with st_cols[id_col]:
                for col in col_col[col_prefix[id_col]]:
                    data = ui_layout_form_fields(data,form_name,old_row,col,
                                widget_types,col_labels,system_columns)
                    key_names.append(f"col_{form_name}_{col}")

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
                    key_names.append(f"col_{form_name}_{col}")

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
                    key_names.append(f"col_{form_name}_{col}")

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
                    key_names.append(f"col_{form_name}_{col}")

                if id_col == len(st_cols)-1:
                    # add checkbox for deleting this record
                    col = "delelte_record"
                    delete_flag = st.checkbox("Delelte Record?", value=False)
                    data.update({col: delete_flag})

        save_btn = st.form_submit_button(STR_SAVE)  
        if save_btn:
            try:
                delete_flag = data.get("delelte_record", False)
                if delete_flag:
                    if data.get("u_id"):
                        db_delete_by_id(data)
                else:
                    if data.get("u_id"):
                        data.update({"ts": get_ts_now(),
                                    })
                        db_update_by_id(data)
                    else:
                        data.update({
                                    "ts": get_ts_now(),
                                    })
                        db_upsert(data)

            except Exception as ex:
                st.error(f"{str(ex)}")

        # clear form
        try:
            for c in key_names:
                st.session_state[c] = ""
        except Exception as e:
            pass # ignore


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
        js_code = """
            function(params) {return params.value ? `<a href=${params.value} target="_blank">${params.value}</a>` : "" }
        """
        cell_renderer_url =  JsCode(js_code)
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

def df_to_csv(df, index=False):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=index).encode('utf-8')
