from utils import *

st.set_page_config(layout="wide")
st.subheader("🐒 部件编辑 - Part Editor 📝")

TABLE_NAME = CFG["TABLE_ZI_PART"]
KEY_PREFIX = f"col_{TABLE_NAME}"
ZI_PART_COLS = [
    "zi_left_up", "zi_up", "zi_right_up",
    "zi_left", "zi_mid", "zi_right",
    "zi_left_down", "zi_down", "zi_right_down",
    "zi_mid_in", "zi_mid_out",
    "is_active",
    "desc_cn",
    "u_id",
    "ts"
]

@st.cache_data
def query_parts(strokes_clause):
    """concat all parts
    """
    sql_stmt = f"""
        select zi,traditional as zi_tr from t_part 
        where is_active = 'Y' and cast(strokes as int) {strokes_clause}
        order by cast(strokes as int), u_id
    """
    with DBConn() as _conn:
        df3 = pd.read_sql(sql_stmt, _conn)
    df3["zi2"] = df3["zi"] + df3["zi_tr"]
    parts  = df3["zi2"].to_list()
    return parts 


@st.cache_data 
def format_parts(chars_per_row=30):
    parts = []
    for i in range(1,9):
        parts.append(f"  [( {str(i)} )]  ")
        strokes_clause = f"={str(i)}"
        part = query_parts(strokes_clause)
        parts.extend(part)

    parts.append("  [( 9+ )]  ")
    strokes_clause = ">8"
    part = query_parts(strokes_clause)
    parts.extend(part)
    
    out = []
    for i in range(0, len(parts), chars_per_row):
        i_st = i 
        i_sp = i + chars_per_row
        out.append("".join(parts[i_st:i_sp]))
    return out

def main():
    # display grid

    st.session_state["table_name"] = TABLE_NAME
    search_term = st.text_input("🔍Search:", key=f"{KEY_PREFIX}_zi_search_editor").strip()
    if search_term:
        where_clause = f"""
            zi like '%{search_term}%'
            OR zi_left_up like '%{search_term}%'
            OR zi_left like '%{search_term}%'
            OR zi_left_down like '%{search_term}%'
            OR zi_up like '%{search_term}%'
            OR zi_mid like '%{search_term}%'
            OR zi_down like '%{search_term}%'
            OR zi_right_up like '%{search_term}%'
            OR zi_right like '%{search_term}%'
            OR zi_right_down like '%{search_term}%'
            OR zi_mid_out like '%{search_term}%'
            OR zi_mid_in like '%{search_term}%'
            OR u_id like '%{search_term}%'
        """
    else:
        where_clause = " 1=1 "

    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                zi
                , zi_left_up
                , zi_left
                , zi_left_down
                , zi_up
                , zi_mid
                , zi_down
                , zi_right_up
                , zi_right
                , zi_right_down
                , zi_mid_out
                , zi_mid_in
                , u_id
                , is_active
                , desc_cn
                , ts
            from {TABLE_NAME}
            where {where_clause}
            ;
        """
        # st.write(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, selection_mode="single")
    selected_rows = grid_resp['selected_rows']

    # display form
    zi = selected_rows[0] if len(selected_rows) else None

    if zi is None:
        return

    col_left, _, col_right = st.columns([6,1,10])

    st.session_state["selected_row_original_value"] = zi


    # display Zi form
    with col_left:
        with st.form(key="zi_parts"):
            c0_1,c0_2,c0_3 = st.columns([1,2,6])
            with c0_1:
                st.subheader(zi["zi"])
            with c0_2:
                st.text_input('ID', value=zi["u_id"], disabled=True, key=f"{KEY_PREFIX}_u_id")
                st.selectbox('Active?', ACTIVE_STATES, index=ACTIVE_STATES.index(fix_None_val(zi["is_active"])),  key=f"{KEY_PREFIX}_is_active")
            with c0_3:
                st.text_area('解释', value=zi["desc_cn"],  key=f"{KEY_PREFIX}_desc_cn")
                st.text_input("ts", value=zi["ts"], key=f"{KEY_PREFIX}_ts")

            c1_1,c1_2,c1_3,_ = st.columns(4)
            with c1_1:
                st.text_input('左上', value=zi["zi_left_up"],  key=f"{KEY_PREFIX}_zi_left_up")
            with c1_2:
                st.text_input('上', value=zi["zi_up"],  key=f"{KEY_PREFIX}_zi_up")
            with c1_3:
                st.text_input("右上", value=zi["zi_right_up"],  key=f"{KEY_PREFIX}_zi_right_up")

            c2_1,c2_2,c2_3,c2_4 = st.columns(4)
            with c2_1:
                st.text_input('左', value=zi["zi_left"],  key=f"{KEY_PREFIX}_zi_left")
            with c2_2:
                st.text_input('中', value=zi["zi_mid"],  key=f"{KEY_PREFIX}_zi_mid")
            with c2_3:
                st.text_input("右", value=zi["zi_right"],  key=f"{KEY_PREFIX}_zi_right")
            with c2_4:
                st.text_input('中外', value=zi["zi_mid_out"],  key=f"{KEY_PREFIX}_zi_mid_out")

            c3_1,c3_2,c3_3,c3_4 = st.columns(4)
            with c3_1:
                st.text_input('左下', value=zi["zi_left_down"],  key=f"{KEY_PREFIX}_zi_left_down")
            with c3_2:
                st.text_input('下', value=zi["zi_down"],  key=f"{KEY_PREFIX}_zi_down")
            with c3_3:
                st.text_input("右下", value=zi["zi_right_down"],  key=f"{KEY_PREFIX}_zi_right_down")
            with c3_4:
                st.text_input('中内', value=zi["zi_mid_in"],  key=f"{KEY_PREFIX}_zi_mid_in")


            st.form_submit_button('Save', on_click=_submit_zi_parts, use_container_width=True)

    # display Zi parts
    with col_right:
        st.subheader("Parts:")
        parts = format_parts()
        for p in parts:
            st.write(p)

def _submit_zi_parts():
    data = {}
    for c in ZI_PART_COLS:
        zp = st.session_state.get(f"{KEY_PREFIX}_{c}","")
        if c == "ts" and zp == "":
            zp = get_ts_now()
        data.update({c : zp})

    zi_orig_val = st.session_state.get("selected_row_original_value",None)
    if zi_orig_val is None: return

    # add id back
    data.update({
        "table_name": st.session_state["table_name"] 
    })

    if len(data) <= 1:
        print("No change, SKIP")
        return 
    
    # submit update to DB
    try:
        # print(zi_orig_val)
        print("DEBUG:======================")
        print(data)
        db_upsert(data)

    except Exception as e:
        print(f"[ERROR] _submit_zi_parts() failed:\n {str(e)}")

    # clear form
    try:
        for c in ZI_PART_COLS:
            st.session_state[f"{KEY_PREFIX}_{c}"] = ""
    except Exception as e:
        pass # ignore

if __name__ == '__main__':
    main()