import os
import csv

def read_csv(path):
  with open(os.path.abspath(path)) as f:
    dict_rows = list(csv.DictReader(f))
  return dict_rows
