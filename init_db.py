import sqlite3
import os

def init():
    if not os.path.isfile("data.db"):
        conn = sqlite3.connect("data.db")
        with open("tables.sql") as file:
            conn.execute(file.read())
        conn.commit()
        conn.close()