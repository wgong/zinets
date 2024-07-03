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

    c_zi, c2, c_cat, c_set_id, c_layer, c_active = st.columns([1,5,2,1,2,1])
    with c_zi:
        search_term = st.text_input("🔍Search Zi:", key=f"{KEY_PREFIX}_search_term").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause  (e.g.    cast(u_id as int) > 0,  zi = '佥'    ):", key=f"{KEY_PREFIX}_search_others").strip()
    with c_cat:
        search_cat = st.selectbox("Category", CFG["ZI_CATEGORY"], index=CFG["ZI_CATEGORY"].index(BLANK_STR_VALUE), key=f"{KEY_PREFIX}_search_cat")
    with c_set_id:
        search_set_id = st.selectbox("Set ID", SET_ID_SEARCH_SPEC, index=SET_ID_SEARCH_SPEC.index(BLANK_STR_VALUE), key=f"{KEY_PREFIX}_search_set_id")
    with c_layer:
        search_layer = st.selectbox("🔍HSK Layer", HSK_LAYERS, index=HSK_LAYERS.index(BLANK_STR_VALUE), key=f"{KEY_PREFIX}_search_layer")
    with c_active:
        active = st.selectbox("🔍Active?", BI_STATES, index=BI_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    where_clause = " 1=1 " 
    where_clause += " " if not active else f" and is_active = '{active}' "
    where_clause += " " if not search_layer else f" and layer = '{search_layer}' "
    where_clause += " " if not search_cat else f" and category = '{search_cat}' "

    if not search_set_id:
        where_clause += " "
    elif "<=" in search_set_id:
        search_set_id_new = search_set_id.replace("<=", "  ")
        where_clause += f" and set_id <= '{search_set_id_new}' "
    else:
        where_clause += f" and set_id = '{search_set_id}' "

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
                , ifnull(pinyin, '') as pinyin
                , ifnull(alias, '') as alias
                , ifnull(traditional, '') as traditional
                , ifnull(as_part, '') as as_part
                , ifnull(is_radical, '') as is_radical
                , ifnull(is_picto, '') as is_picto
                , ifnull(nstrokes, '') as nstrokes
                , ifnull(category, '') as category
                , ifnull(set_id, '') as set_id
                , ifnull(layer, '') as layer
                , ifnull(desc_cn, '') as desc_cn
                , ifnull(desc_en, '') as desc_en
                , ifnull(notes, '') as notes
                , u_id
                , ifnull(is_active, '')  as is_active
            from {TABLE_NAME}
            where {where_clause}
                and cast(u_id as real) > 0   -- exclude u_id=-1
            order by set_id, cast(u_id as real);
        """
        print(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, selection_mode="single")
    selected_rows = grid_resp['selected_rows']
    selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]

    # display form
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