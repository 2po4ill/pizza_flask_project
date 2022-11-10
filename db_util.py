import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="pizza_shop",
            user="postgres",
            password="Init123#",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    def select(self, what, table, query):
        self.cur.execute(f'SELECT {what} FROM {table} {query};')
        return self.cur.fetchall()

    def insert(self, table, query):
        self.cur.execute(f'INSERT INTO {table} VALUES({query});')
        self.con.commit()

