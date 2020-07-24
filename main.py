import discord
import sqlite3
import re

import elo
import config
import result_processor

TOKEN = config.TOKEN

client = discord.Client()

@client.event
async def on_message(message):
    # checks the bots own messages and sets up the reaction verification
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
            rp = result_processor.ResultProcessor(message.author, opp, message.content)
            rp.get_and_set_result()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def main():
    client.run(TOKEN)
    return 0

if __name__ =="__main__":
    main()
