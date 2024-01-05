select c.zi, c.caizi, p.*
from t_zi_part p join w_caizi c on p.zi = c.zi;

select c.zi, c.caizi, p.*
from t_zi_part p join w_caizi c on p.zi = c.zi
where 1=1
and p.zi_left is null and p.zi_left_down is null and p.zi_left_up is null 
and p.zi_right is null and p.zi_right_down is null and p.zi_right_up is null 
and p.zi_up is null and p.zi_mid is null and p.zi_down is null and p.zi_mid_in is null and p.zi_mid_out is null
;
-- 2449 are not yet decomposed


 select max(u_id) from t_note;
 
 select 
	case 
		when max(u_id) is NULL then '10' 
		else cast(max(cast(u_id as int))+1 as text) 
	end as id
 from t_note;
 
 update t_zi_part set zi_left_up = 'X' where zi_left_up = 'x'; 
 update t_zi_part set zi_up = 'X' where zi_up = 'x'; 
 update t_zi_part set zi_right_up = 'X' where zi_right_up = 'x'; 
 update t_zi_part set zi_left = 'X' where zi_left = 'x'; 
 update t_zi_part set zi_mid = 'X' where zi_mid = 'x'; 
 update t_zi_part set zi_right = 'X' where zi_right = 'x'; 
 update t_zi_part set zi_left_down = 'X' where zi_left_down = 'x'; 
 update t_zi_part set zi_down = 'X' where zi_down = 'x'; 
 update t_zi_part set zi_right_down = 'X' where zi_right_down = 'x'; 
 update t_zi_part set zi_mid_in = 'X' where zi_mid_in = 'x'; 
 update t_zi_part set zi_mid_out = 'X' where zi_mid_out = 'x'; 


select zi from t_zi where (layer like 'HSK_1%' or layer like 'HSK_2%') order by zi;

select zi from t_zi_part where is_active = 'Y' and u_id is not null
order by zi;  --3636

select zi from t_zi_part where hsk_note='in HSK'
order by zi;  --1236

select zi from t_zi_part where hsk_note='from HSK'
order by zi;  --2504

select u_id,count(*) from t_zi_part where u_id is not null 
group by u_id having count(*) > 1;


update t_zi_part set hsk_note='in HSK' where is_active='Y' and u_id is not null
and zi in (
	select zi from t_zi where (layer like 'HSK_1%' or layer like 'HSK_2%')
)
;

alter table t_zi_part add column id_shuowen text;
alter table t_zi_part add column hsk_note text;
alter table t_zi_part add column desc_en text;
alter table t_part add column category text;

select * from t_part where zi is null;

update t_zi_part set id_shuowen = u_id;

-- why u_id mismatch
select z.u_id, z.zi, p.zi, p.u_id
from t_zi z join t_zi_part p
on z.u_id = p.u_id 
order by z.sort_val;

with zi as (
select 
	z.u_id as z_u_id,  
	z.zi as z_zi, 
	p.u_id as p_u_id, 
	p.zi as p_zi
from t_zi z join t_zi_part p
on z.zi = p.zi 
--order by z.sort_val
) 
select * from t_zi_part where zi not in (
	select p_zi from zi
);

update t_zi_part set is_active='', u_id = NULL;

update t_zi_part 
set u_id = (
	select u_id from t_zi where t_zi.zi = t_zi_part.zi
)
where zi in (select zi from t_zi);
update t_zi_part set is_active='Y' where u_id is not NULL;

select u_id,count(*) from t_zi group by u_id having count(*) > 1;

with dup as (
	select u_id,count(*) from t_zi_part 
	where u_id is not NULL 
	group by u_id having count(*) > 1
	order by cast(u_id as int)
) 
select p.* from t_zi_part p join dup on dup.u_id = p.u_id 
order by p.u_id;


select count(*) from t_zi;  --11516
select count(*) from t_zi_part; --8530


with uid as (
	select cast(max(cast(u_id as int))+1 as text) as id 
	from t_zi_part
)
insert into t_zi_part (zi,u_id,zi_up,zi_mid)
select 
'元', id, '一', '兀'
from uid;

select * from t_zi_part where u_id = '9830';
delete from t_zi_part where u_id = '9830';

select distinct layer from t_zi order by layer;



select * from t_zi where u_id = '498';  -- 龚龔
select * from t_zi_part where zi in ('龚','龔');  -- 芣

select * from t_zi_part where zi like '%龔%';  -- 

select * from t_zi_part where u_id = '498';  -- 芣



select * from t_zi_part limit 2;
-- 元	2				一	兀
-- zi  u_id             zi_up  zi_mid

with uid as (
	select cast(max(cast(u_id as int))+1 as text) as id 
	from t_part
)
insert into t_part (zi,u_id,meaning,is_active)
select 
'一', id, 'one', 'Y'
from uid;

select * from t_part where u_id = '259';
delete from t_part where u_id = '259';

select max(cast(u_id as int)) from t_part;

select * from t_part limit 5;


select * from t_zi_part where zi_left = '示' and zi_right is not null and zi_mid is null;
update t_zi_part set zi_left='礻', zi_mid = zi_right, zi_right=NULL 
where zi_left = '示' and zi_right is not null and zi_mid is null;

select * from t_part order by cast(strokes as int), u_id;


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

-- DDL
-- create TABLE
create table if not exists t_note
(
    title text NOT NULL,
    u_id text,          -- number in string
    note_type text,     -- REF/JOURNAL
    note text,
    link_url text,
    tags text,
    ts text,
    is_active text default 'Y'
);

create table if not exists w_caizi
(
    zi text NOT NULL,
	caizi text,
    tags text,
    is_active text default 'Y'
);

-- alter table 

