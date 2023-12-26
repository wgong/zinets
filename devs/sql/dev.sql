-- migrate data from w_part to t_part
insert into t_part (
zi
, u_id
, traditional
, pinyin
, strokes
, meaning
, example
, is_active
) select 
radical
, cast(id as text)
, traditional
, pinyin
, cast(strokes as text)
, meaning
, example
, case when is_active=1 then 'Y' else NULL end
from w_part 
--limit 5
;


-- migrate data from w_zi to t_zi
insert into t_zi (
zi
, u_id
, unicode
, pinyin
, nstrokes
, alias
, traditional
, as_part
, is_radical
, layer
, desc_cn
, zi_en
, desc_en
, ts
, sort_val
, is_active
) select 
zi
, id
, NULL 
, pinyin
, NULL 
, NULL 
, alias 
, case when as_part=1 then 'Y' else NULL end 
, case when is_radical=1 then 'Y' else NULL end
, layer
, desc_cn 
, zi_en 
, desc_en 
, NULL 
, sort_val 
, case when is_active=1 then 'Y' else NULL end
from w_zi limit 5;


-- migrate data from w_zi_part to t_zi_part
insert into t_zi_part
(
zi
, u_id
, zi_left_up
, zi_left
, zi_left_down
, zi_up
, zi_mid
, zi_down
, zi_right_up
, zi_right
, zi_right_down
, zi_mid_out
, zi_mid_in
, ts
, desc_cn
, is_active
) select
zi
, id
, zi_left_up
, zi_left
, zi_left_down
, zi_up
, zi_mid
, zi_down
, zi_right_up
, zi_right
, zi_right_down
, zi_mid_out
, zi_mid_in
, ts 
, shuowen_desc
, case when is_active=1 then 'Y' else NULL end
from w_zi_part;


-- cleanup TABLES
ALTER TABLE t_part RENAME TO w_part;
ALTER TABLE t_zi RENAME TO w_zi;
ALTER TABLE t_zi_part RENAME TO w_zi_part;

-- temp
ALTER TABLE t_cedict_all RENAME TO w_cedict_all;
ALTER TABLE t_cedict_dedup RENAME TO w_cedict_dedup;
ALTER TABLE t_radical_1 RENAME TO w_radical_1;
ALTER TABLE t_radical_2 RENAME TO w_radical_2;
ALTER TABLE t_zi_cedict RENAME TO w_zi_cedict;
ALTER TABLE t_zi_hsk RENAME TO w_zi_hsk;
ALTER TABLE t_zi_shuowen_composed RENAME TO w_zi_shuowen_composed;
ALTER TABLE t_zi_shuowen_picto RENAME TO w_zi_shuowen_picto;

-- empty
drop table t_zi_word;
drop table t_zi_text;
drop table t_zi_shufa;
drop table t_zi_media;
drop table t_user;


drop table if exists t_part;
create table if not exists t_part
(
        id int  NOT NULL,
        id_radical int,
        radical text NOT NULL,
        traditional text,
        pinyin text,
        strokes int,
        meaning text,
        example text,
        is_active int default 0
);

select zi from t_zi where as_part=1;
select zi from t_part;

delete from t_part where id in (91,92);

select zi from t_zi where as_part=1
except
select radical as zi from t_part
;

select radical as zi from t_part where radical != ''
except
select zi from t_zi 
--where as_part=1
;

select zi,id,sort_val,layer 
from t_zi where as_part=1 order by sort_val;

select * from t_zi where (zi||desc||pinyin||alias||zi_en) like '%eight%'
select * from t_zi where zi || alias || pinyin || desc || zi_en || desc_en like '%eight%'

select * from t_zi where (zi || alias || pinyin || desc_cn || zi_en || desc_en) like '%kun%';

select * from t_zi where zi like '%kun%' or  pinyin like '%kun%';
select * from t_zi where (zi || pinyin) like '%kun%';

select * from t_zi 
where (zi||alias||pinyin||zi_en) like '%kun%'
or desc_cn like '%kun%'
or desc_en like '%kun%';


alter table t_zi add column sort_val REAL;
update t_zi set sort_val=cast(sort_id as real);

update t_zi set as_part=1 where is_radical=1;

alter table t_zi add column as_part int;
alter table t_zi add column nid int;
update t_zi set nid = cast(id as int);

ALTER TABLE t_zi RENAME COLUMN is_traditional TO has_traditional;
ALTER TABLE t_zi RENAME COLUMN desc TO desc_cn;
select * from t_zi order by cast(id as int);

ALTER TABLE t_zi_part RENAME COLUMN zi_mid_front TO zi_mid_out;
ALTER TABLE t_zi_part RENAME COLUMN zi_mid_back TO zi_mid_in;

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