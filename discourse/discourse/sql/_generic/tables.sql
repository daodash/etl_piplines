/*
DROP TABLE IF EXISTS daodash_ny.discourse_categories;
DROP TABLE IF EXISTS daodash_ny.discourse_topics;
*/

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_categories (
    id integer NOT NULL CONSTRAINT categories_pk PRIMARY KEY,
    name varchar(50) NOT NULL,
    slug varchar(20) NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_topics (
    id integer NOT NULL CONSTRAINT topics_pk PRIMARY KEY,
    title varchar(100) NOT NULL,
    slug varchar(100) NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    description text NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NULL,
    last_post_user_id integer NULL,
    last_posted_at timestamp NULL,
    views_count integer DEFAULT 0 NOT NULL,
    posts_count integer DEFAULT 0 NOT NULL,
    reply_count integer DEFAULT 0 NOT NULL,
    like_count integer DEFAULT 0 NOT NULL,
    is_pinned boolean DEFAULT false NOT NULL,
    is_visible boolean DEFAULT true NOT NULL,
    is_closed boolean DEFAULT false NOT NULL,
    is_archived boolean DEFAULT false NOT NULL,
    deleted_by_user_id integer NULL,
    deleted_at timestamp NULL
);
