import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con

def query(sql, params=None):
    con = get_connection()
    cur = con.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    return rows

def execute(sql, params=None):
    con = get_connection()
    cur = con.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    con.commit()
    last_id = cur.lastrowid
    con.close()
    return last_id