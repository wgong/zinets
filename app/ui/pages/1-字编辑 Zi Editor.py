"""
Note:

- st.data_editor() does not yet support row-selection, will use aggrid for now
    - https://discuss.streamlit.io/t/experimental-data-editor-how-to-retrieve-selection/40518
"""
from utils import *

st.set_page_config(layout="wide")
st.subheader("🐼 字编辑 Zi Editor 📝")

TABLE_NAME = CFG["TABLE_ZI"]
KEY_PREFIX = f"col_{TABLE_NAME}"

@st.cache_data
def query_layer():
    return db_query_layer()

def main():
    if "LAYERS" not in st.session_state:
        LAYERS = query_layer()
        st.session_state["LAYERS"] = LAYERS
    else:
        LAYERS = st.session_state["LAYERS"]

    c1, c2, c3, c4 = st.columns([1,6,2,1])
    with c1:
        search_term = st.text_input("🔍Search:", key=f"{KEY_PREFIX}_search_term").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause:", key=f"{KEY_PREFIX}_search_others").strip()
    with c3:
        search_layer = st.selectbox("🔍Layer", LAYERS, index=LAYERS.index(""), key=f"{KEY_PREFIX}_search_layer")
    with c4:
        active = st.selectbox("🔍Active?", ACTIVE_STATES, index=ACTIVE_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    where_clause = " 1=1 " 
    where_clause += " " if not active else f" and is_active = '{active}' "
    where_clause += " " if not search_layer else f" and layer = '{search_layer}' "

    if search_term:
        where_clause += f""" and (
            zi like '%{search_term}%'
            or alias like '%{search_term}%'
            or pinyin like '%{search_term}%'
            or zi_en like '%{search_term}%'
            or desc_cn like '%{search_term}%'
            or desc_en like '%{search_term}%'         
        )
        """
    if search_others:
        where_clause += f""" 
            and (
                {search_others}
        ) """


    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                zi
                , pinyin
                , alias
                , traditional
                , ifnull(as_part, '') as as_part
                , ifnull(is_radical, '') as is_radical
                , nstrokes
                , desc_cn
                , zi_en
                , desc_en
                , layer
                , u_id
                , ifnull(is_active, '')  as is_active
                , sort_val                
            from {TABLE_NAME}
            where {where_clause}
                and cast(u_id as real) > 1   -- exclude u_id=-1
            order by sort_val;
        """
        # st.write(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, selection_mode="single")
    selected_rows = grid_resp['selected_rows']

    # display form
    selected_row = selected_rows[0] if len(selected_rows) else None
    ui_layout_form(selected_row, TABLE_NAME)

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

if __name__ == '__main__':
    main()