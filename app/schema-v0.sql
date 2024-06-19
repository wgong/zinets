-- table to store zi (unicode), description, and their translations in English (en), Spanish (es)
-- Extend support for additional target language(s) by adding columns
create table if not exists t_zi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    zi text NOT NULL,
    desc text,

    zi_en text,
    desc_en text,

    zi_es text,
    desc_es text,

    pinyin text,
    nstrokes INTEGER,

    is_radical INTEGER,
    is_zi INTEGER,
    is_traditional INTEGER,

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,


    CONSTRAINT uk_zi UNIQUE (zi)
);


-- table to store disected zi parts
create table if not exists  t_zi_part (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    zi text NOT NULL,

    lu text,  -- left up part
    l text,  -- left part
    ld text,  -- left down part
    u text,  -- up part
    m text,  -- mid part
    d text,  -- down part
    ru text,  -- right up part
    r text,  -- right part
    rd text,  -- right down part
    mf text,  -- mid front
    mb text,  -- mid back

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,


    CONSTRAINT uk_zi UNIQUE (zi)
);

-- table to store Zi's calligraphy
create table if not exists  t_zi_shufa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    zi text NOT NULL,

    url_img_1 text,     -- 甲骨 
    url_img_2 text,     -- 金 
    url_img_3 text,     -- 篆
    url_img_4 text,     -- 隶
    url_img_5 text,     -- 楷
    url_img_6 text,     -- 行
    url_img_7 text,     -- 草

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,


    CONSTRAINT uk_zi UNIQUE (zi)
);

-- table to store related short 词 word/vocabulary (up to 10 Zi sequence), overflow to t_zi_text if longer
create table if not exists  t_zi_word (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    zi text NOT NULL,

    zi_0 text,  -- FK to t_zi.zi
    zi_1 text,
    zi_2 text,
    zi_3 text,
    zi_4 text,
    zi_5 text,
    zi_6 text,
    zi_7 text,
    zi_8 text,
    zi_9 text,

    word_en text,
    word_es text,

    desc text,
    desc_en text,
    desc_es text,

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,


    CONSTRAINT uk_zi UNIQUE (zi)
);

-- table to store related long phrases/sentences
create table if not exists  t_zi_text (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    zi text NOT NULL,

    desc text,  -- long description
    desc_en text,
    desc_es text,

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,


    CONSTRAINT uk_zi UNIQUE (zi)
);

-- table to store related media resources (url, img, audio, video, book)
create table if not exists  t_zi_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    zi text NOT NULL,

    media_type text, -- url, image, audio, video, book
    url text,

    desc text,  -- long description
    desc_en text,
    desc_es text,

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,

    CONSTRAINT uk_zi UNIQUE (zi)
);

-- store user info
create table if not exists  t_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id text  NOT NULL,     -- email or user_id
    pwd text,                   -- encrypted password

    role_name text,             -- admin, dev, reviewer, user

    countries text,             -- user countries of origin
    languages text,             -- user languages spoken 

    -- sys_cols
    is_active INTEGER default 0,
    uid INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    uid_created INTEGER REFERENCES t_user (id) ON DELETE CASCADE,
    ts text,
    ts_created text,

    CONSTRAINT uk_userid UNIQUE (user_id)
);