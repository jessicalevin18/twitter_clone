FROM postgis/postgis

RUN apt-get update && apt-get install -y \
    less \
    make \
    vim \
    curl \
    gnupg \
    lsb-release

# Add pgdg apt repo which has postgresql-17-rum
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && apt-get install -y postgresql-17-rum

WORKDIR /tmp/db
RUN mkdir /data && chown postgres /data
COPY schema.sql /docker-entrypoint-initdb.d/01.sql
