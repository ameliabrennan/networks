DROP TABLE IF EXISTS canvas_postgres_copy_timestamp CASCADE;

CREATE TABLE canvas_postgres_copy_timestamp (
	date_updated timestamp
);

INSERT INTO canvas_postgres_copy_timestamp VALUES (current_timestamp);