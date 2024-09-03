"""
TO FIX: failed into new part

 with uid as (
    select
    case
        when max(u_id) is NULL then '10'
        else cast(max(cast(u_id as int))+1 as text)
    end as id
    from t_part
    where u_id not in ('-1')
)
insert into t_part (
    zi, pinyin, alias, is_radical, strokes, category, meaning, is_active, u_id
)
select '⺩', 'yù', '玉', 'Y', '4', 'radical', 'jade', 'Y', id
from uid;

"""

from utils import *

st.set_page_config(layout="wide")
st.subheader("🐒 部件编辑 Part Editor 📝")

TABLE_NAME = CFG["TABLE_PART"]
KEY_PREFIX = f"col_{TABLE_NAME}"

def main():
    c1, c2,  c4 = st.columns([1,8,1])
    with c1:
        search_term = st.text_input("🔍Search:", key=f"{KEY_PREFIX}_search_term").strip()
    with c2:
        search_others = st.text_input("🔍Free-form where-clause  (e.g.    cast(u_id as int) > 0,  zi = '佥'    ):", key=f"{KEY_PREFIX}_search_others").strip()
    with c4:
        active = st.selectbox("🔍Active?", BI_STATES, index=BI_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    where_clause = " 1=1 " 
    where_clause += " " if not active else f" and is_active = '{active}' "

    if search_term:
        where_clause += f""" and (
            zi like '%{search_term}%'
            or alias like '%{search_term}%'
            or traditional like '%{search_term}%'
            or pinyin like '%{search_term}%'
            or meaning like '%{search_term}%'
            or category like '%{search_term}%'       
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
            with parts as (
                select 
                    zi
                    , alias
                    , traditional
                    , pinyin
                    , is_radical
                    , category
                    , sub_category
                    , meaning
                    , notes
                    , case when strokes is null then '99'
                        when strokes='' then '99'
                        else strokes
                      end as strokes
                    , u_id
                    , zi_count
                    , ifnull(is_active, '')  as is_active
                from {TABLE_NAME}
                where {where_clause}
                    and cast(u_id as real) > 0   -- exclude u_id=-1
            )
            select * from parts
            order by cast(strokes as int), cast(u_id as real)
            ;
        """
        # st.write(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, selection_mode="single")
    selected_rows = grid_resp['selected_rows']
    selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]

    # st.write(selected_row)

    # streamlit-aggrid==0.3.3
    # selected_row = selected_rows[0] if len(selected_rows) else None
    # streamlit-aggrid==1.0.5
    selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]

    # display form
    ui_layout_form(selected_row, TABLE_NAME, form_name=TABLE_NAME)

    f1,f2,_ = st.columns([3,3,6])
    with f1:
        st.markdown("#### 部件频率", unsafe_allow_html=True)
    with f2:
        min_count = st.number_input("频率大于", value=20, min_value=0, max_value=300, step=20, key="part_freq_min")
    
    sql_stmt = f"""

    -- unique parts
    with parts as (  
        select zi from t_part where is_active = 'Y'
        union 
        select zi from t_zi where is_active = 'Y' and as_part='Y'
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
    --select * from zi_part_2 order by zi,part;
    -- count part frequency
    , part_freq as (
        select part,count(zi) as zi_freq from zi_part_2 
        group by part -- having count(zi) > 10
        --order by count(zi) desc, part    
    ), part_freq_2 as (
        select 
            f.part, f.zi_freq, p.category, p.sub_category, '0' as tag
        from part_freq f 
        join t_part p
        on f.part = p.zi
        where trim(p.category || '') != ''
        union all
        select 
            f.part, f.zi_freq, p.category, p.sub_category, '1' as tag
        from part_freq f 
        join t_part p
        on f.part = p.zi
        where trim(p.category || '') = ''
    )
    select 
        pf.part            as "部件"
        , p.meaning
        , p.notes as sample
        , pf.zi_freq       as "频率"
        , pf.category      as "类别"
        , pf.sub_category  as "子类别"
        , pf.tag
    from part_freq_2 pf
    join t_part p
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