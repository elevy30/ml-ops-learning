-- Create the user
CREATE USER eyall WITH PASSWORD 'eyall'
    superuser
    createdb
    createrole
    replication
    bypassrls;

-- Create the database
CREATE DATABASE eyall_db;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE eyall_db TO eyall;

-- -- Connect to the new database and set up permissions
-- \c eyall_db
--
-- -- Grant schema permissions
-- GRANT ALL ON SCHEMA public TO eyall;