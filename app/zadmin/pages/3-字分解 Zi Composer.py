"""
hand-crafted UI layout
"""
from utils import *

st.set_page_config(layout="wide")
st.subheader("🐒 字分解 Zi Decomposer 📝")

TABLE_NAME = CFG["TABLE_ZI_PART"]
st.session_state["KEY_PREFIX"] = f"col_{TABLE_NAME}"

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

    ## TODO following code not correct
    ## ================================
    # txt = f" {TAG_LEFT} 10+ {TAG_RIGHT} "
    # parts.append(colorize_text(txt))
    # strokes_clause = " > 9 "
    # part, n_part = query_parts(strokes_clause)
    # n_parts += n_part
    # parts.extend(part)

    out = []
    for i in range(0, len(parts), chars_per_row):
        i_st = i 
        i_sp = i + chars_per_row
        items = parts[i_st:i_sp]
        out.append("".join(items))
    return out, n_parts


def main():
    # fix detail form not refresh correctly when selection changes
    if "previous_zi" not in st.session_state:
        st.session_state.previous_zi = None

    KEY_PREFIX = st.session_state["KEY_PREFIX"]
    st.session_state["table_name"] = TABLE_NAME
    c1, c2, c3, c4 = st.columns([1,6,2,1])
    with c1:
        search_parts = st.text_input("🔍Search parts:", key=f"{KEY_PREFIX}_search_parts").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause (e.g.    cast(zi.u_id as int) > 0,  zi.zi = '佥'    ):", key=f"{KEY_PREFIX}_search_others").strip()
    with c3:
        search_layer = st.selectbox("🔍HSK Layer", HSK_LAYERS, index=HSK_LAYERS.index(""), key=f"{KEY_PREFIX}_search_layer")
    with c4:
        active = st.selectbox("🔍Active?", BI_STATES, index=BI_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    where_clause = " 1=1 " 
    where_clause += " " if not active  else f" and zi.is_active = '{active}' "

    if search_parts:
        where_clause += f""" 
            and (
                zi.zi like '%{search_parts}%'
                OR zp.zi_left_up like '%{search_parts}%'
                OR zp.zi_left like '%{search_parts}%'
                OR zp.zi_left_down like '%{search_parts}%'
                OR zp.zi_up like '%{search_parts}%'
                OR zp.zi_mid like '%{search_parts}%'
                OR zp.zi_down like '%{search_parts}%'
                OR zp.zi_right_up like '%{search_parts}%'
                OR zp.zi_right like '%{search_parts}%'
                OR zp.zi_right_down like '%{search_parts}%'
                OR zp.zi_mid_out like '%{search_parts}%'
                OR zp.zi_mid_in like '%{search_parts}%'
        ) """
    if search_others:
        where_clause += f""" 
            and (
                {search_others}
        ) """
    else:
        where_clause += " and 1=1 "

    if search_layer:
        where_clause += f"""
            and zi.layer = '{search_layer}'
        """
    else:
        where_clause += " and 1=1 "


    df = None
    with DBConn() as _conn:
        ### drive by t_zi
        sql_stmt = f"""
            select distinct
                zi.zi
                , zp.zi_left_up
                , zp.zi_left
                , zp.zi_left_down
                , zp.zi_up
                , zp.zi_mid
                , zp.zi_down
                , zp.zi_right_up
                , zp.zi_right
                , zp.zi_right_down
                , zp.zi_mid_out
                , zp.zi_mid_in
                , zp.desc_cn
                , zp.desc_en
                , zp.hsk_note
                , zi.layer as hsk_layer
                , c.caizi
                , zi.u_id
                , ifnull(zi.is_active, '') as is_active
            from  t_zi zi
            left join {TABLE_NAME} zp 
                on zi.zi = zp.zi
            left join w_caizi c
                on zi.zi = c.zi
            where {where_clause} 
                and cast(zi.u_id as real) > 0   -- exclude u_id=-1
            order by cast(zi.u_id as real)
            ;
        """

        # print(f"[DEBUG-SQL] {sql_stmt}")
        df = pd.read_sql(sql_stmt, _conn)

    # display grid
    grid_resp = ui_display_df_grid(
            df, 
            selection_mode="single",
            # temp use
            page_size=10,
            grid_height=int(0.95*AGGRID_OPTIONS["grid_height"]),
        )
 

    selected_rows = grid_resp['selected_rows']
    # zi = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]

    if selected_rows is None or len(selected_rows) < 1:
        return

    zi = selected_rows.iloc[0].to_dict() if isinstance(selected_rows, pd.DataFrame) else selected_rows[0]
    if zi != st.session_state.previous_zi:
        st.session_state.previous_zi = zi
        st.rerun()

    # st.write(zi)
    msg = ""
    zi_zi = zi.get("zi") if zi else ""
    zi_u_id = zi.get("u_id") if zi else ""
    zi_is_active = zi.get("is_active") if zi else ""
    zi_desc_cn = zi.get("desc_cn") if zi else ""
    # zi_ts = zi.get("ts")

    zi_zi_left_up = zi.get("zi_left_up") if zi else ""
    if zi_zi_left_up: msg += f"zi_zi_left_up={zi_zi_left_up}, "

    zi_zi_up = zi.get("zi_up") if zi else ""
    if zi_zi_up: msg += f"zi_zi_up={zi_zi_up}, "

    zi_zi_right_up = zi.get("zi_right_up") if zi else ""
    if zi_zi_right_up: msg += f"zi_zi_right_up={zi_zi_right_up}, "

    zi_zi_left = zi.get("zi_left") if zi else ""
    if zi_zi_left: msg += f"zi_zi_left={zi_zi_left}, "

    zi_zi_mid = zi.get("zi_mid") if zi else ""
    if zi_zi_mid: msg += f"zi_zi_mid={zi_zi_mid}, "

    zi_zi_right = zi.get("zi_right") if zi else ""
    if zi_zi_right: msg += f"zi_zi_right={zi_zi_right}, "

    zi_zi_mid_out = zi.get("zi_mid_out") if zi else ""
    if zi_zi_mid_out: msg += f"zi_zi_mid_out={zi_zi_mid_out}, "

    zi_zi_left_down = zi.get("zi_left_down") if zi else ""
    if zi_zi_left_down: msg += f"zi_zi_left_down={zi_zi_left_down}, "

    zi_zi_down = zi.get("zi_down") if zi else ""
    if zi_zi_down: msg += f"zi_zi_down={zi_zi_down}, "

    zi_zi_right_down = zi.get("zi_right_down") if zi else ""
    if zi_zi_right_down: msg += f"zi_zi_right_down={zi_zi_right_down}, "

    zi_zi_mid_in = zi.get("zi_mid_in") if zi else ""
    if zi_zi_mid_in: msg += f"zi_zi_mid_in={zi_zi_mid_in}, "

    zi_desc_en = zi.get("desc_en") if zi else ""
    zi_hsk_layer = zi.get("hsk_layer") if zi else ""
    zi_hsk_note = zi.get("hsk_note") if zi else ""
    zi_caizi = zi.get("caizi") if zi else ""
    msg += f"zi_caizi={zi_caizi}, "
    # st.write(f"DEBUG: {msg}")
    col_left, col_right = st.columns([10,10])

    st.session_state["selected_row_original_value"] = zi

    # display Zi form
    with col_left:
        # with st.form(key="zi_parts"):
        c0_1,c0_3,c0_4,c0_5 = st.columns([2,5,4,2])
        with c0_1:
            zi_title = f"""
            <span style="color:red; font-size:5.6em;">{zi_zi}</span>
            """
            st.markdown(zi_title, unsafe_allow_html=True)
        with c0_3:
            st.text_area('解释', value=zi_desc_cn,  key=f"{KEY_PREFIX}_desc_cn")
        with c0_4:
            st.text_area('Explanation', value=zi_desc_en,  key=f"{KEY_PREFIX}_desc_en")
        with c0_5:
            st.text_input('HSK note', value=zi_hsk_note,  key=f"{KEY_PREFIX}_hsk_note")

        c4_0, c4_1, c4_2, c4_3, c4_4 = st.columns([1, 3, 3, 1, 2 ])
        with c4_0:
            st.text_input('字 zi', value=zi_zi, key=f"{KEY_PREFIX}_zi")
        with c4_1:
            st.text_input("拆字", value=zi_caizi, key=f"{KEY_PREFIX}_caizi")
        with c4_2:
            st.text_input('HSK layer', value=zi_hsk_layer,  key=f"{KEY_PREFIX}_hsk_layer")
        with c4_3:
            st.text_input('ID', value=zi_u_id, disabled=True, key=f"{KEY_PREFIX}_u_id")
        with c4_4:
            # st.form_submit_button(STR_SAVE, on_click=_submit_zi_parts, use_container_width=True)
            st.button(STR_SAVE, on_click=_submit_zi_parts)

        c1_1,c1_2,c1_3,c1_4 = st.columns([2,2,2,2])
        with c1_1:
            st.text_input('左上 left_up', value=zi_zi_left_up,  key=f"{KEY_PREFIX}_zi_left_up")
        with c1_2:
            st.text_input('上 up', value=zi_zi_up,  key=f"{KEY_PREFIX}_zi_up")
        with c1_3:
            st.text_input("右上 right_up", value=zi_zi_right_up,  key=f"{KEY_PREFIX}_zi_right_up")
        with c1_4:
            st.selectbox('Active?', BI_STATES, index=BI_STATES.index(fix_None_val(zi_is_active)),  key=f"{KEY_PREFIX}_is_active")

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

        st.subheader(f"元字 ({n_parts}):")
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
    KEY_PREFIX = st.session_state["KEY_PREFIX"]
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