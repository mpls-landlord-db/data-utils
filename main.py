import sys
import dotenv
# import database
# import csv_parser


import os
import re
import csv
import psycopg2

ACTIVE_RENTAL_LICENSE_COLUMN_NAMES = [
  'apn',
  'objectid',
  'license_number',
  'category',
  'milestone',
  'tier',
  'status',
  'issue_date',
  'expiration_date',
  'address',
  'owner_name',
  'owner_address1',
  'owner_address2',
  'owner_city',
  'owner_state',
  'owner_zip',
  'owner_phone',
  'owner_email',
  'applicant_name',
  'applicant_address1',
  'applicant_address2',
  'applicant_city',
  'applicant_state',
  'applicant_zip',
  'applicant_phone',
  'applicant_email',
  'licensed_units',
  'ward',
  'neighborhood_desc',
  'community_desc',
  'police_precinct',
  'latitude',
  'longitude',
  'x_web_mercator',
  'y_web_mercator',
]

def execute_sql(sql, rows=None):
  with psycopg2.connect(os.environ.get('DATABASE_URL')) as connection:
    with connection.cursor() as cursor:
      if rows:
        for row in rows:
          cursor.execute(sql, row)
      else:
        cursor.execute(sql)


def create_tables():
  with open('create_table.sql') as sql:
    execute_sql(sql.read())


def clean_row(row):
  rv = []
  for col in row:
    col = col.upper().strip()
    col = re.sub(r'\s{2,}', ' ', col)
    phone_match = re.match(r'^\(?(?P<first>\d{3})\)?-?(?P<second>\d{3})(-|\s)?(?P<third>\d{4})$', col)
    if phone_match:
      col = '{}{}{}'.format(phone_match.group('first'), phone_match.group('second'), phone_match.group('third'))
    rv.append(col)
  return rv

def insert_active_rental_license_data(csv_path):
  with open(os.path.abspath(csv_path)) as csv_file:
    _, *rows = list(csv.reader(csv_file))
    rows = [clean_row(row) for row in rows]
    stmt = 'INSERT INTO mpls_active_rental_licenses ({}) VALUES ({});'.format(
      ','.join(ACTIVE_RENTAL_LICENSE_COLUMN_NAMES),
      ','.join(['%s' for x in range(len(rows[0]))])
    )
    execute_sql(stmt, rows)



def main():
  create_tables()
  insert_active_rental_license_data(sys.argv[1])


if __name__ == '__main__':
  dotenv.load_dotenv()
  main()