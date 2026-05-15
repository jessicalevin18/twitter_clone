\set ON_ERROR_STOP on

BEGIN;

CREATE TABLE IF NOT EXISTS urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id_users BIGINT PRIMARY KEY,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    id_urls BIGINT REFERENCES urls(id_urls),
    friends_count INTEGER,
    listed_count INTEGER,
    favourites_count INTEGER,
    statuses_count INTEGER,
    protected BOOLEAN,
    verified BOOLEAN,
    screen_name TEXT,
    name TEXT,
    location TEXT,
    description TEXT,
    withheld_in_countries VARCHAR(2)[],
    FOREIGN KEY (id_urls) REFERENCES urls(id_urls)
);

CREATE TABLE IF NOT EXISTS tweets (
    id_tweets BIGINT PRIMARY KEY,
    id_users BIGINT,
    created_at TIMESTAMPTZ,
    in_reply_to_status_id BIGINT,
    in_reply_to_user_id BIGINT,
    quoted_status_id BIGINT,
    retweet_count SMALLINT,
    favorite_count SMALLINT,
    quote_count SMALLINT,
    withheld_copyright BOOLEAN,
    withheld_in_countries VARCHAR(2)[],
    source TEXT,
    text TEXT,
    country_code VARCHAR(2),
    state_code VARCHAR(2),
    lang TEXT,
    place_name TEXT,
    FOREIGN KEY (id_users) REFERENCES users(id_users),
    FOREIGN KEY (in_reply_to_user_id) REFERENCES users(id_users)
);

CREATE TABLE IF NOT EXISTS credentials (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

-- Extensions and indexes (IF NOT EXISTS so safe to re-run)
CREATE EXTENSION IF NOT EXISTS rum;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

ALTER TABLE tweets ADD COLUMN IF NOT EXISTS tsv_text TSVECTOR
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(text, ''))) STORED;

CREATE INDEX IF NOT EXISTS tweets_rum_tsv ON tweets USING rum(tsv_text);
CREATE INDEX IF NOT EXISTS tweets_index_withheldincountries ON tweets USING gin(withheld_in_countries);
CREATE INDEX IF NOT EXISTS tweets_trgm_text ON tweets USING gin(text gin_trgm_ops);
CREATE INDEX IF NOT EXISTS tweets_index_created_at ON tweets(created_at DESC);
CREATE INDEX IF NOT EXISTS users_index_screen_name ON users(screen_name);

COMMIT;
