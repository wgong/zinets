alter table t_zi add column as_part int;
alter table t_zi add column nid int;
update t_zi set nid = cast(id as int);

ALTER TABLE t_zi RENAME COLUMN is_traditional TO has_traditional;
ALTER TABLE t_zi RENAME COLUMN nid TO sort_id;
select * from t_zi order by cast(id as int);

select * from t_zi order by sort_id;
--layer, pinyin;

select distinct layer from t_zi order by layer;

update t_zi set layer = 'HSK_8' where layer is null;

select layer,count(*) from t_zi group by layer order by layer;

alter table t_zi add column sort_id int;
with ids as (
	SELECT id, ROW_NUMBER() OVER (order by layer, pinyin) as sort_id FROM t_zi
)
update t_zi set sort_id = (select sort_id from ids where ids.id = t_zi.id);

SELECT ROW_NUMBER() OVER (order by layer, pinyin) nid, * FROM t_zi  
order by layer, pinyin
;