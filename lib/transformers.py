import re
from datetime import datetime

def utc_from_timestamp(x):
  return datetime.utcfromtimestamp(int(x) / 1000).strftime('%Y-%m-%d %H:%M:%S')

def utc_from_utc_str(x):
  return datetime.strptime(x, '%Y/%m/%d %H:%M:%S+00')

def format_phone(x):
  digits = re.sub(r'\D', '', x)
  return '{}-{}-{}'.format(digits[:3], digits[3:6], digits[6:])
