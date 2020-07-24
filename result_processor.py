import sqlite3
import config
from elo import Elo

class ResultProcessor:
    def __init__(self, author, opp, content):
        self.author = author
        self.opp = opp
        self.content = content
        self.msg = ""
        self.usr = ""
        self.usr_score = 0
        self.opp_score = 0
        self.game = ""
        return

    def get_and_set_result(self):
        self.msg = self.content.split(" ")
        self.usr = '<@{}>'.format(self.author)
        self.opp = '<@{}>'.format(self.opp)
        self.game = self.msg[1]
        self.usr_score = self.msg[3]
        self.opp_score = self.msg[4]

        if self.usr_score > self.opp_score:
            result = "{} beat {} {}-{} in {}".format(self.usr, self.opp, self.usr_score, self.opp_score, self.game)
        elif self.opp_score > self.usr_score:
            result = "{} beat {} {}-{} in {}".format(self.opp, self.usr, self.opp_score, self.usr_score, self.game)
        else:
            result = None

        self.add_to_sqlite()

        return result

    def add_to_sqlite(self):
        conn = sqlite3.connect(config.DB_CONN)
        self.create_sqlite()
        # 1 = Win 0 - Loss
        c = conn.cursor()
        if self.usr_score > self.opp_score:
            result = 1
        elif self.opp_score > self.usr_score:
            result = 0
        else:
            result = None

        c.execute("""INSERT INTO {} ('player', 'opponent', 'usr_score', 'opp_score', 'result')
                VALUES (?, ?, ?, ?, ?);""".format(self.game),
                (
                    self.usr, self.opp, self.usr_score, self.opp_score, result
                )
                )

        conn.commit()
        elo = Elo(self.usr, self.opp, result, self.game)
        elo.get_new_elo()

    def create_sqlite(self):
        conn = sqlite3.connect(config.DB_CONN)
        c = conn.cursor()
        print("creating table...")
        c.execute('''CREATE TABLE IF NOT EXISTS {}
              (player text, opponent text, usr_score int, opp_score int, result int)'''.format(self.game))
        conn.commit()
