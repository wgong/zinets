- 2025-02-22

 backup `zi.sqlite` as `zi-20250222.sqlite`

```sql
alter table t_ele_zi add column is_neted CHAR(1) CHECK (is_neted IS NULL OR is_neted = 'Y');


create table t_ele_zi_bkup1 as select * from t_ele_zi;

drop table t_ele_zi;

create table t_ele_zi as 
select 
zi, is_zi, id_kangxi, meaning, pinyin, n_strokes, term, examples, variant, n_frequency, category, sub_category, notes, u_id, is_active, is_radical, phono, ts
from t_ele_zi_bkup1;

alter table t_ele_zi add column is_neted CHAR(1) CHECK (is_neted IS NULL OR is_neted in ('', 'Y'));
```