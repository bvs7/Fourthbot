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
    raw_data = data.handler.read('Character Chart!A2:G13')
    msg = '```'
    for character in raw_data:
        if author == character[0] or author in data.dms and character[0] is not 'Player':
            if not specific_flag or character[1].lower() in specific_char:
                msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(character[1],
                                                character[4],character[5],character[6])
    msg = msg + '```'
    if msg == '``````':
        msg = 'No characters found, please check your spelling! :clap:'
    await data.client.send_message(message.channel,msg)

async def current(data,message):
    words = message.content.split()
    ## Check if a specific character name is selected
    specific_flag = False
    specific_char = ''
    if len(words) >= 2:
        specific_flag = True
        specific_char = words[1]
    author_id = message.author.id
    author = data.users[author_id]
    raw_data = data.handler.read('Character Chart!A:G')
    with open('config/current_characters.json','r') as current_file:
        current = json.load(current_file)
    msg = ''
    if specific_flag == True:
        for character in raw_data:
            if author == character[0] and specific_char == character[1]: # set current character
                current[author] = specific_char
                msg =       'I set your current character as \n'
                msg = msg + '```{:10}{:5} XP Level {:3}({:5} XP to next level)```'.format(
                            character[1],character[4],character[5],character[6])
                with open('config/current_characters.json','w') as current_file:
                    json.dump(current,current_file)
        if msg == '': # For when character name is wrong
            msg = 'I didn\'t recognize the character you listed.  Here are your current characters:\n```'
            for character in raw_data:
                if author == character[0]:
                    msg = msg + '{:10}'
            msg = msg + '```\nUse **!current (character)** to switch characters.'
            msg = msg + 'Be sure to use proper capitalization.'
    elif author in data.dms:
        msg = msg + 'Current Characters:\n```'
        for player in current:
            msg = msg + '{:10}:{:10}\n'.format(player,current[player])
        msg = msg +'```'
    else:
        msg = 'Your current character is\n```{:10}```\n'.format(current[author]) 
        msg = msg + 'To switch to a different character use **!current (character)**'
    await data.client.send_message(message.channel,msg)

async def bank(data,message):
    words = message.content.split()
    author_id = message.author.id
    author = data.users[author_id]
    if len(words) == 1: # Simple call
        raw_data = data.handler.read('Bank Chart!A:C')
        if not author in data.dms:
            for player in raw_data:
                if player[0] == author:
                    msg = 'You currently have **{}** banked xp\n'.format(str(player[1]))
                    msg = msg +'To spend xp use **!bank (character) (amount) confirm**'
        else:
            msg = 'Players\' banked xp:\n```'
            for player in raw_data:
                msg = msg + '{:8}:{:4}\n'.format(player[0],str(player[1]))
            msg = msg +'```'
    else: # call to change values 
        character_flag = False
        spend_flag = False
        confirm_flag = False
        raw_data = data.handler.read('Character Chart!A:B')
        characters = set() ### Creating list of potential characters
        for character in raw_data:
            if author == character[0]:
                characters.add(character[1])
        raw_data = data.handler.read('Bank Chart!A:B')
        for player in raw_data:
            if author == player[0]:
                max_spend = int(player[1])
        for word in words[1:]:
            if word in characters and not character_flag:
                character = word
                character_flag = True
            if word.isdigit() and int(word) <= max_spend and not spend_flag:
                spend = word
                spend_flag = True
            if word == 'Confirm' or word == 'confirm':
                confirm_flag = True
        if not character_flag:
            msg = "I didn't recognize which character you want to spend on.  Use !xp if you forget your character names."
        elif not spend_flag:
            msg = "I didn't recognize a number of points to spend.  Don't use anything but numbers for that."
        elif not confirm_flag:
            msg = "Enter the same command, with \"Confirm\" after it in order to confirm your spending"
        else: #Date,Author,Player,Character,Debits,Credits #Delta
            data.handler.append('Bank Tracker!A:G',[[str(datetime.date.today()),author,author,character,'0', spend,'-'+spend]])
            msg = "Confirmed! {} gained {} xp!".format(character,str(spend))
    await data.client.send_message(message.channel,msg)


async def session(data,message):
    words = message.content.split()
    author_id = message.author.id
    author = data.users[author_id]
    if len(words) == 1: # Help call
        msg = """DMs can use this command in order to award session xp. Any awarded XP will show up in the #announcements tab"""
    else:
        if not author in data.dms:
            msg = """Sorry kid.  You have to be running the game to use this command."""
        else:
            session_data = []
            points = words[1]
            msg = "The following characters have been awarded {} xp for a session\n```".format(points)
            with open('config/current_characters.json','r') as current_file:
                current = json.load(current_file)
                for player in current:
                    session_data.append([str(datetime.date.today()),author, player,current[player],points])
                    msg = msg + "{:10}\n".format(current[player])
                msg = msg+'```'
            data.handler.append('Session Tracker!A:E',session_data)
    await data.client.send_message(message.channel,msg)

async def bonus(data,message):
    words = message.content.split()
    author_id = message.author.id
    author = data.users[author_id]
    if author not in data.dms:
        msg = """Sorry kid.  You have to be running the game to use this command."""
    else:
        player_flag = False
        number_flag = False
        with open('config/character_chats.json','r') as cc_file:
            chats = json.load(cc_file)
            if str(message.channel.id) in chats:
                player_flag = True
                player = chats[str(message.channel.id)]
            if words[1].isdigit():
                number_flag = True
                number = int(words[1])
        
        if not player_flag or not number_flag:
            msg = "No xp awarded because message did not parse correctly."
        else:
            session_data = [[str(datetime.date.today()),author,player,"",str(number),"0",str(number)]]
            data.handler.append('Bank Tracker!A:G',session_data)
            msg = "{} awarded {} {} bonus xp.  Congrats!".format(author,player,str(number))
    await data.client.send_message(message.channel,msg)


            


if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    G = googleHandler.googleHandler('1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo')
    D = discordHandler.discordHandler('config/discord.json',G)

    D.add_command('roll',roll,'Roll Dice')
    D.add_command('oof',oof,'For those oofs that are bound to happen.')
    D.add_command('xp',xp,'List your character\'s xp totals')
    D.add_command('current',current,'Check or change your current character')
    D.add_command('bank',bank,'Check or use your banked bonus xp')
    D.add_command('session',session,'DMS ONLY: Add session xp')
    D.add_command('bonus',bonus,'DMS ONLY: Add bonus xp')

    D.run()
