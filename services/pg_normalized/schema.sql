
\set ON_ERROR_STOP on

BEGIN;

DROP TABLE IF EXISTS tweets CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS urls CASCADE;
DROP TABLE IF EXISTS credentials CASCADE;

CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

CREATE TABLE users (
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

CREATE TABLE tweets (
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

    -- NOTE:
    -- We do not have the following foreign keys because they would require us
    -- to store many unhydrated tweets in this table.
    -- FOREIGN KEY (in_reply_to_status_id) REFERENCES tweets(id_tweets),
    -- FOREIGN KEY (quoted_status_id) REFERENCES tweets(id_tweets)
);

CREATE INDEX tweets_index_created_at ON tweets(created_at DESC);
CREATE INDEX tweets_index_withheldincountries ON tweets USING gin(withheld_in_countries);

CREATE TABLE credentials (
    username TEXT PRIMARY KEY,
    password TEXT
);

COMMIT;

