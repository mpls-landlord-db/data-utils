import os
import click
from .read_csv import read_csv
from .table_map import TableMap
from .schema_file import SchemaFile


class App:

  def __init__(self, database_url='', schema_directory='./schemas', use_uuid=False, mapping=[]):
    self.schema_directory = schema_directory
    self.table_map = TableMap(
      database_url=database_url,
      schema_directory=schema_directory,
      use_uuid=use_uuid,
      mapping=mapping
    )


  def run(self):

    @click.group()
    def app():
      pass

    @click.command()
    @click.option('-s', '--schema-name', help='The name of the file containing the sql statement that will be used to create your database table')
    @click.option('-t', '--table-name', help='The name of the database table you wish to create')
    def create_schema(schema_name, table_name):
      '''
      Create a file with a prepared SQL statement that will be used to create a table in a PostgreSQL database.

      We use the `mapping` passed to `App` to generate the sql column names and types
      '''
      if not schema_name:
        raise Exception('You must provide a -s or --schema-name argument')
      if not table_name:
        raise Exception('You must provide a -t or --table-name argument')
      self.table_map.write_schema_file(schema_name, table_name)


    @click.command()
    @click.option('-s', '--schema-name', help='The name of the file containing the sql statement that will be used to create your database table')
    def create_table(schema_name):
      '''
      Execute the prepared statement in a schema file to create a PostgreSQL database table.
      
      We use the "--schema-name" argument to look up the schema in the `App.schema_directory`. Assuming you have not overridden the default schema directory,
      passing "my-schema" would find "./schemas/my-schema.sql" given this directory structure:

      \b
      app/
        schemas/
          my-schema.sql
        main.py

      '''
      if not schema_name:
        raise Exception('You must provide a -s or --schema-name argument')
      self.table_map.create_table(schema_name)

    
    @click.command()
    @click.option('-d', '--data-path', help='Relative path to CSV file containing the data you wish to insert into your database')
    @click.option('-t', '--table_name', help='The name of the database table into which you wish to insert data')
    def transfer_data(data_path, table_name):
      '''
      Transfer data from a CSV file to a PostgreSQL database table.
      '''
      if not data_path:
        raise Exception('You must provide a -d or --data-path argument')
      if not table_name:
        raise Exception('You must provide a -t or --table-name argument')
      data = read_csv(data_path)
      self.table_map.transfer_data(table_name, data)

    
    @click.command()
    def ls():
      '''
      List all schema files
      '''
      for x in os.listdir(self.schema_directory):
        click.echo(x)

    
    @click.command()
    @click.option('-s', '--schema-name', help='The name of the file containing the sql statement that will be used to create your database table')
    def show(schema_name):
      '''
      Show contents of schema file
      '''
      click.echo(SchemaFile.read(schema_name, self.schema_directory))



    app.add_command(create_schema)
    app.add_command(create_table)
    app.add_command(transfer_data)
    app.add_command(ls)
    app.add_command(show)

    app()