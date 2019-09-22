#############
## Treasure.py
## Author: Brian Scaramella
## Date: 9/22/2019
## For treasure based commands
#############
## Command List
## !treasure view magic items
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
TREASURE_LOCATION = "Treasure Chart!A2:G22"

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


    ### TODO:
    # Treasure commands
    # !treasure [treasure name]
    #   Get further info on a treasure. If in DM_chat or DM direct messages, give known/full description
    # !treasure [character]
    #   Get list of treasures for a specific character
    # !treasure all
    #   For players to get list of all treasures of characters of players in channel
    @commands.command(help="Use this to look at treasure descriptions for your current character")
    async def treasure(self, ctx, *args):
        args = [x.lower() for x in args]
        author    = self.users[str(ctx.message.author.id)]
        is_dm     = 'DM' in (role.name for role in ctx.message.author.roles)
        raw_data = self.handler.read(TREASURE_LOCATION)

        with open(JSON_CURRENT,'r') as current_file:
            current = json.load(current_file)

        filter_character =  None if is_dm else current[author]

        # Mapping from characters to their treasure entries
        characters_treasures = {}

        for treasure_entry in raw_data:
            ## treasure_entry = [name, owner, attuned, attunement req, rarity, known desc, full desc]
            character = treasure_entry[1]
            if is_dm or filter_character == character:
                if not character in characters_treasures:
                    characters_treasures[character] = []
                characters_treasures[character].append(treasure_entry)
        
        msg = ""

        for character in sorted(characters_treasures.keys()):
            t_entries = characters_treasures[character]
            owner = "Unowned" if character=="" else character
            msg += owner + ":\n  "
            msg += "\n  ".join(t[0] for t in t_entries)
            msg += "\n"

        while len(msg) > (2000-6):
            await ctx.send("```" + msg[0:2000-6] + "```")
            msg = msg[2000-6:]

        await ctx.send("```" + msg + "```")



