import psycopg2


class DB:
    def __init__(self, host, uuid, dbname, password):

        conn_string = "host={0} user={1} dbname={2} password={3}".format(host, uuid, dbname, password)
        self.conn = psycopg2.connect(conn_string)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute("select * from information_schema.tables where table_name=%s", ('movies',))
        if not bool(self.cur.rowcount):
            print("create table")
            self.cur.execute("CREATE TABLE movies (id serial PRIMARY KEY, title VARCHAR(500), link VARCHAR(500), runtime VARCHAR(500), type VARCHAR(500), imdb_id VARCHAR(500), poster VARCHAR(500), trailer VARCHAR(500), actors VARCHAR(500), characters VARCHAR(500), storyline VARCHAR(500));")
        print("Finished creating table")

            
    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()

# def db(host, uuid, dbname, password):
#     conn_string = "host={0} user={1} dbname={2} password={3}".format(host, uuid, dbname, password)
#     conn = psycopg2.connect(conn_string)

    
#     cur = conn.cursor()
#     cur.execute("select * from information_schema.tables where table_name=%s", ('movie',))
#     if not bool(cur.rowcount):
#         cur.execute("CREATE TABLE movie (id serial PRIMARY KEY, header VARCHAR(100), link VARCHAR(100), runtime VARCHAR(50), type VARCHAR(100));")
#     print("Finished creating table")

#     return cur