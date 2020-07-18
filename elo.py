import sqlite3
import config

conn = sqlite3.connect(config.ELO_CONN)

# k-factor most accurate rating is a global 32 which is adjusted according to elo bracket
k = 32
DEFAULT_ELO = 1400


def get_new_elo(usr, opp, result, game):
    add_new_user(usr, opp, game)

    c = conn.cursor()
    c.execute("SELECT elo FROM {} WHERE player = '{}'".format(game, usr))
    usr_elo = c.fetchone()[0]
    c.execute("SELECT elo FROM {} WHERE player = '{}'".format(game, usr))
    opp_elo = c.fetchone()[0]

    usr_prob = get_usr_probability(usr_elo, opp_elo)
    opp_prob = get_opp_probability(opp_elo, usr_elo)

    new_elo = calculate_elo(usr_elo, opp_elo, usr_prob, opp_prob, result)
    update_elo(usr, opp, new_elo, game)


def add_new_user(usr, opp, game):
    c = conn.cursor()
    c.execute("INSERT or IGNORE INTO {} (player, elo) VALUES ('{}', {})".format(game, usr, DEFAULT_ELO))
    c.execute("INSERT or IGNORE INTO {} (player, elo) VALUES ('{}', {})".format(game, opp, DEFAULT_ELO))


def get_usr_probability(usr_rating, opp_rating):
    # probability of user (player1) to win
    p = (1.0 / (1.0 + pow(10, ((opp_rating - usr_rating) / 400))))
    return p


def get_opp_probability(opp_rating, usr_rating):
    # probability of opponent (player2) to win
    p = (1.0 / (1.0 + pow(10, ((usr_rating - opp_rating) / 400))))
    return p


def calculate_elo(usr_rating, opp_rating, usr_prob, opp_prob, result):
    # TODO: remove duplication here
    print("old_usr_rating = {}, old_opp_rating = {}".format(usr_rating, opp_rating))
    if result == 1:
        usr_rating = usr_rating + k * (1 - usr_prob)
        print("new_usr_rating = {}".format(usr_rating))
        opp_rating = opp_rating + k * (0 - opp_prob)
        print("new_opp_rating = {}".format(opp_rating))
    elif result == 0:
        usr_rating = usr_rating + k * (0 - usr_prob)
        print("new_usr_rating = {}".format(usr_rating))
        opp_rating = opp_rating + k * (1 - opp_prob)
        print("new_opp_rating = {}".format(opp_rating))
    else:
        print("error")

    return [usr_rating, opp_rating]


def update_elo(usr, opp, new_elo, game):
    c = conn.cursor()
    c.execute("UPDATE {} SET `elo`={} WHERE player='{}';".format(game, new_elo[0], usr))
    c.execute("UPDATE {} SET `elo`={} WHERE player='{}';".format(game, new_elo[1], opp))
    conn.commit()


def main(usr, opp, result, game):
    # for result, 1 = win and 0 = lose. This is important as it affects the formula (result - usr_prob)
    return get_new_elo(usr, opp, result, game)


if __name__ == "__main__":
    main()

