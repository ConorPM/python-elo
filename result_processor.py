import sqlite3
from elo import Elo

results_database = "results.db"


class ResultProcessor:
    def __init__(self, game, user, opponent, user_score, opponent_score):
        self.game = game
        self.user = user
        self.opponent = opponent
        self.user_score = user_score
        self.opponent_score = opponent_score
        self.winner = ""
        self.loser = ""
        self.winner_score = int
        self.loser_score = int
        return

    def get_and_set_result(self):
        if self.user_score > self.opponent_score:
            self.winner = self.user
            self.loser = self.opponent
            self.winner_score, self.loser_score = self.user_score, self.opponent_score

        elif self.user_score < self.opponent_score:
            self.winner = self.opponent
            self.loser = self.user
            self.loser_score, self.winner_score = self.user_score, self.opponent_score

        else:
            raise Exception("Invalid score")

        result = "{} beat {} {}-{} in {}".format(
            self.winner, self.loser, self.user_score, self.opponent_score, self.game
        )

        self.add_to_sqlite()

        return result

    def add_to_sqlite(self):
        conn = sqlite3.connect(results_database)
        self.create_sqlite()
        c = conn.cursor()
        if self.winner and self.loser != "":
            c.execute("""INSERT INTO {} ('winner', 'loser', 'winner_score', 'loser_score')
                            VALUES (?, ?, ?, ?);""".format(self.game),
                      (
                          self.winner, self.loser, self.winner_score, self.loser_score
                      )
                      )

            conn.commit()
            conn.close()
            elo = Elo(self.winner, self.loser, self.game)
            elo.get_new_elo()

    def create_sqlite(self):
        conn = sqlite3.connect(results_database)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS {}
              (winner text, loser text, winner_score int, loser_score int)'''.format(self.game))
        conn.commit()
        conn.close()