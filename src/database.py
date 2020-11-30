import psycopg2

class Database:
  def __init__(self, database_url=''):
    self.database_url = database_url

  def _connect(self):
    return psycopg2.connect(dsn=self.database_url)

  def execute(self, sql='', params=[]):
    with self._connect() as conn:
      with conn.cursor() as cur:
        cur.execute(sql, params)

  def execute_many(self, sql, rows=[]):
    with self._connect() as conn:
      with conn.cursor() as cur:
        for row in rows:
          cur.execute(sql, row)