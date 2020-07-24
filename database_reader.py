import sqlite3


def pull_all_elo(game):
    conn = sqlite3.connect("elo.db")
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(game))
    rows = c.fetchall()
    return rows
