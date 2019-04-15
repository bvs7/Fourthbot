# discordHandler.py
# Author: Sc4ry
# Functionality:
# adds discordHandler, which 

import sys
import os
import json
import discord
import re

import random     
import datetime  

class Data:
    def __init__(self,client,handler,users):
        self.client = client
        self.handler = handler
        self.users = users
        self.dms = ['Chris','Brian','Tommy']

class discordHandler:
    def __init__(self, config_filename,handler):
        self.init_config(config_filename) # Get config data for Discord connection
        self.init_log() # Initialize logging system
        self.init_commands() # Set basic commands up
        self.init_remember_users() # Recall user data
        self.client = discord.Client() # Create client
        self.data = Data(self.client, handler, self.users) #For passing into functions
        self.init_client()
    def init_config(self, config_filename):
        if not os.path.exists(config_filename):
            print("Config File not found.")
            return
        else:
            with open(config_filename,'rb') as config_file:
                self.config = json.load(config_file)
    def init_log(self):
        if os.path.exists('config/log.txt'):
            self.log = open('config/log.txt','a')
        else:
            self.log = open('config/log.txt','w')
    def init_commands(self):
        # Create empty command dictionary
        self.commands = dict()
        # Each command includes a function reference and a description
        self.commands['hi'] = [self.say_hello, 'Say hi!']
        self.commands['about'] = [self.about, 'Get basic information about bot']
        self.commands['help'] = [self.help, 'Check bot\'s current commands']
    def init_client(self):
        @self.client.event
        async def on_ready():
            print(self.client.user.name + ' is now online!')
            print(self.client.user.name + ' is now online!', file=self.log,flush=True)

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            else:
                await self.parse(message)
    def init_remember_users(self):
        with open('config/users.json','r') as users_file:
            self.users = json.load(users_file)
    def run(self):
        self.client.run(self.config['token'])

    def add_command(self, command, command_function, command_description):
        self.commands[command] = [command_function,command_description]

    async def parse(self, message):
        if not message.content.startswith(self.config['prefix']): return
        words = message.content.split()
        command = words[0]
        if len(command) == 1: return # No command
        if not command[1:] in self.commands: return
        parse_func = self.commands[command[1:]][0]
        print('Command:',command[1:] ,':from',message.author.name)
        print('Command:',command[1:] ,':from',message.author.name,file=self.log,flush=True) 
        await parse_func(self.data,message)

    # Basic command functions
    async def say_hello(self,data,message):
        msg = 'Hello {0.author.mention}'.format(message)
        print('Response: ', msg)
        print('Response: ', msg, file=self.log,flush=True)
        await self.client.send_message(message.channel,msg)
    async def about(self,data,message):
        msg = ("I am FourthBot v1.1.  I act as the 4th DM for the group.  You can ask "
            "me lots of things or use me to roll dice through discord, or use me to "
            "keep track of your characters, experience, and treasure.  I am not "
            "finished yet though!  Use !help to see all of my current commands.")
        print('Response: About message')
        print('Response: About message',file=self.log,flush=True)
        await self.client.send_message(message.channel,msg)
    async def help(self,data,message):
        words = message.content.split()
        if len(words)==1:
            msg = "Here is an updated list of commands: \n"
            for key in self.commands:
                next_line = '  **!' +key+'**: '+self.commands[key][1]+'\n'
                msg = msg + next_line
            msg = msg + "Use **!help command** (ie. **hi**) to learn more about specific commands"
            print('Response: Help message')
            print('Response: Help message',file=self.log,flush=True)
        else:
            if words[1] == 'hi':
                msg = ("Use **!hi** to say hello to FourthBot. This command is useful"
                        " for checking if the bot is currently on, or if you are lonely"
                        " and just want someone to say hello to you <3")
            elif words[1] == 'about':
                msg = ("Use **!about** to learn more about what FourthBot is designed "
                        "to do.  As the program changes, the about command will change "
                        "so you can keep up with major changes!")
            elif words[1] == 'help':
                msg = ("Dude.  You're already using help... but use **!help (command)** "
                        "to learn about new commands ")
            elif words[1] == 'roll':
                msg = ("Use **!roll** to roll dice.\n"
                        "You can roll any die of any size from 2-100, and you can roll "
                        "any number of dice. The number before the d says how many dice "
                        "you want to roll, and the number after the d says what size "
                        "die you want to use.\n\n"
                        "Example: 2d20 = Roll 2 d20's \n\n"
                        "You can also roll multiple different dice by using multiple commands "
                        "at once. \n\n"
                        "Example: d20 5d6 2d7 = roll 1 d20, 5 d6s, and 2 d7s\n\n"
                        "The number at the end of the numbers is the sum of the numbers.")
            elif words[1] == 'xp':
                msg = ("Use **!xp** to check your characters' current xp totals.  "
                        "If you only want to see xp for a single character, use **!xp (character)**")
            elif words[1] == 'current':
                msg = ("Use **!current** to check who your current character is.  Your current "
                        "character is the one that you use during sessions, and the one that "
                        "will be awarded session xp.  To change your current character, use "
                        "**!current (character)**.")
            elif words[1] == 'bank':
                msg = ("Use **!bank** to check how many bonus xp you have banked.  You can also "
                        " use **!bank (character) (xp to spend) confirm** to spend your xp points "
                        "on a specific character.  You cannot spend more points than you have avaliable to you.")
            elif words[1] == 'session':
                msg = ("Don't use **!session** unless you are a DM entering session xp from the last session."
                        " If you are a DM, you can use **!session (amount of xp)** to award all current "
                        "characters xp for the current session.")
        await self.client.send_message(message.channel,msg)


async def roll(data,message):
    words = message.content.split()
    if len(words) == 1:
        msg = ("Roll dice how you would see the dice written\n"
                "Examples: **!roll d20** : roll 1 d20\n"
                "**!roll 8d6** : roll 8 d6s \n"
                "**!roll 1d20 2d12 3d8**")
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
        if die_size < 2: die_size = 2
        if die_size > 100: die_size = 100
        rolls = []
        for i in range(quantity):
            rolls.append(random.randint(1,die_size))
        output.append(rolls)
    
    await data.client.send_message(message.channel,str(output))
        
        


if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    D = discordHandler('config/discord.json',[])
    D.add_command('roll', roll, 'Roll Dice')
    D.run()