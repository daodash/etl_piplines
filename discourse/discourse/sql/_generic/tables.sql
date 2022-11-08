/*
DROP TABLE IF EXISTS daodash_ny.discourse_users;
DROP TABLE IF EXISTS daodash_ny.discourse_categories;
DROP TABLE IF EXISTS daodash_ny.discourse_topics;
DROP TABLE IF EXISTS daodash_ny.discourse_posts;
DROP TABLE IF EXISTS daodash_ny.discourse_polls;
DROP TABLE IF EXISTS daodash_ny.discourse_poll_votes;
*/

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_users (
    id integer NOT NULL CONSTRAINT pk_discourse_users PRIMARY KEY,
    username varchar(50) NOT NULL,
    name varchar(100) NULL,
    days_visited integer DEFAULT 0 NOT NULL,
    time_read integer DEFAULT 0 NOT NULL,
    topics_entered integer DEFAULT 0 NOT NULL,
    topic_count integer DEFAULT 0 NOT NULL,
    posts_read integer DEFAULT 0 NOT NULL,
    post_count integer DEFAULT 0 NOT NULL,
    likes_received integer DEFAULT 0 NOT NULL,
    likes_given integer DEFAULT 0 NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_categories (
    id integer NOT NULL CONSTRAINT pk_discourse_categories PRIMARY KEY,
    name varchar(50) NOT NULL,
    slug varchar(20) NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_topics (
    id integer NOT NULL CONSTRAINT pk_discourse_topics PRIMARY KEY,
    category_id integer NOT NULL,
    title varchar(200) NOT NULL,
    slug varchar(200) NULL,
    excerpt text NULL,
    views_count integer DEFAULT 0 NOT NULL,
    posts_count integer DEFAULT 0 NOT NULL,
    reply_count integer DEFAULT 0 NOT NULL,
    like_count integer DEFAULT 0 NOT NULL,
    is_pinned boolean DEFAULT false NOT NULL,
    is_visible boolean DEFAULT true NOT NULL,
    is_closed boolean DEFAULT false NOT NULL,
    is_archived boolean DEFAULT false NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NULL,
    last_post_user_id integer NULL,
    last_posted_at timestamp NULL,
    deleted_by_user_id integer NULL,
    deleted_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_posts (
    id integer NOT NULL CONSTRAINT pk_discourse_posts PRIMARY KEY,
    topic_id integer NOT NULL, 
    content text NOT NULL,
    reply_count integer DEFAULT 0 NOT NULL,
    reads_count integer DEFAULT 0 NOT NULL,
    readers_count integer DEFAULT 0 NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NULL,
    deleted_by_user_id integer NULL,
    deleted_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_polls (
    id bigint NOT NULL CONSTRAINT pk_discourse_polls PRIMARY KEY,
    post_id integer NOT NULL,
    title varchar(250) NULL,
    status varchar(30) NOT NULL,
    voters_count integer DEFAULT 0 NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NULL
);

CREATE TABLE IF NOT EXISTS daodash_ny.discourse_poll_votes (
    id bigint NOT NULL CONSTRAINT pk_discourse_poll_votes PRIMARY KEY,
    poll_id bigint NOT NULL,
    vote_option varchar(500) NULL,
    votes_count integer DEFAULT 0 NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NULL
);

/*
CREATE SEQUENCE daodash_ny.discourse_polls_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE daodash_ny.discourse_polls_id_seq OWNED BY daodash_ny.discourse_polls.id;

CREATE SEQUENCE daodash_ny.discourse_poll_votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE daodash_ny.discourse_poll_votes_id_seq OWNED BY daodash_ny.discourse_poll_votes.id;
*/

/*
select * from daodash_ny.discourse_users;
select * from daodash_ny.discourse_categories;
select * from daodash_ny.discourse_topics;
select * from daodash_ny.discourse_posts;
select * from daodash_ny.discourse_polls;
select * from daodash_ny.discourse_poll_votes;
*/
