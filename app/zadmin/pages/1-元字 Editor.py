"""


"""

from utils import *

st.set_page_config(layout="wide")
st.subheader("⚛️ 元字编辑 Editor 📝")

TABLE_NAME = CFG["TABLE_ELEZI"]
KEY_PREFIX = f"col_{TABLE_NAME}"

SORT_COLS = ['', 'category',
    'is_radical',
    'is_neted',
    'meaning',
    'n_frequency',
    'n_strokes',
    'phono',
    'pinyin',
    'u_id',
    'zi']

def main():
    # fix detail form not refresh correctly when selection changes
    if "previous_selected_row" not in st.session_state:
        st.session_state.previous_selected_row = None

    c1, c2, c3, c4 = st.columns([1,6,2,1])
    with c1:
        search_term = st.text_input("🔍Search:", key=f"{KEY_PREFIX}_search_term").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause  (e.g.    cast(u_id as int) > 0,  zi = '佥'    ):", key=f"{KEY_PREFIX}_search_others").strip()
    with c3:
        order_by = st.selectbox("Sort By", SORT_COLS, index=SORT_COLS.index(""), key=f"{KEY_PREFIX}_order_by")
    with c4:
        active = st.selectbox("🔍Active?", BI_STATES, index=BI_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    where_clause = " 1=1 " 
    where_clause += " " if not active else f" and is_active = '{active}' "

    if search_term:
        where_clause += f""" and (
            zi like '%{search_term}%'
            or variant like '%{search_term}%'
            or pinyin like '%{search_term}%'
            or meaning like '%{search_term}%'
            or category like '%{search_term}%'
            or sub_category like '%{search_term}%'       
            or examples like '%{search_term}%'
        )
        """
    if search_others:
        where_clause += f""" 
            and (
                {search_others}
        ) """

    order_clause = ""
    if order_by:
        order_clause = f"""
            order by {order_by} desc
        """ 

    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                zi
                , pinyin
                , phono
                , n_strokes
                , n_frequency
                , meaning
                , category
                , sub_category
                , examples
                , traditional
                , variant
                , notes
                , is_neted
                , is_radical
                , id_kangxi
                , u_id
                , is_active
            from {TABLE_NAME}
            where {where_clause}
            {order_clause}
            ;
        """
        # st.write(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn).fillna("")

    grid_resp = ui_display_df_grid(df, selection_mode="single")
    selected_rows = grid_resp['selected_rows']


    # streamlit-aggrid==0.3.3
    # selected_row = selected_rows[0] if len(selected_rows) else None
    # streamlit-aggrid==1.0.5
    selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]
    if selected_row != st.session_state.previous_selected_row:
        st.session_state.previous_selected_row = selected_row
        st.rerun()

    # print(selected_row)

    # display form
    # st.write(selected_row)
    ui_layout_form(selected_row, TABLE_NAME, form_name=TABLE_NAME)

    n_freq_qi = 24
    f1,f2,_ = st.columns([3,3,6])
    with f1:
        st.markdown("#### 元字频率", unsafe_allow_html=True)
    with f2:
        min_count = st.number_input("频率大于", value=(n_freq_qi-1), min_value=0, max_value=200, step=1, key="part_freq_min")
    
    # sql_stmt = f"""

    # -- unique parts
    # with parts as (  
    #     select zi from {TABLE_NAME} where is_active = 'Y'
    # )
    # -- zi vs part
    # , zi_part as (
    #     select zi_left_up as part, zi from t_zi_part 
    #     union all
    #     select zi_left as part, zi from t_zi_part 
    #     union all
    #     select zi_left_down as part, zi from t_zi_part 
    #     union all
    #     select zi_up as part, zi from t_zi_part 
    #     union all
    #     select zi_mid as part, zi from t_zi_part 
    #     union all
    #     select zi_down as part, zi from t_zi_part 
    #     union all
    #     select zi_right_up as part, zi from t_zi_part 
    #     union all
    #     select zi_right as part, zi from t_zi_part 
    #     union all
    #     select zi_right_down as part, zi from t_zi_part 
    #     union all
    #     select zi_mid_in as part, zi from t_zi_part 
    #     union all
    #     select zi_mid_out as part, zi from t_zi_part 
    # )
    # -- unique zi,part
    # , zi_part_2 as (
    #     select distinct zp.zi, zp.part 
    #     from zi_part zp 
    #     join parts p 
    #         on zp.part = p.zi
    #     where zp.part is not null and trim(zp.part) !='' 
    # )
    # -- count part frequency
    # , part_freq as (
    #     select part,count(zi) as zi_freq from zi_part_2 
    #     group by part -- having count(zi) > 10
    #     --order by count(zi) desc, part    
    # ), part_freq_2 as (
    #     select 
    #         f.part, f.zi_freq, p.category, p.sub_category, '0' as tag
    #     from part_freq f 
    #     join t_part p
    #     on f.part = p.zi
    #     where trim(p.category || '') != ''
    #     union all
    #     select 
    #         f.part, f.zi_freq, p.category, p.sub_category, '1' as tag
    #     from part_freq f 
    #     join t_part p
    #     on f.part = p.zi
    #     where trim(p.category || '') = ''
    # )
    # select 
    #     pf.part            as "元字"
    #     , p.meaning
    #     , p.notes as sample
    #     , pf.zi_freq       as "频率"
    #     , pf.category      as "类别"
    #     , pf.sub_category  as "子类别"
    #     , pf.tag
    # from part_freq_2 pf
    # join t_part p
    # on pf.part = p.zi
    # where pf.zi_freq > {min_count}
    # order by pf.category,pf.sub_category,pf.zi_freq desc, pf.part;
    # """

    # switch from t_part to t_ele_zi
    sql_stmt = f"""

        -- unique parts
        with parts as (  
            select zi from {TABLE_NAME} where is_active = 'Y'
        )
        -- zi vs part
        , zi_part as (
            select zi_left_up as part, zi from t_zi_part 
            union all
            select zi_left as part, zi from t_zi_part 
            union all
            select zi_left_down as part, zi from t_zi_part 
            union all
            select zi_up as part, zi from t_zi_part 
            union all
            select zi_mid as part, zi from t_zi_part 
            union all
            select zi_down as part, zi from t_zi_part 
            union all
            select zi_right_up as part, zi from t_zi_part 
            union all
            select zi_right as part, zi from t_zi_part 
            union all
            select zi_right_down as part, zi from t_zi_part 
            union all
            select zi_mid_in as part, zi from t_zi_part 
            union all
            select zi_mid_out as part, zi from t_zi_part 
        )
        -- unique zi,part
        , zi_part_2 as (
            select distinct zp.zi, zp.part 
            from zi_part zp 
            join parts p 
                on zp.part = p.zi
            where zp.part is not null and trim(zp.part) !='' 
        )
        -- count part frequency
        , part_freq as (
            select part,count(zi) as zi_freq from zi_part_2 
            group by part -- having count(zi) > 10
            --order by count(zi) desc, part    
        ), part_freq_2 as (
            select 
                f.part, f.zi_freq, p.category, p.sub_category, p.is_neted as tag
            from part_freq f 
            join {TABLE_NAME} p
            on f.part = p.zi
            where trim(p.category || '') != ''
            union all
            select 
                f.part, f.zi_freq, p.category, p.sub_category, p.is_neted as tag
            from part_freq f 
            join {TABLE_NAME} p
            on f.part = p.zi
            where trim(p.category || '') = ''
        )
        select 
            pf.part            as "元字"
            , p.meaning
            , p.pinyin
            , p.phono
            , p.n_strokes as strokes
            , p.variant as alias
            , p.n_frequency as n_freq
            , pf.zi_freq       as "频率"
            , pf.category      as "类别"
            , pf.sub_category  as "子类别"
            , p.examples as sample
            , pf.tag
            , p.is_zi
            , p.notes
            , p.term
            , p.id_kangxi
        from part_freq_2 pf
        join {TABLE_NAME} p
        on pf.part = p.zi
        where pf.zi_freq > {min_count}
        order by pf.category,pf.sub_category,pf.zi_freq desc, pf.part;
    """

    with DBConn() as _conn:
        df_part_freq = pd.read_sql(sql_stmt, _conn).fillna("")
        st.dataframe(df_part_freq)


    # optional download
    with st.expander("Download CSV", expanded=False):
        _, c1, _ = st.columns([5,2,5])
        with c1:
            st.download_button(
                label="Submit",
                data=df_to_csv(df_part_freq, index=False),
                file_name=f"{TABLE_NAME}-{get_ts_now()}.csv",
                mime='text/csv',
            )      

if __name__ == '__main__':
    main()