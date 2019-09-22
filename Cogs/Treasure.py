#############
## Treasure.py
## Author: Brian Scaramella
## Date: 9/22/2019
## For treasure based commands
#############
## Command List
## 
#############

import discord
from discord.ext import commands

import googleHandler
import json
import difflib
import logging
import string

## Magic Variables
# Other
DM_LIST         = ['Chris','Brian','Tommy']

# Google
GOOGLE_HANDLE   = '1dVZlsgtbUq0MGWV4kBg7m6Kwv2kQtbBd88KFHq9uumo'
TREASURE_LOCATION = "Treasure Chart!A:G"

#JSON
JSON_USERS      = 'config/users.json'
JSON_CURRENT    = 'config/current_characters.json'
JSON_CHATS      = 'config/character_chats.json'

def setup(bot):
    bot.add_cog(Treasure(bot))

class Treasure(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        logging.debug("Treasure Cog Loaded")        
        ## TODO: Eventually pull handle from somewhere
        google_token = GOOGLE_HANDLE
        self.handler = googleHandler.googleHandler(google_token)
        ## Get Important JSON files
        with open(JSON_USERS,'r') as users_file:
          self.users = json.load(users_file)
        self.dms = DM_LIST

    @commands.command(help="Use this to look at treasure descriptions for your current character")
    async def treasure(self, ctx, *args):
        args = [x.lower() for x in args]
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data = self.handler.read(TREASURE_LOCATION)

        with open(JSON_CURRENT,'r') as current_file:
            current = json.load(current_file)

        current_character = current[author]

        treasure_names = []
        for treasure_entry in raw_data:
            treasure_name = treasure_entry[0]
            character = treasure_entry[1]
            if character == current_character:
                treasure_names.append(treasure_name)

        msg = "```{}```".format("\n".join(treasure_names))

        await ctx.send(msg)



