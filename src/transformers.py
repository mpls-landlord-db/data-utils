import re
from datetime import datetime

class Transform:

  @classmethod
  def timestamp_to_utc_date(cls, ts):
    return datetime.utcfromtimestamp(int(ts) / 1000).strftime('%Y-%m%d %H:%M:S')

  @classmethod
  def utc_str_to_utc_date(cls, date_str):
    return datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S+00')

  @classmethod
  def hyphenate_phone_number(cls, phone):
    digits = re.sub(r'\D', '', phone)
    return '{}-{}-{}'.format(digits[:3], digits[3:6], digits[6:])
