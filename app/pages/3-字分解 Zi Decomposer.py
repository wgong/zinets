"""
hand-crafted UI layout
"""
from utils import *

st.set_page_config(layout="wide")
st.subheader("🐒 字分解 Zi Decomposer 📝")

TABLE_NAME = CFG["TABLE_ZI_PART"]
KEY_PREFIX = f"col_{TABLE_NAME}"


TAG_LEFT = "|["
TAG_RIGHT = "]|"

@st.cache_data
def colorize_text(txt, color="red"):
    return f"""<span style="color:{color}">{txt}</span>"""

# @st.cache_data
def query_parts(strokes_clause):
    """query and concat all parts based on strokes
        if =n:  (n = 1..9)
        else: strokes is null or >9
    """
    if strokes_clause.strip().startswith("="):
        where_clause = f""" 
            cast(strokes as int) {strokes_clause} 
        """
    else:
        one2nine = str(list(range(1,10)))
        where_clause = f""" 
            (
                strokes is null or cast(strokes as int) not 
                    in {one2nine.replace("[","(").replace("]",")")}
            )
        """
    # sql_stmt = f"""
    #     select 
    #         distinct zi
    #         ,traditional as zi_tr 
    #     from t_part 
    #     where is_active = 'Y' 
    #         and zi is not null
    #         and {where_clause}
    #     order by cast(strokes as int), u_id
    # """
    sql_stmt = f"""
        with parts as (
            select 
                zi
                ,traditional as zi_tr
                , strokes
                , u_id
            from t_part 
            where is_active = 'Y' 
                and zi is not null
            union all
            select 
                zi
                ,traditional as zi_tr
                , nstrokes as strokes
                , u_id
            from t_zi
            where is_active = 'Y' 
                and zi is not null
                and as_part = 'Y'                       
        )
        select 
            distinct zi
            -- , zi_tr 
        from parts
        where {where_clause}
            order by cast(strokes as int), u_id    
    """
    # if CFG["DEBUG_FLAG"]:
    #     print(sql_stmt)

    with DBConn() as _conn:
        df3 = pd.read_sql(sql_stmt, _conn).fillna("")
    # df3["zi2"] = df3["zi"] + df3["zi_tr"]
    # parts  = df3["zi2"].to_list()
    parts  = df3["zi"].to_list()

    out = [p for p in parts if isinstance(p, str)]
    return out, len(out)

# @st.cache_data 
def format_parts(chars_per_row=30):
    n_parts = 0
    parts = []
    for i in range(1,10):
        txt = f" {TAG_LEFT} {str(i)} {TAG_RIGHT} "
        parts.append(colorize_text(txt))
        strokes_clause = f"={str(i)}"
        part, n_part = query_parts(strokes_clause)
        n_parts += n_part
        parts.extend(part)

    txt = f" {TAG_LEFT} 10+ {TAG_RIGHT} "
    parts.append(colorize_text(txt))
    strokes_clause = "null or >9"
    part, n_part = query_parts(strokes_clause)
    n_parts += n_part
    parts.extend(part)

    out = []
    for i in range(0, len(parts), chars_per_row):
        i_st = i 
        i_sp = i + chars_per_row
        items = parts[i_st:i_sp]
        out.append("".join(items))
    return out, n_parts

@st.cache_data
def query_layer():
    return db_query_layer()

