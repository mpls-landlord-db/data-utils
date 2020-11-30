import os
import importlib
import click
from src import TableMap, read_csv


@click.group()
def app():
  pass


@click.command()
@click.option('-m', '--mapping-path', help='The import path of the module holding your "mapping=TableMap(...)" definition')
@click.option('-t', '--table-name', help='The name of the database table you wish to create')
@click.option('-s', '--schema-name', help='The name of the file holding the sql statement that will be used to create your database table')
@click.option('--use-uuid', is_flag=True, help='Include an "id UUID PRIMARY KEY DEFAULT uuid_generate_v4()," column in your schema definition')
def create_schema(mapping_path, schema_name, table_name, use_uuid):
  '''
  Generate a schema file in "./schemas/" directory 
  using mapping imported from provided MAPPING import
  path arg
  '''
  mapping_mod = importlib.import_module(mapping_path)
  table_map = TableMap({
    'table_name': table_name,
    'schema_name': schema_name,
    'mapping': mapping_mod.mapping
  })
  table_map.write_schema_file(use_uuid)



@click.command()
@click.option('-s', '--schema-name')
def create_table(schema_name):
  '''
  Create a PostgreSQL database table using the content
  in the SCHEMA_FILE
  '''
  table_map = TableMap({
    'schema_name': schema_name,
    'database_url': os.environ.get('DATABASE_URL'),
  })
  table_map.create_table()


@click.command()
@click.option('-m', '--mapping-path', help='The import path of the module holding your "mapping=TableMap(...)" definition')
@click.option('-d', '--data-path', help='Relative path to CSV file containing the data you wish to insert into your database')
@click.option('-t', '--table-name', help='The name of the database table into which you wish to insert data')
def transfer_data(mapping_path, data_path, table_name):
  '''
  Transfer data from a CSV
  '''
  mapping_mod = importlib.import_module(mapping_path)
  table_map = TableMap({
    'database_url': os.environ.get('DATABASE_URL'),
    'table_name': table_name,
    'mapping': mapping_mod.mapping,
  })
  table_map.transfer_data(read_csv(data_path))



app.add_command(create_table)
app.add_command(create_schema)
app.add_command(transfer_data)


if __name__ == '__main__':
  app()
