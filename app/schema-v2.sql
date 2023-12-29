-- schema for ZiZi app
--===================================

-- Zi character
drop table if exists t_zi;
create table if not exists t_zi
(
    zi text NOT NULL,  -- unique
    u_id text,    -- internal id
    unicode text,
    pinyin text,
    nstrokes text,
    alias text,
    traditional text,
    as_part text,
    is_radical text,
	layer text,
    desc_cn text,
    zi_en text,
    desc_en text,
    ts text,
    sort_val real,
    is_active text default 'Y'
);

-- Zi part
drop table if exists t_part;
create table if not exists t_part
(
    zi text NOT NULL,   -- radical , unique
    u_id text,    -- internal id
    traditional text,
    pinyin text,
    strokes text,
    meaning text,
    example text,
    category text,
    is_active text default 'Y'
);

-- Zi decomposed
drop table if exists t_zi_part;
create table if not exists t_zi_part
(
    zi text NOT NULL,  -- non-unique
    u_id text,    -- internal id
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
    ts text,
    desc_cn text,
    desc_en text,
    hsk_note text,
    id_shuowen text,
    is_active text default 'Y'
);

-- emoji
drop table if exists t_emoji;
create table if not exists t_emoji
(
    desc_en text NOT NULL,
    desc_cn text,
    unicodes text,
    u_id text,
    sample_ text,
    browser_ text,
    category text,
    ts text,
    is_active text default 'Y'
);

-- shufa
drop table if exists t_shufa;
create table if not exists t_shufa
(
    title text NOT NULL,
    u_id text,
    shufa_type text,
    img_url text,
    ts text,
    is_active text default 'Y'
);

-- short text: phrase/word
drop table if exists t_phrase;
create table if not exists t_phrase
(
    title text NOT NULL,
    u_id text,
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
    desc_en text,
    ts text,
    is_active text default 'Y'
);

-- long text: article/book
drop table if exists t_text;
create table if not exists t_text
(
    title text NOT NULL,
    u_id text,
    desc_cn text,
    desc_en text,
    ts text,
    is_active text default 'Y'
);

-- resource: text/image/audio/video
drop table if exists t_resource;
create table if not exists t_resource
(
    title text NOT NULL,
    u_id text,
    media_type text,  -- text/image/audio/video
    desc_cn text,
    desc_en text,
    link_url text,
    ts text,
    is_active text default 'Y'
);

-- note: note-taking: journal/resource
-- similar to watchetf app table: notes
drop table if exists t_note;
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