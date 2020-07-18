import discord
import sqlite3
import re

import elo
import config

TOKEN = config.TOKEN

client = discord.Client()
conn = sqlite3.connect(config.DB_CONN)

@client.event
async def on_message(message):
    if message.author == client.user:
        if message.content == 'React with thumbs up for correct or thumbs down for false.':
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        return

    if message.content.startswith('!report'):
        # desired format = !report melee @CPM 2 0
        opp_id = message.mentions[0].id
        opp = client.get_user(opp_id)
        await message.channel.send('React with thumbs up for correct or thumbs down for false.')

        reaction, user = await client.wait_for('reaction_add', check=lambda r, u: u.id == opp_id)
        await message.channel.send('{} reacted with {}!'.format(opp.mention, reaction))

        if reaction.emoji == "👍":
            print("Updating database with result")
            await message.channel.send("Updating database with result!")
            get_result(message.author, opp, message.content)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def get_result(author, opp, content):
    msg = content.split(" ")
    usr = '<@{}>'.format(author)
    opp = '<@{}>'.format(opp)
    game = msg[1]
    usr_score = msg[3]
    opp_score = msg[4]

    if usr_score > opp_score:
        result = "{} beat {} {}-{} in {}".format(usr, opp, usr_score, opp_score, game)
    elif opp_score > usr_score:
        result = "{} beat {} {}-{} in {}".format(opp, usr, opp_score, usr_score, game)
    else:
        result = None

    add_to_sqlite(usr, opp, usr_score, opp_score, game)

    return result


def create_sqlite(game):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS {}
              (player text, opponent text, usr_score int, opp_score int, result int)'''.format(game))
    conn.commit()


def add_to_sqlite(usr, opp, usr_score, opp_score, game):
    create_sqlite(game)
    # 1 = Win 0 - Loss
    c = conn.cursor()
    if usr_score > opp_score:
        result = 1
    elif opp_score > usr_score:
        result = 0
    else:
        result = None

    c.execute("""INSERT INTO {} ('player', 'opponent', 'usr_score', 'opp_score', 'result')
              VALUES (?, ?, ?, ?, ?);""".format(game),
              (
                  usr, opp, usr_score, opp_score, result
              )
              )

    conn.commit()
    elo.get_new_elo(usr, opp, result, game)

def main():
    client.run(TOKEN)
    return 0

if __name__ =="__main__":
    main()