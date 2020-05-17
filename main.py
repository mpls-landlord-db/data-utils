import sys
import dotenv
import database
import csv_parser

def main():
  path = sys.argv[1]
  tablename = path.split('/')[-1].replace('.csv', '').lower()
  parsed = csv_parser.parse(path)
  database.create_table(tablename, parsed['colnames'])
  database.insert_rows(tablename, parsed['rows'])

if __name__ == '__main__':
  dotenv.load_dotenv()
  main()