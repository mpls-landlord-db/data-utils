import os
from datetime import date
from collections import OrderedDict

class Column:
  def __init__(self, csv_colname='', sql_colname='', pytype=None, transformer=None):
    self.csv_colname = csv_colname
    self.sql_colname = sql_colname
    self.pytype = pytype
    self.transformer = transformer

  def __repr__(self):
    return f'''
  Column: {self.parse_colname()}
  ----------------------------------
  PROPERTIES:
    csv_colname = {self.csv_colname}
    sql_colname = {self.sql_colname}
    pytype = {self.pytype}
    transformer = {self.transformer}

  SQL:
    {self.parse_colname()} {self.parse_type()}
  '''

  def parse_colname(self):
    return self.sql_colname if self.sql_colname else self.csv_colname

  def parse_type(self):
    if self.pytype == int: return 'INTEGER'
    elif self.pytype == str: return 'VARCHAR'
    elif self.pytype == float: return 'DOUBLE PRECISION'
    elif self.pytype == date: return 'TIMESTAMPTZ'
    raise 'Unable to parse pytype'

  def to_sql(self):
    return f'{self.parse_colname()} {self.parse_type()}'


class CsvSqlMap:
  '''
  Use this class to generate a postgresql table schema
  '''

  def __init__(self, tablename='', schema_path='./schema.sql', col_mapping=[]):
    self.columns = OrderedDict()
    self.tablename = tablename
    self.schema_path = schema_path
    for x in col_mapping:
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
    self.columns.update({ col.parse_colname(): col })

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
        


