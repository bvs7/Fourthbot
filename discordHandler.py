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


class discordHandler:
    def __init__(self, config_filename):
        # Load in config file
        self.init_config(config_filename)
        # Initialize Log
        self.init_log()
        # Create basic commands
        self.init_commands()
        # Create Client
        self.client = discord.Client()
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
        await parse_func(self.client,message,words)

    # Basic command functions
    async def say_hello(self,client,message,words):
        msg = 'Hello {0.author.mention}'.format(message)
        print('Response: ', msg)
        print('Response: ', msg, file=self.log,flush=True)
        await self.client.send_message(message.channel,msg)
    async def about(self,client,message,words):
        msg = ("I am FourthBot v0.1.  I act as the 4th DM for the group.  You can ask "
            "me lots of things or use me to roll dice through discord, or use me to "
            "keep track of your characters, experience, and treasure.  I am not "
            "finished yet though!  Use !help to see all of my current commands.")
        print('Response: About message')
        print('Response: About message',file=self.log,flush=True)
        await self.client.send_message(message.channel,msg)
    async def help(self,client,message,words):
        msg = "Here is an updated list of commands: \n"
        for key in self.commands:
            next_line = '  **!' +key+'**: '+self.commands[key][1]+'\n'
            msg = msg + next_line
        print('Response: Help message')
        print('Response: Help message',file=self.log,flush=True)
        await self.client.send_message(message.channel,msg)


async def roll(client,message,words):
    if len(words) == 1:
        msg = ("Roll dice how you would see the dice written\n"
                "Examples: **!roll d20** : roll 1 d20\n"
                "**!roll 8d6** : roll 8 d6s \n"
                "**!roll 1d20 2d12 3d8**")
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
        if die_size < 2: die_size = 2
        if die_size > 100: die_size = 100
        rolls = []
        for i in range(quantity):
            rolls.append(random.randint(1,die_size))
        output.append(rolls)
    
    await client.send_message(message.channel,str(output))
        
        


if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    D = discordHandler('config/discord.json')
    D.add_command('roll', roll, 'Roll Dice')
    D.run()