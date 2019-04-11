import googleHandler
import discordHandler


import random
import datetime
import re
import json
## Discord Bot Commands
async def roll(data,message):
    words = message.content.split()
    msg = ("Roll dice how you would see the dice written\n"
            "Examples: **!roll d20** : roll 1 d20\n"
            "**!roll 8d6** : roll 8 d6s \n"
            "**!roll 1d20 2d12 3d8**")
    if len(words) == 1:
        await data.client.send_message(message.channel,msg)
    output = []
    for die in words[1:]:
        matchObj = re.match(r'(\d*)d(\d+)', die)
        if matchObj == None: continue
        if matchObj.group(1) == '':
            quantity = 1
        else:
            quantity = int(matchObj.group(1))
        if quantity > 100: quantity = 100
        die_size = int(matchObj.group(2))
        if die_size < 2: die_size = 1
        if die_size > 100: die_size = 100
        rolls = []
        for i in range(quantity):
            rolls.append(random.randint(1,die_size))
        output.append(rolls)
        sum_rolls = 0
    for values in output:
        sum_rolls = sum_rolls + sum(values)
    msg = str(output) + ' : ' + str(sum_rolls)
    await data.client.send_message(message.channel,msg)

async def oof(data,message):
    msg = ("Big oof my dudes.")
    await data.client.send_message(message.channel,msg)

async def xp(data,message):
    words = message.content.split()
    specific_flag = False
    specific_char = []
    if len(words) >= 2:
        specific_flag = True
        for character in words[1:]:
            specific_char.append(character.lower())
    # Figure out who sent the message
    author_id = message.author.id
    author = data.users[author_id]
    dms = ['Chris','Brian','Tommy']
    raw_data = data.handler.read('Character Chart!A2:E11')
    msg = '```'
    for character in raw_data:
        if author == character[0] or author in dms:
            if not specific_flag or character[1].lower() in specific_char:
                msg = msg + '{:12}{:5} XP Level {:3}({:5} XP to next level)\n'.format(character[1],
                                                character[2],character[3],character[4])
    msg = msg + '```'
    if msg == '``````':
        msg = 'No characters found, please check your spelling! :clap:'
    await data.client.send_message(message.channel,msg)

if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    G = googleHandler.googleHandler('1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo')
    D = discordHandler.discordHandler('config/discord.json',G)

    D.add_command('roll',roll,'Roll Dice')
    D.add_command('oof',oof,'For those oofs that are bound to happen.')
    D.add_command('xp',xp,'Still under development')

    D.run()
