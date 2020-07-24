import sqlite3
import config

# The most accurate and widely used k-factor rating is 32
k = 32
DEFAULT_ELO = 1400
conn = sqlite3.connect(config.ELO_CONN)

class Elo:   
    def __init__(self, usr, opp, result, game):
        self.usr = usr
        self.opp = opp
        self.result = result
        self.game = game

    def get_new_elo(self):
        self.create_sqlite()
        self.add_new_user()

        c = conn.cursor()
        c.execute("SELECT elo FROM {} WHERE player = '{}'".format(self.game, self.usr))
        usr_elo = c.fetchone()[0]
        c.execute("SELECT elo FROM {} WHERE player = '{}'".format(self.game, self.usr))
        opp_elo = c.fetchone()[0]

        usr_prob = self.get_usr_probability(usr_elo, opp_elo)
        opp_prob = self.get_opp_probability(opp_elo, usr_elo)

        new_elo = self.calculate_elo(usr_elo, opp_elo, usr_prob, opp_prob)
        self.update_elo(new_elo)


    def add_new_user(self):
        c = conn.cursor()
        c.execute("INSERT or IGNORE INTO {} (player, elo) VALUES ('{}', {})".format(self.game, self.usr, DEFAULT_ELO))
        c.execute("INSERT or IGNORE INTO {} (player, elo) VALUES ('{}', {})".format(self.game, self.opp, DEFAULT_ELO))


    def get_usr_probability(self, usr_rating, opp_rating):
        # probability of user (player1) to win
        p = (1.0 / (1.0 + pow(10, ((opp_rating - usr_rating) / 400))))
        return p


    def get_opp_probability(self, opp_rating, usr_rating):
        # probability of opponent (player2) to win
        p = (1.0 / (1.0 + pow(10, ((usr_rating - opp_rating) / 400))))
        return p


    def calculate_elo(self, usr_rating, opp_rating, usr_prob, opp_prob):
        # TODO: remove duplication here
        print("old_usr_rating = {}, old_opp_rating = {}".format(usr_rating, opp_rating))
        if self.result == 1:
            usr_rating = usr_rating + k * (1 - usr_prob)
            print("new_usr_rating = {}".format(usr_rating))
            opp_rating = opp_rating + k * (0 - opp_prob)
            print("new_opp_rating = {}".format(opp_rating))
        elif self.result == 0:
            usr_rating = usr_rating + k * (0 - usr_prob)
            print("new_usr_rating = {}".format(usr_rating))
            opp_rating = opp_rating + k * (1 - opp_prob)
            print("new_opp_rating = {}".format(opp_rating))
        else:
            print("error")

        return [usr_rating, opp_rating]


    def update_elo(self, new_elo):
        c = conn.cursor()
        c.execute("UPDATE {} SET `elo`={} WHERE player='{}';".format(self.game, new_elo[0], self.usr))
        c.execute("UPDATE {} SET `elo`={} WHERE player='{}';".format(self.game, new_elo[1], self.opp))
        conn.commit()

    def create_sqlite(self):
            # conn = sqlite3.connect(config.ELO_CONN)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS {}
                (player text, elo int)'''.format(self.game))
            conn.commit()
