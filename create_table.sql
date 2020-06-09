DROP TABLE IF EXISTS mpls_active_rental_licenses;
-- DROP EXTENSION IF EXISTS "uuid-ossp";
-- DROP DOMAIN PHONE_NUMBER;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- CREATE DOMAIN
--   PHONE_NUMBER AS TEXT
--   CHECK (VALUE ~ E'^\\d{10}$');

CREATE TABLE IF NOT EXISTS mpls_active_rental_licenses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  apn VARCHAR,
  objectid VARCHAR,
  license_number VARCHAR,
  category VARCHAR,
  milestone VARCHAR,
  tier VARCHAR,
  status VARCHAR,
  issue_date BIGINT default 0,
  expiration_date BIGINT default 0,
  address VARCHAR,
  owner_name VARCHAR,
  owner_address1 VARCHAR,
  owner_address2 VARCHAR,
  owner_city VARCHAR,
  owner_state VARCHAR,
  owner_zip VARCHAR,
  owner_phone VARCHAR,
  owner_email VARCHAR,
  applicant_name VARCHAR,
  applicant_address1 VARCHAR,
  applicant_address2 VARCHAR,
  applicant_city VARCHAR,
  applicant_state VARCHAR,
  applicant_zip VARCHAR,
  applicant_phone VARCHAR,
  applicant_email VARCHAR,
  licensed_units INT default 0,
  ward VARCHAR,
  neighborhood_desc VARCHAR,
  community_desc VARCHAR,
  police_precinct VARCHAR,
  latitude DOUBLE PRECISION default 0.0,
  longitude DOUBLE PRECISION default 0.0,
  x_web_mercator DOUBLE PRECISION default 0.0,
  y_web_mercator DOUBLE PRECISION default 0.0
)

