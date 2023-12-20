"""
Note:

- st.data_editor() does not yet support row-selection, will use aggrid for now
    - https://discuss.streamlit.io/t/experimental-data-editor-how-to-retrieve-selection/40518
"""

from utils import *

st.set_page_config(layout="wide")
st.subheader("📝 Zi - Manager")

def main():
    TABLE_NAME = CFG["TABLE_ZI"]
    search_term = st.text_input("🔍Search:", key="zi_search_update").strip()
    if search_term:
        where_clause = f"""
            (zi||desc||pinyin||alias||zi_en) like '%{search_term}%'
        """
    else:
        where_clause = " 1=1 "

    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                *
            from {TABLE_NAME}
            where {where_clause}
            order by sort_id;
        """
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, selection_mode="single")
    selected_rows = grid_resp['selected_rows']

    # display form
    selected_row = selected_rows[0] if len(selected_rows) else None
    ui_layout_form(selected_row, TABLE_NAME)

if __name__ == '__main__':
    main()