select * from sh_kangxi_radical_214 where id_kangxi = 18;

-- delete from sh_elemental_zi_v2 where zi is null;

UPDATE sh_kangxi_radical_214_wikipedia
SET 
    radical_forms = REPLACE(REPLACE(radical_forms, CHAR(13)||CHAR(10), ' '), CHAR(10), ' '),
    colloquial__term = REPLACE(REPLACE(colloquial__term, CHAR(13)||CHAR(10), ' '), CHAR(10), ' ')
WHERE 1=1 
-- and id_kangxi = 18
and (radical_forms  LIKE '%' || CHAR(10) || '%'
   OR radical_forms  LIKE '%' || CHAR(13) || CHAR(10) || '%'
   OR colloquial__term  LIKE '%' || CHAR(10) || '%'
   OR colloquial__term  LIKE '%' || CHAR(13) || CHAR(10) || '%');

UPDATE sh_kangxi_radical_214
SET 
    zi__radical = REPLACE(REPLACE(zi__radical, CHAR(13)||CHAR(10), ' '), CHAR(10), ' '),
    term = REPLACE(REPLACE(term, CHAR(13)||CHAR(10), ' '), CHAR(10), ' ')
WHERE 1=1 
-- and id_kangxi = 18
and (zi__radical  LIKE '%' || CHAR(10) || '%'
   OR zi__radical  LIKE '%' || CHAR(13) || CHAR(10) || '%'
   OR term  LIKE '%' || CHAR(10) || '%'
   OR term  LIKE '%' || CHAR(13) || CHAR(10) || '%');