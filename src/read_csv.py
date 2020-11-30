import os
import csv

def read_csv(path):
  '''
  Returns a list of dictionaries where thee keys are CSV column names and the values are CSV column values

  args:
    path: str - A relative path to the CSV file you want to read.
  '''
  with open(os.path.abspath(path)) as f:
    dict_rows = list(csv.DictReader(f))
  return dict_rows