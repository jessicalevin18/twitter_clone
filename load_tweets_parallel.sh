#!/bin/sh

files1=$(find data/*)
files='/data/tweets/geoTwitter21-01-01.zip
/data/tweets/geoTwitter21-01-02.zip
/data/tweets/geoTwitter21-01-03.zip
/data/tweets/geoTwitter21-01-04.zip
/data/tweets/geoTwitter21-01-05.zip
/data/tweets/geoTwitter21-01-06.zip
/data/tweets/geoTwitter21-01-07.zip
/data/tweets/geoTwitter21-01-08.zip
/data/tweets/geoTwitter21-01-09.zip
/data/tweets/geoTwitter21-01-10.zip'

echo '================================================================================'
echo 'load data'
echo '================================================================================'
# FIXME: implement this with GNU parallel
time echo "$files1" | parallel -j $(nproc) 'time python3 load_tweets.py --inputs="{}" --db postgresql://postgres:pass@localhost:24528'
# time echo "$files" | parallel -j $(nproc) 'time python3 load_tweets_batch.py --inputs="{}" --db postgresql://postgres:pass@localhost:10871'
