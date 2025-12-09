import csv
import io
import sqlite3
from pprint import pprint

conn = sqlite3.connect("elog.db")
cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS event (
      etime DATETIME
      category INT
      description TEXT
  )
""")
