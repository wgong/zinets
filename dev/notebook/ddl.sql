
    select  tzp.zi, tzp.zi_left_up as part from t_zi_part tzp join zi_part zp on zp.part = tzp.zi where tzp.zi_left_up is not null

    
sqls = []
for c in [c for c in df.columns if c.startswith("zi_")]:
    sql = f"select  tzp.zi, tzp.{c} as part from t_zi_part tzp join zi_part zp on zp.part = tzp.zi where tzp.{c} is not null"
    sqls.append(sql)
sql_stmt = "\n union all \n".join(sqls)
print(sql_stmt)


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
)