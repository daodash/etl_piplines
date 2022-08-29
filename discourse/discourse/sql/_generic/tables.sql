DROP TABLE IF EXISTS daodash_ny.discourse_categories;
DROP TABLE IF EXISTS daodash_ny.discourse_topics;

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_categories (
    id integer NOT NULL CONSTRAINT categories_pk PRIMARY KEY,
    name varchar(50) NOT NULL,
    slug varchar(20) NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_topics (
    id integer NOT NULL CONSTRAINT topics_pk PRIMARY KEY,
    title character varying NOT NULL,
    slug character varying,
    user_id integer,
    category_id integer,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    last_post_user_id integer NOT NULL,
    last_posted_at timestamp without time zone,
    views_count integer DEFAULT 0 NOT NULL,
    posts_count integer DEFAULT 0 NOT NULL,
    reply_count integer DEFAULT 0 NOT NULL,
    like_count integer DEFAULT 0 NOT NULL,
    is_pinned boolean DEFAULT false NOT NULL,
    is_visible boolean DEFAULT true NOT NULL,
    is_closed boolean DEFAULT false NOT NULL,
    is_archived boolean DEFAULT false NOT NULL,
    deleted_by_id integer,
    deleted_at timestamp without time zone
);
