"""
store textbook pages in t_textbook_page table
annotage useful pages for One-Zi-One-Story video series
"""

from utils import *
from PIL import Image

st.set_page_config(layout="wide")
st.subheader("Textbook Pages 📚")

TABLE_NAME = CFG["TABLE_TEXTBOOK_PAGE"]
KEY_PREFIX = f"col_{TABLE_NAME}"
TEXTBOOK_PAGE_ROOT = CFG["TEXTBOOK_PAGE_ROOT"]

if "record_index" not in st.session_state:
    st.session_state["record_index"] = 0

if "NUM_IMAGES" not in st.session_state:
    st.session_state["NUM_IMAGES"] = 0

if "selected_row" not in st.session_state:
    st.session_state["selected_row"] = {}

   
if "df" not in st.session_state:
    st.session_state["df"] = None

def set_selected_row():
    # set selected_row
    df = st.session_state.get("df")
    if df is not None and not df.empty:
        curr_row = st.session_state["record_index"]
        selected_row = df.iloc[curr_row].to_dict()
        st.session_state["selected_row"] = selected_row

def next_record():
    # print(f"curr_row: {st.session_state.record_index} ")
    curr_row = st.session_state["record_index"]
    curr_row += 1
    st.session_state["record_index"] = curr_row if curr_row <= st.session_state["NUM_IMAGES"] else 0
    # print(f"curr_row: {st.session_state.record_index} ")
    set_selected_row()

def prev_record():
    # print(f"curr_row: {st.session_state.record_index} ")
    curr_row = st.session_state["record_index"]
    curr_row -= 1
    st.session_state["record_index"] = curr_row if curr_row >= 0 else st.session_state["NUM_IMAGES"]
    # print(f"curr_row: {st.session_state.record_index} ")
    set_selected_row()

def parse_subject(filename):
    for subject in CFG["SUBJECT_CODE"]:
        if not subject: continue
        if filename.startswith(subject):
            return subject
    return ""

