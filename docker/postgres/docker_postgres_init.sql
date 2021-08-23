CREATE USER dagster WITH PASSWORD 'dagster' CREATEDB;
CREATE DATABASE dagster
    WITH 
    OWNER = dagster
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;