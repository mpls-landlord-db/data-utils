import os
import collections
from datetime import date
from .database import Database
from .schema_file import SchemaFile

def create_insert_statement(table_name, col_names):
  rv = 'INSERT INTO {} VALUES ('.format(table_name)
  for i, col_name in enumerate(col_names):
    if i < len(col_names) - 1:
      rv += '%({})s, '.format(col_name)
    else:
      rv += '%({})s);'.format(col_name)
  return rv

class Column:
  def __init__(self, csv_colname, sql_colname, pytype, transformer):
    self.csv_colname = csv_colname
    self.sql_colname = sql_colname
    self.pytype = pytype
    self.transformer = transformer

  def __repr__(self):
    return f'''
  Column: {self.get_sql_colname()}
  ----------------------------------
  PROPERTIES:
    csv_colname = {self.csv_colname}
    sql_colname = {self.sql_colname}
    pytype = {self.pytype}
    transformer = {self.transformer}

  SQL:
    {self.get_sql_colname()} {self.get_sql_type()}
  '''

  def get_sql_colname(self):
    return self.sql_colname if self.sql_colname else self.csv_colname

  def get_sql_type(self):
    if self.pytype == int: return 'INTEGER'
    elif self.pytype == str: return 'VARCHAR'
    elif self.pytype == float: return 'DOUBLE PRECISION'
    elif self.pytype == date: return 'TIMESTAMPTZ'
    raise 'Unable to parse pytype'

  def to_sql(self):
    return f'{self.get_sql_colname()} {self.get_sql_type()}'

  

class TableMap:
  def __init__(self, config={}):
    self.columns = collections.OrderedDict()
    self.csv_sql_colnames = {}
    self.database = Database(database_url=config.get('database_url'))
    self.table_name = config.get('table_name')
    self.schema_name = config.get('schema_name', 'schema')
    self.schema_directory = config.get('schema_directory', './schemas')
    for x in config.get('mapping', []):
      self.csv_sql_colnames[x[0]] = x[1] if x[1] else x[0]
      self.add_column(
        csv_colname=x[0],
        sql_colname=x[1],
        pytype=x[2],
        transformer=x[3]
      )

  def get_column(self, col_name):
    return self.columns.get(col_name)

  def add_column(self, csv_colname='', sql_colname='', pytype=None, transformer=None):
    col = Column(csv_colname, sql_colname, pytype, transformer)
    self.columns.update({ col.get_sql_colname(): col })

  def generate_schema_string(self, use_uuid=False):
    rv = ''
    if use_uuid:
      rv += 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";\n\n'
    rv += 'CREATE TABLE {} (\n'.format(self.table_name)
    if use_uuid:
      rv += ' id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),\n'
    for i, col_name in enumerate(self.columns):
      col = self.get_column(col_name)
      if i < len(self.columns) - 1:
        rv += ' {},\n'.format(col.to_sql())
      else:
        rv += ' {}\n'.format(col.to_sql())
    rv += ');'
    return rv

  def write_schema_file(self, use_uuid=False):
    SchemaFile.write(
      self.schema_name,
      self.generate_schema_string(use_uuid),
      self.schema_directory
    )
  
  def create_table(self):
    sql = SchemaFile.read(self.schema_name, self.schema_directory)
    self.database.execute(sql)

  def transfer_data(self, csv_rows=[]):
    sql = create_insert_statement(self.table_name, self.columns.keys())
    rows = []
    for csv_row in csv_rows:
      row = {}
      for csv_colname in csv_row:
        sql_colname = self.csv_sql_colnames.get(csv_colname)
        if sql_colname:
          if self.columns[sql_colname].transformer:
            row[sql_colname] = self.columns[sql_colname].transformer(csv_row[csv_colname])
          else:
            row[sql_colname] = csv_row[csv_colname]
        rows.append(row)
    self.database.execute_many(sql, rows)