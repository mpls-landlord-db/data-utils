import sys
from datetime import date
from lib.transformers import utc_from_timestamp, format_phone
from lib.csv_to_sql import CsvSqlMap


def main():
  m = CsvSqlMap('active_rental_licenses', './schema.sql', col_mapping=[
    ('apn', '', str, None),
    ('OBJECTID', 'object_id', int, None),
    ('licenseNumber', 'license_number', str, None),
    ('category', '', str, None),
    ('milestone', '', str, None),
    ('tier', '', str, None),
    ('status', '', str, None),
    ('issueDate', 'issuee_date', date, utc_from_timestamp),
    ('expirationDate', 'expiration_date', date, utc_from_timestamp),
    ('address', '', str, None),
    ('ownerName', 'owner_name', str, None),
    ('ownerAddress1', 'owner_address_1', str, None),
    ('ownerAddress2', 'owner_address_2', str, None),
    ('ownerCity', 'owner_city', str, None),
    ('ownerState', 'owner_state', str, None),
    ('ownerZip', 'owner_zip', str, None),
    ('ownerPhone', 'owner_phone', str, format_phone),
    ('ownerEmail', 'owner_email', str, None),
    ('applicantName', 'applicant_name', str, None),
    ('applicantAddress1', 'applicant_address_1', str, None),
    ('applicantAddress2', 'applicant_address_2', str, None),
    ('applicantCity', 'applicant_city', str, None),
    ('applicantState', 'applicant_state', str, None),
    ('applicantZip', 'applicant_zip', str, None),
    ('applicantPhone', 'applicant_phone', str, format_phone),
    ('applicantEmail', 'applicant_email', str, None),
    ('licensedUnits', 'licensed_units', int, None),
    ('ward', '', str, None),
    ('neighborhoodDesc', 'neighborhood_desc', str, None),
    ('communityDesc', 'community_desc', str, None),
    ('policePrecinct', 'police_precinct', str, None),
    ('latitude', '', float, None),
    ('longitude', '', float, None),
    ('xWebMercator', 'x_web_mercator', float, None),
    ('yWebMercator', 'y_web_mercator', float, None)
  ])
  m.write_schema_file()

  print(m.get_column('applicant_phone'))
  print(m.generate_schema_string())


if __name__ == '__main__':
  main()

  
