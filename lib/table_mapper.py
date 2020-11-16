import os
import collections
from datetime import date
from .database import Database

class Column:
  def __init__(self, csv_colname='', sql_colname='', pytype=None, transformer=None):
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
  def __init__(self, database_url='', tablename='', schema_path='./schema.sql', mapping=[]):
    self.columns = collections.OrderedDict()
    self.database = Database(database_url=database_url)
    self.tablename = tablename
    self.schema_path = schema_path 
    self.csv_sql_colnames = {}
    for x in mapping:
      self.csv_sql_colnames[x[0]] = x[1] if x[1] else x[0]
      self.add_column(
        csv_colname=x[0],
        sql_colname=x[1],
        pytype=x[2],
        transformer=x[3]
      )
  
  def get_column(self, key):
    return self.columns.get(key)

  def add_column(self, csv_colname='', sql_colname='', pytype=None, transformer=None):
    col = Column(csv_colname, sql_colname, pytype, transformer)
    self.columns.update({ col.get_sql_colname(): col })

  def generate_schema_string(self):
    rv = f'CREATE TABLE {self.tablename} (\n'
    for i, colname in enumerate(self.columns):
      col = self.columns[colname]
      if i < len(self.columns) - 1:
        rv += f'  {col.to_sql()},\n'
      else:
        rv += f'  {col.to_sql()}\n'
    rv += ');'
    return rv

  def write_schema_file(self):
    with open(os.path.abspath(self.schema_path), 'w') as f:
      f.write(self.generate_schema_string())

  def create_table(self):
    with open(os.path.abspath(self.schema_path)) as f:
      schema = f.read()
    try:
      self.database.execute(schema)
    except Exception as exc:
      print('The was an error when trying to create the table', exc)
    
  def transfer_data(self, csv_rows):
    '''
    Insert data into the postgres table
    '''
    sql = create_insert_statement(self.tablename, self.columns.keys())
    rows = []
    for csv_row in csv_rows:
      row = {}
      for csv_colname in csv_row:
        sql_colname = self.csv_sql_colnames[csv_colname]
        if self.columns[sql_colname].transformer:
          row[sql_colname] = self.columns[sql_colname].transformer(csv_row[csv_colname])
        else:
          row[sql_colname] = csv_row[csv_colname]
      rows.append(row)
    self.database.execute_many(sql, rows)
        


def create_insert_statement(tablename, col_names):
  sql = f'INSERT INTO {tablename} VALUES ('
  for i, col_name in enumerate(col_names):
    if i < len(col_names) - 1:
      sql += f'%({col_name})s, '
    else:
      sql += f'%({col_name})s);'
  return sql