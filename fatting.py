import os
from dotenv import load_dotenv
import threading
import time
import psycopg2

#  connect Database
load_dotenv()
# update connection string information
host = os.getenv('HOST')
dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
sslmode = os.getenv('SSLMODE')
print(u)
conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
conn = psycopg2.connect(conn_string)

cur = conn.cursor()
cur.execute("select * from information_schema.tables where table_name=%s", ('movie',))
if not bool(cur.rowcount):
  cur.execute("CREATE TABLE movie (id serial PRIMARY KEY, header VARCHAR(100), link VARCHAR(100), runtime VARCHAR(50), type VARCHAR(100));")
  print("Finished creating table")
# Insert some data into the table
# cur.execute("INSERT INTO movie (header, link, runtime, type) VALUES (%s, %s, %s, %s);", ("banana", 150))


# 子執行緒的工作函數
def job():
  for i in range(5000):
    # print("Child thread:", i)
    # Insert some data into the table
    cur.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", i))
    # time.sleep(1)

# 建立一個子執行緒
t = threading.Thread(target = job)
# 執行該子執行緒
t.start()
# 等待 t 這個子執行緒結束
t.join()

# Clean up
conn.commit()
cur.close()
conn.close()

print("Done.")