def main():
    if "LAYERS" not in st.session_state:
        LAYERS = query_layer()
        st.session_state["LAYERS"] = LAYERS
    else:
        LAYERS = st.session_state["LAYERS"]

    st.session_state["table_name"] = TABLE_NAME
    c1, c2, c3, c4 = st.columns([1,6,2,1])
    with c1:
        search_parts = st.text_input("🔍Search parts:", key=f"{KEY_PREFIX}_search_parts").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause (e.g.    cast(z.u_id as int) > 1,  z.zi = '佥'    ):", key=f"{KEY_PREFIX}_search_others").strip()
    with c3:
        search_layer = st.selectbox("🔍Layer", LAYERS, index=LAYERS.index(""), key=f"{KEY_PREFIX}_search_layer")
    with c4:
        active = st.selectbox("🔍Active?", ACTIVE_STATES, index=ACTIVE_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    where_clause = " 1=1 " 
    where_clause += " " if not active  else f" and z.is_active = '{active}' "

    if search_parts:
        where_clause += f""" 
            and (
                z.zi like '%{search_parts}%'
                OR z.zi_left_up like '%{search_parts}%'
                OR z.zi_left like '%{search_parts}%'
                OR z.zi_left_down like '%{search_parts}%'
                OR z.zi_up like '%{search_parts}%'
                OR z.zi_mid like '%{search_parts}%'
                OR z.zi_down like '%{search_parts}%'
                OR z.zi_right_up like '%{search_parts}%'
                OR z.zi_right like '%{search_parts}%'
                OR z.zi_right_down like '%{search_parts}%'
                OR z.zi_mid_out like '%{search_parts}%'
                OR z.zi_mid_in like '%{search_parts}%'
        ) """
    if search_others:
        where_clause += f""" 
            and (
                {search_others}
        ) """

    if search_layer:
        where_clause += f"""
            and z.zi in (
                select zi from {CFG["TABLE_ZI"]}
                where layer = '{search_layer}'
            )
        """


    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                z.zi
                , z.zi_left_up
                , z.zi_left
                , z.zi_left_down
                , z.zi_up
                , z.zi_mid
                , z.zi_down
                , z.zi_right_up
                , z.zi_right
                , z.zi_right_down
                , z.zi_mid_out
                , z.zi_mid_in
                , z.u_id
                , ifnull(z.is_active, '') as is_active
                , z.desc_cn
                , z.desc_en
                , z.hsk_note
                , c.caizi
            from {TABLE_NAME} z 
            left join w_caizi c
                on z.zi = c.zi
            where {where_clause} 
                and cast(z.u_id as real) > 1   -- exclude u_id=-1
            order by cast(z.u_id as integer)
            ;
        """
        # st.write(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)

    # display grid
    grid_resp = ui_display_df_grid(
            df, 
            selection_mode="single",
            # temp use
            page_size=10,
            grid_height=int(1.0*AGGRID_OPTIONS["grid_height"]),
        )
 

    selected_rows = grid_resp['selected_rows']
    # display form
    zi = selected_rows[0] if len(selected_rows) else None
    if zi is not None:
        zi_zi = zi["zi"]
        zi_u_id = zi["u_id"]
        zi_is_active = zi["is_active"]
        zi_desc_cn = zi["desc_cn"]
        # zi_ts = zi["ts"]
        zi_zi_left_up = zi["zi_left_up"]
        zi_zi_up = zi["zi_up"]
        zi_zi_right_up = zi["zi_right_up"]
        zi_zi_left = zi["zi_left"]
        zi_zi_mid = zi["zi_mid"]
        zi_zi_right = zi["zi_right"]
        zi_zi_mid_out = zi["zi_mid_out"]
        zi_zi_left_down = zi["zi_left_down"]
        zi_zi_down = zi["zi_down"]
        zi_zi_right_down = zi["zi_right_down"]
        zi_zi_mid_in = zi["zi_mid_in"]
        zi_desc_en = zi["desc_en"]
        zi_hsk_note = zi["hsk_note"]
        zi_caizi = zi["caizi"]
    else:
        zi_zi = ""
        zi_u_id = ""
        zi_is_active = ""
        zi_desc_cn = ""
        # zi_ts = ""
        zi_zi_left_up = ""
        zi_zi_up = ""
        zi_zi_right_up = ""
        zi_zi_left = ""
        zi_zi_mid = ""
        zi_zi_right = ""
        zi_zi_mid_out = ""
        zi_zi_left_down = ""
        zi_zi_down = ""
        zi_zi_right_down = ""
        zi_zi_mid_in = ""
        zi_desc_en = ""
        zi_hsk_note = ""
        zi_caizi = ""

    col_left, col_right = st.columns([10,10])

    st.session_state["selected_row_original_value"] = zi


    # display Zi form
    with col_left:
        with st.form(key="zi_parts"):
            c0_1,c0_3,c0_4 = st.columns([2,6,6])
            with c0_1:
                zi_title = f"""
                <span style="color:red; font-size:5.6em;">{zi_zi}</span>
                """
                st.markdown(zi_title, unsafe_allow_html=True)
            with c0_3:
                st.text_area('解释', value=zi_desc_cn,  key=f"{KEY_PREFIX}_desc_cn")
            with c0_4:
                st.text_area('Explanation', value=zi_desc_en,  key=f"{KEY_PREFIX}_desc_en")
                # st.text_input("ts", value=zi_ts, key=f"{KEY_PREFIX}_ts")

            c4_0, c4_1,c4_2,c4_3, c4_4 = st.columns([1, 3, 4, 1, 1 ])
            with c4_0:
                st.text_input('字 zi', value=zi_zi, key=f"{KEY_PREFIX}_zi")
            with c4_1:
                st.text_input("拆字", value=zi_caizi, key=f"{KEY_PREFIX}_caizi")
            with c4_2:
                st.text_input('HSK note', value=zi_hsk_note,  key=f"{KEY_PREFIX}_hsk_note")
            with c4_3:
                st.text_input('ID', value=zi_u_id, disabled=True, key=f"{KEY_PREFIX}_u_id")
            with c4_4:
                st.form_submit_button(STR_SAVE, on_click=_submit_zi_parts, use_container_width=True)


            c1_1,c1_2,c1_3,c1_4,c1_5 = st.columns([2,2,2,1,1])
            with c1_1:
                st.text_input('左上 left_up', value=zi_zi_left_up,  key=f"{KEY_PREFIX}_zi_left_up")
            with c1_2:
                st.text_input('上 up', value=zi_zi_up,  key=f"{KEY_PREFIX}_zi_up")
            with c1_3:
                st.text_input("右上 right_up", value=zi_zi_right_up,  key=f"{KEY_PREFIX}_zi_right_up")
            with c1_4:
                st.selectbox('Active?', ACTIVE_STATES, index=ACTIVE_STATES.index(fix_None_val(zi_is_active)),  key=f"{KEY_PREFIX}_is_active")

            c2_1,c2_2,c2_3,c2_4 = st.columns([2,2,2,2])
            with c2_1:
                st.text_input('左 left', value=zi_zi_left,  key=f"{KEY_PREFIX}_zi_left")
            with c2_2:
                st.text_input('中 mid', value=zi_zi_mid,  key=f"{KEY_PREFIX}_zi_mid")
            with c2_3:
                st.text_input("右 right", value=zi_zi_right,  key=f"{KEY_PREFIX}_zi_right")
            with c2_4:
                st.text_input('中外 mid_outer', value=zi_zi_mid_out,  key=f"{KEY_PREFIX}_zi_mid_out")

            c3_1,c3_2,c3_3,c3_4 = st.columns([2,2,2,2])
            with c3_1:
                st.text_input('左下 left_down', value=zi_zi_left_down,  key=f"{KEY_PREFIX}_zi_left_down")
            with c3_2:
                st.text_input('下 down', value=zi_zi_down,  key=f"{KEY_PREFIX}_zi_down")
            with c3_3:
                st.text_input("右下 right_down", value=zi_zi_right_down,  key=f"{KEY_PREFIX}_zi_right_down")
            with c3_4:
                st.text_input('中内 mid_inner', value=zi_zi_mid_in,  key=f"{KEY_PREFIX}_zi_mid_in")

    # display Zi parts
    with col_right:
        parts, n_parts = format_parts(40)

        st.subheader(f"Parts ({n_parts}):")
        for p in parts:
            st.markdown(p, unsafe_allow_html=True)

    # optional download
    with st.expander("Download CSV", expanded=False):
        _, c1, _ = st.columns([5,2,5])
        with c1:
            st.download_button(
                label="Submit",
                data=df_to_csv(df, index=False),
                file_name=f"{TABLE_NAME}-{get_ts_now()}.csv",
                mime='text/csv',
            )               


def _submit_zi_parts():
    data = {}
    for c in ZI_PART_COLS:
        zp = st.session_state.get(f"{KEY_PREFIX}_{c}","")
        if c == "ts" and zp == "":
            zp = get_ts_now()
        if c == "caizi": continue  # skip caizi
        data.update({c : zp})

    zi_orig_val = st.session_state.get("selected_row_original_value",None)
    # if zi_orig_val is None: return
    # commented out on 2024-01-20 to allow adding

    # add id back
    data.update({
        "table_name": st.session_state["table_name"] 
    })

    if len(data) <= 1:
        print("No change, SKIP")
        return 
    
    # submit update to DB
    try:
        if CFG["DEBUG_FLAG"]:
            print("DEBUG:======================")
            print(f"[SelectedRow]\n\t {zi_orig_val}")
            print(f"[DATA]\n\t {data}")
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