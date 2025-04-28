-- store pinyin data for each zi and comp
CREATE TABLE if not exists t_zi_part_pinyin
(
    zi text NOT NULL,  -- non-unique
	comp text,
	position text,
	zi_pinyin text,
	zi_initial text,
	zi_final text,
	comp_pinyin text,
	comp_initial text,
	comp_final text,
	simi_raw text,
	simi_refined text,
    is_active text default 'Y'
);