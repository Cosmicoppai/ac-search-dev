import csv
import os
import lzma
import psycopg2
import psycopg2.extras
import dotenv
from datetime import datetime as dt




class CreateTrigger:
    def __init__(self):
        dotenv.read_dotenv('.env')
        self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))
        self.cur = self.conn.cursor()
        self.cur.execute("ALTER TABLE app_post ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce('title', '') || ' ' || coalesce(text,''))) STORED")
        self.cur.execute("CREATE INDEX ts_post_idx ON app_post USING GIN (ts)")
        self.cur.execute("ALTER TABLE app_comment ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('english', text)) STORED")
        self.cur.execute("CREATE INDEX ts_comm_idx ON app_comment USING GIN (ts)")
        self.conn.commit()



class batch_insert:
    def __init__(self):
        self.rows = []
        dotenv.read_dotenv('.env')
        self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))
        self.cur = self.conn.cursor()
        self.ins = 0

    def add_row(self, row):
        self.rows.append(row)
        if len(self.rows) >= 1000:
            self.do_insert()

    def do_insert(self):
        # print(f"Inserting {len(self.rows)} / {self.ins}...")
        psycopg2.extras.execute_values(self.cur, "INSERT INTO app_post (post_id, title, text, username, sub, upvotes, create_date) VALUES %s", self.rows)
        self.conn.commit()
        self.rows.clear()
        self.ins += 1


def create_new():
    sql = batch_insert()
    with open("one-million-reddit-confessions.csv", mode="rt", encoding='utf8') as csv_file:
        data = csv.DictReader(csv_file)
        for obj in data:
            if obj['selftext'] == '[deleted]' or obj['selftext'] == '[removed]':
                continue
            sql.add_row((obj['id'], obj['title'], obj['selftext'], 'ShadowGuy', 'cryptocurrency', obj['score'], dt.now()))
    sql.do_insert()



if __name__ == "__main__":
    CreateTrigger()
    create_new()