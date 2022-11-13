import sqlite3 as db


DB_FILE = 'db/db.db'


def execute(query):
    try:
        con = db.connect(DB_FILE)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
    except db.Error:
        pass


def evaluate(query):
    try:
        con = db.connect(DB_FILE)
        cur = con.cursor()
        res = cur.execute(query).fetchall()
        return res
    except db.Error:
        return None
