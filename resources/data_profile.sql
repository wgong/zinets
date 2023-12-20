select max(length(traditional)) from t_mdbg_dict;
--20

select length(traditional), count(*) from t_mdbg_dict group by length(traditional) order by 1;
/*
1	13564
2	58893
3	23727
4	19218
5	3040
6	1301
7	858
8	305
9	365
10	112
11	121
12	24
13	27
14	6
15	24
16	1
17	2
19	2
*/

select * from t_mdbg_dict where length(traditional) >= 10 order by length(traditional) desc;

select * from t_mdbg_dict where length(traditional) = 1 order by pinyin -- simplified
;

select distinct simplified from t_mdbg_dict where length(traditional) = 1;

create table t_zi_hsk (zi text, url text, hsk_level text);

select count(*) from t_zi;

alter table t_zi add column layer text;

select count(*) from t_zi_cedict;
-- 13527

select rowid,* from t_zi_cedict order by pinyin;

select zi,count(*) from t_zi_cedict group by zi having count(*) > 1;

alter table t_zi_cedict add column id text;

update t_zi_cedict set id=rowid, pinyin=lower(pinyin);

-- export duplicates
with dup as (
	select zi,count(*) from t_zi_cedict group by zi having count(*) > 1
)
select * from t_zi_cedict where zi in (
	select zi from dup
)
order by zi,pinyin
;


--drop table t_radical_1;

select * from t_cedict_dedup limit 10;

select is_active, count(*) from t_cedict_dedup group by is_active;

select * from t_cedict_dedup where is_active=1;

update t_zi set is_zi = 1;

update t_zi_hsk set hsk_level = 'Common-01' where hsk_level = 'Common-1';
update t_zi_hsk set hsk_level = 'Common-02' where hsk_level = 'Common-2';
update t_zi_hsk set hsk_level = 'Common-03' where hsk_level = 'Common-3';
update t_zi_hsk set hsk_level = 'Common-04' where hsk_level = 'Common-4';
update t_zi_hsk set hsk_level = 'Common-05' where hsk_level = 'Common-5';
update t_zi_hsk set hsk_level = 'Common-06' where hsk_level = 'Common-6';
update t_zi_hsk set hsk_level = 'Common-07' where hsk_level = 'Common-7';
update t_zi_hsk set hsk_level = 'Common-08' where hsk_level = 'Common-8';
update t_zi_hsk set hsk_level = 'Common-09' where hsk_level = 'Common-9';

select * from t_zi_hsk where hsk_level like 'HSK%';

update t_zi_hsk set hsk_level = 'HSK_3' where hsk_level like 'HSK%';

update t_zi_hsk set hsk_level = 'HSK_1-'||hsk_level where hsk_level like 'Common-%';

select * from t_zi where is_active =1 and layer is not null order by layer,zi;

update t_zi_hsk set hsk_level = 'HSK_2-'||hsk_level where hsk_level like 'CommonLow-%';

alter table t_zi add column is_picto int;
alter table t_zi add column is_composed int;
alter table t_zi_part add column shuowen_desc text;

select * from t_zi where exists (select 1 from t_zi_shuowen_picto p where p.zi = t_zi.zi);  -- 175
update t_zi set is_picto=1 where exists (select 1 from t_zi_shuowen_picto p where p.zi = t_zi.zi);
select * from t_zi where is_picto = 1;

select * from t_zi where exists (select 1 from t_zi_shuowen_composed p where p.zi = t_zi.zi);  --3864
update t_zi set is_composed=1 where exists (select 1 from t_zi_shuowen_composed p where p.zi = t_zi.zi);
select * from t_zi where is_composed = 1;

select * from t_zi where is_picto=1 and is_composed=1;

select zi, p1, p2, id_json, explanation from t_zi_shuowen_composed;

insert into t_zi_part(zi, zi_left, zi_right, id, shuowen_desc) 
select zi, p1, p2, id_json, explanation from t_zi_shuowen_composed;

select * from t_zi_part;
select * from t_zi_part p 
where exists (
	select 1 from t_zi z where z.is_active = 1 and z.zi = p.zi 
);  --3657

update t_zi_part
set is_active=1 
where exists (
	select 1 from t_zi z where z.is_active = 1 and z.zi = t_zi_part.zi 
);

select * from t_zi_part where is_active=1;