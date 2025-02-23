with links as (
	SELECT 
		'L-R' as "link", t_zi_part.*
	FROM t_zi_part 
	WHERE 1=1
	AND TRIM(COALESCE(zi_left, '')) <> '' 
	AND TRIM(COALESCE(zi_right, '')) <> '' 
	AND TRIM(COALESCE(zi_up, '')) = '' 
	AND TRIM(COALESCE(zi_down, '')) = '' 
	AND TRIM(COALESCE(zi_mid, '')) = '' 
	AND TRIM(COALESCE(zi_left_up, '')) = '' 
	AND TRIM(COALESCE(zi_left_down, '')) = '' 
	AND TRIM(COALESCE(zi_right_up, '')) = '' 
	AND TRIM(COALESCE(zi_right_down, '')) = '' 
	AND TRIM(COALESCE(zi_mid_in, '')) = '' 
	AND TRIM(COALESCE(zi_mid_out, '')) = ''

UNION

	SELECT 
		'L-M' as "link", t_zi_part.*
	FROM t_zi_part 
	WHERE 1=1
	AND TRIM(COALESCE(zi_left, '')) <> '' 
	AND TRIM(COALESCE(zi_mid, '')) <> '' 
	AND TRIM(COALESCE(zi_up, '')) = '' 
	AND TRIM(COALESCE(zi_down, '')) = '' 
	AND TRIM(COALESCE(zi_right, '')) = '' 
	AND TRIM(COALESCE(zi_left_up, '')) = '' 
	AND TRIM(COALESCE(zi_left_down, '')) = '' 
	AND TRIM(COALESCE(zi_right_up, '')) = '' 
	AND TRIM(COALESCE(zi_right_down, '')) = '' 
	AND TRIM(COALESCE(zi_mid_in, '')) = '' 
	AND TRIM(COALESCE(zi_mid_out, '')) = ''

UNION

	SELECT 
		'M-R' as "link", t_zi_part.*
	FROM t_zi_part 
	WHERE 1=1
	AND TRIM(COALESCE(zi_mid, '')) <> '' 
	AND TRIM(COALESCE(zi_right, '')) <> '' 
	AND TRIM(COALESCE(zi_up, '')) = '' 
	AND TRIM(COALESCE(zi_down, '')) = '' 
	AND TRIM(COALESCE(zi_left, '')) = '' 
	AND TRIM(COALESCE(zi_left_up, '')) = '' 
	AND TRIM(COALESCE(zi_left_down, '')) = '' 
	AND TRIM(COALESCE(zi_right_up, '')) = '' 
	AND TRIM(COALESCE(zi_right_down, '')) = '' 
	AND TRIM(COALESCE(zi_mid_in, '')) = '' 
	AND TRIM(COALESCE(zi_mid_out, '')) = ''

UNION

	SELECT 
		'L-M-R' as "link", t_zi_part.*
	FROM t_zi_part 
	WHERE 1=1
	AND TRIM(COALESCE(zi_left, '')) <> '' 
	AND TRIM(COALESCE(zi_mid, '')) <> '' 
	AND TRIM(COALESCE(zi_right, '')) <> '' 
	AND TRIM(COALESCE(zi_up, '')) = '' 
	AND TRIM(COALESCE(zi_down, '')) = '' 
	AND TRIM(COALESCE(zi_left_up, '')) = '' 
	AND TRIM(COALESCE(zi_left_down, '')) = '' 
	AND TRIM(COALESCE(zi_right_up, '')) = '' 
	AND TRIM(COALESCE(zi_right_down, '')) = '' 
	AND TRIM(COALESCE(zi_mid_in, '')) = '' 
	AND TRIM(COALESCE(zi_mid_out, '')) = ''
	
)
-- select * from links;
select link, count(*) from links group by link order by link;




SELECT 'L-R' as link, COUNT(*) AS "count"
FROM t_zi_part
WHERE COALESCE(zi_left, '') <> ''  -- Left is NOT empty
  AND COALESCE(zi_right, '') <> '' -- Right is NOT empty
  AND COALESCE(zi_up, '') = ''     -- All other positions
  AND COALESCE(zi_down, '') = ''   -- ARE empty
  AND COALESCE(zi_mid, '') = ''
  AND COALESCE(zi_left_up, '') = ''
  AND COALESCE(zi_left_down, '') = ''
  AND COALESCE(zi_right_up, '') = ''
  AND COALESCE(zi_right_down, '') = ''
  AND COALESCE(zi_mid_in, '') = ''
  AND COALESCE(zi_mid_out, '') = '';