def get_tags():
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                distinct tags
            from {TABLE_NAME}
            ;
        """
        # print(sql_stmt)
        return pd.read_sql(sql_stmt, _conn)["tags"].to_list()

def main():

    # get distinct tags
    tags = get_tags()

    c1, c2 = st.columns([3,6])
    with c1:
        search_terms = st.text_input("🔍Search:", key=f"{KEY_PREFIX}_search_term").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause:", key=f"{KEY_PREFIX}_search_others").strip()
    search_term_list = [i.strip() for i in search_terms.split() if i.strip()]
    where_clause = " 1=1 " 
    for search_term in search_term_list:
        where_clause += f""" and (
            page_path like '%{search_term}%'
            or root_path like '%{search_term}%'
            or subject like '%{search_term}%'
            or note like '%{search_term}%'
            or note_enu like '%{search_term}%'
            or tags like '%{search_term}%'       
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
                page_path
                , ifnull(note, '')  as note 
                , ifnull(note_enu, '')  as note_enu 
                , tags
                , ifnull(subject, '')  as subject 
                , root_path
                , u_id
               -- , ifnull(is_active, '')  as is_active
            from {TABLE_NAME}
            where {where_clause}
            order by page_path
            ;
        """
        # # print(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)
        st.session_state["df"] = df
        if df is not None and not df.empty:
            st.session_state["NUM_IMAGES"] = df.shape[0]
    

    # st.dataframe(df)
    grid_resp = ui_display_df_grid(df, 
                                   selection_mode="single")
    selected_rows = grid_resp['selected_rows']

    # handle manual selection
    if selected_rows is not None and selected_rows.empty:   
        # debug
        # st.write(selected_rows)
        # st.write(selected_rows.index[0])
        # st.write(selected_rows.to_dict(orient='records'))
        selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]
        record_index = selected_rows.index[0]
        if record_index != st.session_state.get("record_index"):
            # reset session_state
            st.session_state["record_index"] = int(record_index)
            st.session_state["selected_row"] = selected_row
    else:
        selected_row = st.session_state.get("selected_row")

    # st.write(selected_row)
    c_left, c_right = st.columns([3,3])
    with c_right:
        # display image
        _, c_prev, c_next, c_hint = st.columns([4,2,2,4])
        with c_prev:
            if st.session_state.record_index > 0:
                st.button("< Prev", on_click=prev_record)
            else:
                st.write("") 

        with c_next:
            if st.session_state.record_index < len(df.index)-1:
                st.button("Next >", on_click=next_record)
            else:
                st.write("") 
        with c_hint:
            st.markdown(f"""
                <span style="font-size:13px;color:blue;">
                    unselect row when using buttons
                </span>
            """, unsafe_allow_html=True)

        if selected_row:
            image_file = selected_row["page_path"]
            root_path = selected_row["root_path"]
            subject = selected_row["subject"]
            img_path = os.path.join(root_path, image_file)
            orig_img = Image.open(img_path)
            if subject in ["Chinese","Math","Science"]:
                img = orig_img
            else:
                c_left_180, c_left_90, c_right_90, c_right_180 = st.columns(4)
                with c_right_90:
                    b_n_90 = st.button("R-90")
                with c_right_180:
                    b_n_180 = st.button("R-180")
                with c_left_90:
                    b_p_90 = st.button("L-90")
                with c_left_180:
                    b_p_180 = st.button("L-180")

                if b_n_90:
                    img = orig_img.rotate(-90)
                elif b_n_180:
                    img = orig_img.rotate(-180)
                elif b_p_90:
                    img = orig_img.rotate(90)
                elif b_p_180:
                    img = orig_img.rotate(180)
                else:
                    img = orig_img

            st.image(img, caption=image_file, use_column_width=True)
    with c_left:
        # display form
        ui_layout_form(selected_row, TABLE_NAME)

    st.image("images/ocean-surface.png", width=1000)

    with st.expander("Download CSV or view tags", expanded=False):
        c_1, c_2 = st.columns([3,3])
        with c_1:
            st.markdown(f"""
                ##### Download CSV
            """, unsafe_allow_html=True)
            st.download_button(
                label="Submit",
                data=df_to_csv(df, index=False),
                file_name=f"{TABLE_NAME}-{get_ts_now()}.csv",
                mime='text/csv',
            )
        with c_2:
            tags_new = []
            for t in tags:
                if t is None or not t: continue
                if "," in t:
                    tags_new.extend([i.strip().upper() for i in t.split(",") if i.strip()])
                else:
                    tags_new.append(t.strip().upper())
            tag_str = " , ".join(sorted(list(set(tags_new))))
            st.markdown(f"""
                ##### Tags
                {tag_str}
            """, unsafe_allow_html=True)

    with st.expander("Load Textbook Pages", expanded=False):
        c_path, c_mode = st.columns([10,2])
        with c_path:
            root_path = st.text_input("Root Path:", value=TEXTBOOK_PAGE_ROOT, key=f"{TABLE_NAME}-root-path")
            if "~" in root_path:
                root_path = os.path.expanduser(root_path)
        with c_mode:
            write_mode = st.selectbox("Write Mode:", options=CFG["PANDAS_WRITE_MODE"], index=CFG["PANDAS_WRITE_MODE"].index("append"), key=f"{TABLE_NAME}-write-mode")
        if st.button("Load"):
            # with st.spinner("Loading images to databse ...... "):
            # prepare dataframe
            data = []
            root_path = root_path.strip() if root_path.strip() else "."
            all_filenames = list_all_filenames(root_path)
            # st.write(all_filenames)
            ts = get_ts_now()
            for f in all_filenames:
                filename = remove_parent_path(f, parent_path=root_path)
                subject = parse_subject(filename)
                u_id = get_uuid()
                data.append([u_id, filename, root_path, subject, "", "", "", ts, "Y"])
            df = pd.DataFrame(data, columns=CFG["COLUMN_DEFS"][TABLE_NAME])
            with DBConn() as _conn:
                df.to_sql(TABLE_NAME, con=_conn, if_exists=write_mode, index=False)


    
if __name__ == '__main__':
    main()