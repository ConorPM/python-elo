import sqlite3

conn = sqlite3.connect("elo.db")


def pull_all_elo(game):
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(game))
    rows = c.fetchall()
    return rows
