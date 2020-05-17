import os
import re
import psycopg2

def format_columns(columns):
  return ',\n'.join(['{} VARCHAR'.format(x) for x in columns])

def create_table(tablename, columns):
  sql = '''
    DROP TABLE IF EXISTS {};
    CREATE TABLE {} (
      {}
    );
  '''.format(tablename, tablename, format_columns(columns))
  execute(sql)

def insert_rows(tablename, rows):
  sql = '''
    INSERT INTO {} VALUES ({});
  '''.format(tablename, ','.join(['%s' for x in range(len(rows[0]))]))
  execute(sql, rows)

def execute(sql, rows=None):
  with psycopg2.connect(os.environ.get('DATABASE_URL')) as conn:
    with conn.cursor() as cursor:
      if rows:
        for row in rows:
          cursor.execute(sql, row)
      else:
        cursor.execute(sql)

