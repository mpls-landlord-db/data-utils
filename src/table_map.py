import os
import collections
from datetime import date
from .database import Database
from .schema_file import SchemaFile

def create_insert_statement(table_name, col_names, use_uuid):
  rv = 'INSERT INTO {} ('.format(table_name)
  for i, col_name in enumerate(col_names):
    if i < len(col_names) - 1:
      rv += '{},'.format(col_name)
    else:
      rv += '{})'.format(col_name)
  rv += ' VALUES ('
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
  def __init__(self, database_url='', schema_directory='./schemas', use_uuid=False, mapping=[]):
    self.columns = collections.OrderedDict()
    self.csv_sql_colnames = {}
    self.use_uuid = use_uuid
    self.database = Database(database_url=database_url)
    self.schema_directory = schema_directory
    for x in mapping:
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

  def generate_schema_string(self, table_name):
    rv = ''
    if self.use_uuid:
      rv += 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";\n\n'
    rv += 'CREATE TABLE {} (\n'.format(table_name)
    if self.use_uuid:
      rv += ' id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),\n'
    for i, col_name in enumerate(self.columns):
      col = self.get_column(col_name)
      if i < len(self.columns) - 1:
        rv += ' {},\n'.format(col.to_sql())
      else:
        rv += ' {}\n'.format(col.to_sql())
    rv += ');'
    return rv

  def write_schema_file(self, schema_name, table_name):
    SchemaFile.write(
      schema_name,
      self.generate_schema_string(table_name),
      self.schema_directory
    )
  
  def create_table(self, schema_name):
    sql = SchemaFile.read(schema_name, self.schema_directory)
    self.database.execute(sql)

  def transfer_data(self, table_name, csv_rows=[]):
    sql = create_insert_statement(table_name, self.columns.keys(), self.use_uuid)
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
    total_rows = len(rows)
    chunk_size = 1000
    complete_chunks = 0
    print('')
    print('   Inserting {} rows...'.format(total_rows))
    print('')
    while len(rows):
      chunk = rows[:chunk_size]
      rows = rows[chunk_size:]
      self.database.execute_many(sql, chunk)
      complete_chunks += 1
      complete_rows = complete_chunks * chunk_size if complete_chunks * chunk_size < total_rows else total_rows 
      percent_complete = round((complete_rows / total_rows) * 100)
      print('   {}% complete'.format(percent_complete), end='\r' if percent_complete < 100 else '\n')