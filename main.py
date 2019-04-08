import googleHandler
import discordHandler


import random
import datetime
import re
## Discord Bot Commands
async def roll(client,message,words):
    msg = ("Roll dice how you would see the dice written\n"
            "Examples: **!roll d20** : roll 1 d20\n"
            "**!roll 8d6** : roll 8 d6s \n"
            "**!roll 1d20 2d12 3d8**")
    if len(words) == 1:
        await client.send_message(message.channel,msg)
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
    await client.send_message(message.channel,msg)

async def oof(client, message, words):
    msg = ("Big oof my dudes.")
    await client.send_message(message.channel,msg)

if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    D = discordHandler.discordHandler('config/discord.json')
    D.add_command('roll',roll,'Roll Dice')
    D.add_command('oof',oof,'For those oofs that are bound to happen.')
    D.run()