select e.category,count(p.zi) from t_zi_part p join t_ele_zi e on p.zi_mid = e.zi
group by e.category order by count(p.zi) desc;

select zi,n_frequency,category, is_radical,n_strokes 
 from t_ele_zi where n_frequency > 20 and category !='radical' order by category, n_frequency desc;

select e.category,sum(e.n_frequency) from t_ele_zi e
group by e.category order by e.category;


select * FROM t_ele_zi;

select count(*) FROM t_ele_zi where is_active='Y' and cast(id_kangxi as int) > 0;
--245
select count(*) FROM t_ele_zi where is_active='Y' and cast(id_kangxi as int) <= 0;
--177

update t_ele_zi set id_kangxi = 149 where zi = '讠';

SELECT 
    n_strokes,
    GROUP_CONCAT(zi, '') as concatenated_characters
FROM t_ele_zi where is_active='Y'
GROUP BY n_strokes
ORDER BY n_strokes, zi;

select * from t_ele_zi order by n_strokes, category, zi;

select count(*) from t_zi_part where is_active='Y'
and (zi_left_up is not null or  zi_left is not null or  zi_left_down is not null or  zi_up is not null or  zi_mid is not null or  zi_down is not null or  zi_right_up is not null or  zi_right is not null or  zi_right_down is not null or  zi_mid_in is not null or  zi_mid_out is not null)
;
--6197

select count(*) from t_zi where layer not like 'HSK_z%';
--3918

update t_ele_zi set id_kangxi = -1 where id_kangxi = 0;
--

--drop table t_elemental_zi;

with comm_zi as (
	select * from t_ele_zi where n_frequency > 20
)
select zi, n_frequency, category from comm_zi order by category, n_frequency desc, zi;

select z.category, z.* from t_ele_zi z where z.is_zi = 0 and category||'' != ''  order by category;

select zi,variant  from t_ele_zi order by cast(n_frequency as int) desc;
alter table t_ele_zi add column notes text;

alter table t_ele_zi add column u_id text;
alter table t_ele_zi add column is_active text default 'Y';
alter table t_ele_zi add column is_radical text;

update t_ele_zi set is_radical = 'Y' where is_zi = 0;
update t_ele_zi set is_radical = '' where is_zi = 1;

select * from t_part;
update t_ele_zi set u_id = (select u_id from t_part where zi = t_ele_zi.zi);



with zi_part as (
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
	join t_elemental_zi p 
		on zp.part = p.zi
	where zp.part is not null and trim(zp.part) !='' 
)
, part_freq as (
	select part,count(zi) as zi_freq from zi_part_2 
	group by part 
	-- having count(zi) > 10
	--order by count(zi) desc, part    
)
select * from part_freq order by zi_freq desc,part 
where part in (
select zi from t_elemental_zi
--'日', '乙', '口'
);


            update t_elemental_zi 
            set n_frequency = '11'
                where zi='乙' and n_frequency is null 
            ;

			select * from t_elemental_zi where zi='乙';

--drop table t_elemental_zi;

select zi, freq from t_elemental_zi order by freq desc limit 30;

with hot1 as (
	select 
		  case when zi_left_up = '日' then 1 else 0 end as n_left_up
		, case when zi_left = '日' then 1 else 0 end as n_left
		, case when zi_left_down = '日' then 1 else 0 end as n_left_down
		, case when zi_up = '日' then 1 else 0 end as n_up
		, case when zi_mid = '日' then 1 else 0 end as n_mid
		, case when zi_down = '日' then 1 else 0 end as n_down
		, case when zi_right_up = '日' then 1 else 0 end as n_right_up
		, case when zi_right = '日' then 1 else 0 end as n_right
		, case when zi_right_down = '日' then 1 else 0 end as n_right_down
		, case when zi_mid_in = '日' then 1 else 0 end as n_mid_in
		, case when zi_mid_out = '日' then 1 else 0 end as n_mid_out
	from t_zi_part 
)
, sum1 as (
	select 
		sum(n_left_up) as n1, sum(n_left) as n2, sum(n_left_down) as n3,
		sum(n_up) as n4, sum(n_mid) as n5, sum(n_down) as n6,
		sum(n_right_up) as n7, sum(n_right) as n8, sum(n_right_down) as n9,
		sum(n_mid_in) as n10, sum(n_mid_out) as n11
	from hot1
)
select '日' as zi, (n1+n2+n3+n4+n5+n6+n7+n8+n9+n10+n11) as freq
from sum1
;

