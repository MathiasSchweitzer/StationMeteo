import sqlite3
import os

def init():
    if not os.path.isfile("data.db"):
        print("Création db")
        conn = sqlite3.connect("data.db")
        with open("tables.sql") as file:
            conn.execute(file.read())
        conn.commit()
        print(conn.execute("SELECT name FROM sys.tables").fetchall())
        conn.close()