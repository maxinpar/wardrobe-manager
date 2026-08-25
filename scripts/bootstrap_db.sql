-- One-off: create the wardrobe database and its owning role on PG15 (port 5432).
-- Run as the postgres superuser:
--
--   psql -U postgres -h localhost -p 5432 -f scripts/bootstrap_db.sql
--
-- It prompts for a password for the new role, so the password never lands in
-- shell history, in this file, or in the repo. Put that same password into .env
-- as part of DATABASE_URL.
--
-- This script only CREATEs. It drops nothing and touches no existing database.
-- If the role or database already exists you'll get a "already exists" error,
-- which is harmless — skip that statement and carry on.

\prompt 'Password for the new wardrobe_app role: ' pw

CREATE ROLE wardrobe_app LOGIN PASSWORD :'pw';

-- CREATEDB so the export round-trip check can build its own scratch database.
ALTER ROLE wardrobe_app CREATEDB;

CREATE DATABASE wardrobe OWNER wardrobe_app ENCODING 'UTF8' TEMPLATE template0;

\connect wardrobe

GRANT ALL ON SCHEMA public TO wardrobe_app;
ALTER SCHEMA public OWNER TO wardrobe_app;
