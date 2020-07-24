import sqlite3

# The most accurate and widely used k-factor rating is 32
k = 32
DEFAULT_ELO = 1400

elo_database = "elo.db"


class Elo:   
    def __init__(self, winner, loser, game):
        self.winner = winner
        self.loser = loser
        self.game = game

    def get_new_elo(self):
        self.create_sqlite()
        self.add_new_user()
        conn = sqlite3.connect(elo_database)
        c = conn.cursor()
        c.execute("SELECT elo FROM {} WHERE player = '{}'".format(self.game, self.winner))
        winner_elo = c.fetchone()[0]
        c.execute("SELECT elo FROM {} WHERE player = '{}'".format(self.game, self.loser))
        loser_elo = c.fetchone()[0]
        conn.close()

        winner_prob = self.get_winner_probability(winner_elo, loser_elo)
        loser_prob = self.get_loser_probability(loser_elo, winner_elo)

        new_elo = self.calculate_elo(winner_elo, loser_elo, winner_prob, loser_prob)
        self.update_elo(new_elo)

    def add_new_user(self):
        conn = sqlite3.connect(elo_database)
        c = conn.cursor()
        c.execute("INSERT or IGNORE INTO {} (player, elo) VALUES ('{}', {})".format(self.game, self.winner, DEFAULT_ELO))
        c.execute("INSERT or IGNORE INTO {} (player, elo) VALUES ('{}', {})".format(self.game, self.loser, DEFAULT_ELO))
        conn.close()

    def get_winner_probability(self, winner_rating, loser_rating):
        p = (1.0 / (1.0 + pow(10, ((loser_rating - winner_rating) / 400))))
        return p

    def get_loser_probability(self, loser_rating, winner_rating):
        p = (1.0 / (1.0 + pow(10, ((winner_rating - loser_rating) / 400))))
        return p

    def calculate_elo(self, winner_rating, loser_rating, usr_prob, opp_prob):
        winner_rating = winner_rating + k * (1 - usr_prob)
        print("{}'s new rating = {}".format(self.winner, winner_rating))
        loser_rating = loser_rating + k * (0 - opp_prob)
        print("{}'s new rating = {}".format(self.loser, loser_rating))

        return [winner_rating, loser_rating]

    def update_elo(self, new_elo):
        conn = sqlite3.connect(elo_database)
        c = conn.cursor()
        c.execute("UPDATE {} SET `elo`={} WHERE player='{}';".format(self.game, new_elo[0], self.winner))
        c.execute("UPDATE {} SET `elo`={} WHERE player='{}';".format(self.game, new_elo[1], self.loser))
        conn.commit()
        conn.close()

    def create_sqlite(self):
        conn = sqlite3.connect(elo_database)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS {}
            (player text, elo int)'''.format(self.game))
        conn.commit()
        conn.close()
