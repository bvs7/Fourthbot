#############
## XP.py
## Author: Chris Scaramella and Brian Scaramella
## Date: 5/15/2019
## All commands involved in experience calculation
#############
## List of commands:
## xp       :   Check xp of all players, can check specific characters using that player's name
## current  :   Check who your current character is, can be used to change a player's current character
## bank     :   Check player's banked xp, can be used to spend banked xp on characters
## session  :   Used by DMs to grant all player current characters xp for the previous session
## bonus    :   Used by DMs to grant a player bonus XP
#############
import discord
from discord.ext import commands

import logging
import googleHandler
import json
import os
import datetime

## Magic Variables
# Google
GOOGLE_HANDLE   = '1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo'
XP_LOCATION     = 'Character Chart!A2:G13'
BANK_LOCATION   = 'Bank Chart!A:B'
BANK_TRACKER    = 'Bank Tracker!A:G'
SESSION_TRACKER = 'Session Tracker!A:E'

#JSON
JSON_USERS      = 'config/users.json'
JSON_CURRENT    = 'config/current_characters.json'
JSON_CHATS      = 'config/character_chats.json'

def setup(bot):
    bot.add_cog(XP(bot))

class XP(commands.Cog):
    """ All experience related commands"""
    ## XP Cog Variables
    ## self.handler : googleHandler - for accessing Google Doc
    ## self.users   : dict of ids to the names associated with them
    ## self.dms     : list of dm names #TODO: Replace self.dms with check role of the author
    
    def __init__(self,bot):
        self.bot = bot
        logging.debug("XP Cog loaded")
        ## TODO: Eventually pull handle from somewhere
        google_token = GOOGLE_HANDLE
        self.handler = googleHandler.googleHandler(google_token)
        ## Get Important JSON files
        with open(JSON_USERS,'r') as users_file:
            self.users = json.load(users_file)
    
    @commands.command(help="Use this command to check the xp of your characters")
    async def xp(self, ctx, *args):
        ## Get important variables
        args = [x.lower() for x in args]
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data = self.handler.read(XP_LOCATION)
        msg = '```'
        if not args: # No arg call show all chars user can possibly see
            for character in raw_data:
                if author == character[0] or is_dm:
                    msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(
                          character[1],character[4],character[5],character[6])
        if args: # call for if there are args
            for character in raw_data:
                if (author == character[0] or is_dm) and character[1].lower() in args:
                    msg = msg + '{:10}{:5} XP Level {:3}({:5} XP to next level)\n'.format(
                          character[1],character[4],character[5],character[6])
        msg = msg + '```'
        if msg == '``````':
            msg = 'No characters found, please check your spelling! :clap:'
        await ctx.send(msg)

    @commands.command(help="Check or change your current character")
    async def current(self,ctx, *args):
        ## Get important variables
        args = [x.capitalize() for x in args]
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data = self.handler.read(XP_LOCATION)
        with open(JSON_CURRENT,'r') as current_file:
            current = json.load(current_file)
        msg = ''
        if args and is_dm:
            for arg in args:
                if arg in current:
                    msg = msg + '{}\'s current character is **{}**\n'.format(arg, current[arg])
            if not msg:
                msg = 'I did not recognize any names.'
        elif args and not is_dm:
            if len(args) > 1:
                msg = 'You can only have one current character.  Please only use one name'
            arg = args[0]
            for character in raw_data:
                if arg != character[1]:
                    continue
                if author != character[0]:
                    msg = 'You do not own that character!'
                    break
                msg = 'I set your current character as \n'
                msg = msg + '```{:10}{:5} XP Level {:3}({:5} XP to next level)```'.format(
                    character[1],character[4],character[5],character[6])
                break
        elif not args and is_dm:
            msg = msg + 'Current Characters:\n```'
            for player in current:
                msg = msg + '{:10}:{:10}\n'.format(player,current[player])
            msg = msg + '```'
        elif not args and not is_dm:
            msg = 'Your current character is\n```{:10}```\n'.format(current[author])
            msg = msg + 'To switch to a different character use **!current (character)**'    
        await ctx.send(msg)

    @commands.command(help="Check your xp bank balance or spend it on characters")
    async def bank(self, ctx, *args):
        words = ctx.message.content.split()
        author_id = ctx.message.author.id
        author    = self.users[str(author_id)]
        roles     = list(role.name for role in ctx.message.author.roles)
        if len(words) == 1: # Simple bank check call
            raw_data = self.handler.read(BANK_LOCATION)
            if not 'DM' in roles:
                for player in raw_data:
                    if player[0] == author:
                        msg = 'You currently have **{}** banked xp\n'.format(str(player[1]))
                        msg = msg + 'To spend xp use **!bank (character) (amount) confirm**'
            else:
                msg = 'Players\' banked xp:\n```'
                for player in raw_data:
                    msg = msg + '{:8}:{:4}\n'.format(player[0],str(player[1]))
                msg = msg + '```'
        else: # call to change values
            character_flag = False
            spend_flag = False
            confirm_flag = False
            raw_data = self.handler.read(BANK_LOCATION)
            characters = set() ### Creating list of potential characters
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
                if word == 'Confirm' or word == 'corfirm':
                    confirm_flag = True
            if not character_flag:
                msg = "I didn't recognize which character you want to spend on.  Use !xp if you forget your character names."
            elif not spend_flag:
                msg = "I didn't recognize a number of points to spend.  Don't use anything but numbers for that."
            elif not confirm_flag:
                msg = "Enter the same command, with \"Confirm\" after it in order to confirm your spending"
            else: #Date, Author, Player, Character, Debits, Credits, Delta
                self.handler.append(BANK_TRACKER,[[str(datetime.date.today()),author,author, character, '0', spend, '-'+spend]])
                msg = "Confirmed! {} gained {} xp!".format(character, str(spend))
        await ctx.send(msg)

    @commands.command(help="DMs ONLY: grant session XP")
    async def session(self,ctx):
        words = ctx.message.content.split()
        author_id = ctx.message.author.id
        author    = self.users[str(author_id)]
        roles     = list(role.name for role in ctx.message.author.roles)
        if len(words) == 1: # Help call
            msg = "DMs can use this command in order to award session xp.  Any awarded XP will show up in the #announcements thread"
        else:
            if not 'DM' in roles:
                msg = "Sorry kid.  You have to be running the game to use this command."
            else:
                session_data = []
                points = words[1]
                msg = "The following characters have been awarded {} xp for a session\n```".format(points)
                with open(JSON_CURRENT,'r') as current_file:
                    current = json.load(current_file)
                    for player in current:
                        session_data.append([str(datetime.date.today()),author,player,current[player],points])
                        msg = msg + "{:10}\n".format(current[player])
                    msg = msg + "```"
                self.handler.append(SESSION_TRACKER, session_data)
        await ctx.send(msg)

    @commands.command(help="DMs ONLY: grant bonus XP")
    async def bonus(self, ctx):
        words = ctx.message.content.split()
        author_id = ctx.message.author.id
        author    = self.users[str(author_id)]
        roles     = list(role.name for role in ctx.message.author.roles)
        if 'DM' in roles:
            msg = "Sorry kid.  You have to be running the game to use this command."
        else:
            player_flag = False
            number_flag = False
            with open(JSON_CHATS,'r') as cc_file:
                chats = json.load(cc_file)
                if str(ctx.message.channel.id) in chats:
                    player_flag = True
                    player = chats[str(ctx.message.channel.id)]
                if words[1].isdigit():
                    number_flag = True
                    number = int(words[1])
            
            if not player_flag or not number_flag:
                msg = "No xp awarded because message did not parse correctly."
            else:
                session_data = [[str(datetime.date.today()),author, player, "",str(number),"0",str(number)]]
                self.handler.append(BANK_TRACKER, session_data)
                msg = "{} awarded {} {} bonus xp.  Congrats!".format(author,player,str(number))
        await ctx.send(msg)
