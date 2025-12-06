import sqlite3

main_db = r"finance.db"

de_dbf = r"directexpress/test.db"
ne_dbf = r"netspend/test.db"

conn = sqlite3.connect(main_db)

cursor = conn.cursor()

conn.execute(
    """
    DROP TABLE IF EXISTS transactions;
"""
)

cursor.execute(
    """
CREATE TABLE [transactions](
  [day] DATE,
  [asset] INT,
  [entity] INT,
  [description] TEXT, 
  [amount] CURRENCY);
"""
)

cursor.execute("ATTACH '" + de_dbf + "' AS de_db;")
cursor.execute("ATTACH '" + ne_dbf + "' AS ne_db;")

conn.commit()

cursor.execute(
    """
    INSERT INTO transactions (day, asset, description, amount)
        SELECT day, asset, description, amount FROM de_db.transactions
        UNION ALL
        SELECT day, asset, description, amount FROM ne_db.transactions order by day;
        """
)

conn.commit()
conn.close()
