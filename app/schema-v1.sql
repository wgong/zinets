-- desc cannot be column name, rename to desc_cn
-- rename column: uid to u_id
-- rename column: zi_mid_front to zi_mid_out
-- rename column: zi_mid_back to zi_mid_int

drop table if exists t_zi;
create table if not exists t_zi
(
        zi text NOT NULL,
        desc_cn text,
        pinyin text,
        nstrokes int,
        alias text,
        is_radical int,
        as_part int,
        is_zi int,
        has_traditional int,
        zi_en text,
        desc_en text,
        id text NOT NULL,
        ts text,
        u_id text,
        sort_val real,
        is_active int default 0
);

drop table if exists t_zi_part;
create table if not exists t_zi_part
(
        zi text NOT NULL,
        zi_left_up text,
        zi_left text,
        zi_left_down text,
        zi_up text,
        zi_mid text,
        zi_down text,
        zi_right_up text,
        zi_right text,
        zi_right_down text,
        zi_mid_out text,
        zi_mid_in text,
        id text NOT NULL,
        ts text,
        u_id text,
        shuwen_desc text,
        is_active int default 0
);

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

drop table if exists t_zi_shufa;
create table if not exists t_zi_shufa
(
        zi text NOT NULL,
        seq_num int,
        shufa_type text,
        url_img text,
        id text NOT NULL,
        ts text,
        u_id text,
        is_active int default 0
);

drop table if exists t_zi_word;
create table if not exists t_zi_word
(
        zi text NOT NULL,
        zi_0 text,
        zi_1 text,
        zi_2 text,
        zi_3 text,
        zi_4 text,
        zi_5 text,
        zi_6 text,
        zi_7 text,
        zi_8 text,
        zi_9 text,
        desc_cn text,
        word_en text,
        desc_en text,
        id text NOT NULL,
        ts text,
        u_id text,
        is_active int default 0
);

drop table if exists t_zi_text;
create table if not exists t_zi_text
(
        zi text NOT NULL,
        zi_text text,
        desc_cn text,
        zi_text_en text,
        desc_en text,
        id text NOT NULL,
        ts text,
        u_id text,
        is_active int default 0
);

drop table if exists t_zi_media;
create table if not exists t_zi_media
(
        zi text NOT NULL,
        seq_num int,
        media_type text,
        desc_cn text,
        desc_en text,
        id text NOT NULL,
        ts text,
        u_id text,
        is_active int default 0
);