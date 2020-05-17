import os
import re
import csv

class Casify:
  @classmethod
  def _clean(cls, txt: str):
    txt = txt.replace('\ufeff', '')
    txt = txt.replace('\n', '')
    # if whole txt is uppercased, make it lower
    if re.match(r'^[A-Z]+$', txt):
      txt = txt.lower()
    # if txt has any consecutive capital letters (myABCDetective)
    # preserve casing for beginning and end of capitals sequesnce and
    # make middle letters lowercase
    for m in re.finditer(r'([A-Z]{2,})', txt):
      match, = m.groups()
      txt = txt.replace(match, match[0] + match[1:-2].lower() + match[-1])
    return txt

  @classmethod
  def _camel_replacer(cls, m: re.Match):
    return '_' + m.string[m.start()].lower()

  @classmethod
  def camel_to_snake(cls, txt):
    return re.sub(r'([A-Z])', cls._camel_replacer, cls._clean(txt))

def format_colnames(colnames):
  if next((re.match(r'[a-z]*', x) for x in colnames), None):
    return [Casify.camel_to_snake(x) for x in colnames]
  else:
    return [x.lower().replace('\ufeff', '').replace('\n', '') for x in colnames]


def parse(path):
  with open(os.path.abspath(path)) as csv_file:
    colnames, *rows = list(csv.reader(csv_file))
  return {
    'colnames': format_colnames(colnames),
    'rows': rows
  }