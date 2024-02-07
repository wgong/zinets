delete from t_zipart;

select zi,count(*) from t_zi_part 
where is_active='Y' and cast(u_id as int) > 0
group by zi having count(*) > 1;

drop table zi_part;
create table zi_part(
zi TEXT,
part text );

insert into zi_part (zi,part)
select zi,part from (
select zi, zi_left_up as part from t_zi_part where zi_left_up is not null
     union all 
    select zi, zi_left as part from t_zi_part where  zi_left is not null
     union all 
    select zi, zi_left_down as part from t_zi_part where  zi_left_down is not null
     union all 
    select zi, zi_up as part from t_zi_part where  zi_up is not null
     union all 
    select zi, zi_mid as part from t_zi_part where   zi_mid is not null
     union all 
    select zi, zi_down as part from t_zi_part where  zi_down is not null
     union all 
    select zi, zi_right_up as part from t_zi_part where  zi_right_up is not null
     union all 
    select zi, zi_right as part from t_zi_part where  zi_right is not null
     union all 
    select zi, zi_right_down as part from t_zi_part where  zi_right_down is not null
     union all 
    select zi, zi_mid_out as part from t_zi_part where  zi_mid_out is not null
     union all 
    select zi, zi_mid_in as part from t_zi_part where  zi_mid_in is not null
) 
where zi is not null and part is not null and zi != '' and part != '' 
order by zi,part;

create index i_zi_part on zi_part(zi);

CREATE TABLE t_zipart(
  zi TEXT primary key,
  u_id TEXT,
  zi_left_up TEXT REFERENCES  t_zipart,
  zi_left TEXT REFERENCES  t_zipart,
  zi_left_down TEXT REFERENCES  t_zipart,
  zi_up TEXT REFERENCES  t_zipart,
  zi_mid TEXT REFERENCES  t_zipart,
  zi_down TEXT REFERENCES  t_zipart,
  zi_right_up TEXT REFERENCES  t_zipart,
  zi_right TEXT REFERENCES  t_zipart,
  zi_right_down TEXT REFERENCES  t_zipart,
  zi_mid_out TEXT REFERENCES  t_zipart,
  zi_mid_in TEXT REFERENCES  t_zipart,
  ts TEXT,
  desc_cn TEXT,
  is_active TEXT,
  id_shuowen TEXT,
  hsk_note TEXT,
  desc_en TEXT
);

insert into t_zipart select * from t_zi_part;

select * from t_zipart limit 10;


select zi, zi_left_up as part from t_zi_part where zi='藻' and  zi_left_up is not null
 union all 
select zi, zi_left as part from t_zi_part where zi='藻' and  zi_left is not null
 union all 
select zi, zi_left_down as part from t_zi_part where zi='藻' and  zi_left_down is not null
 union all 
select zi, zi_up as part from t_zi_part where zi='藻' and  zi_up is not null
 union all 
select zi, zi_mid as part from t_zi_part where zi='藻' and  zi_mid is not null
 union all 
select zi, zi_down as part from t_zi_part where zi='藻' and  zi_down is not null
 union all 
select zi, zi_right_up as part from t_zi_part where zi='藻' and  zi_right_up is not null
 union all 
select zi, zi_right as part from t_zi_part where zi='藻' and  zi_right is not null
 union all 
select zi, zi_right_down as part from t_zi_part where zi='藻' and  zi_right_down is not null
 union all 
select zi, zi_mid_out as part from t_zi_part where zi='藻' and  zi_mid_out is not null
 union all 
select zi, zi_mid_in as part from t_zi_part where zi='藻' and  zi_mid_in is not null;


select * from t_zi_part where zi='藻';
select * from t_zi_part where zi='艹'; --0
select * from t_zi_part where zi='喿'; --2
select * from t_zi_part where zi='品'; --3
select * from t_zi_part where zi='木'; --0





WITH RECURSIVE
  org_chart(name,level) AS (
    VALUES('Bob',0)
    UNION ALL
    SELECT org.name, org_chart.level+1
      FROM org JOIN org_chart ON org.boss=org_chart.name
     ORDER BY 2 desc
  )
SELECT substr('..............................',1,level*3) || name as tree, level
FROM org_chart;