import discord
from discord.ext import commands

import logging
import random
import re

UNOOF_PERCENT = 2
B_OOF_PERCENT = 20

OOF_RESPONSES = ["Big oof, my dudes", 
    "Aw fuck I can't believe you done this",
    "I'm not even surprised tbh", 
    "I am dead :joy::joy::joy:",
    ""
    '"Bitchy Bic Bickerson" -Alyssa Knight', 
    "I am confusion",
    "You tried", 
    "May I ask why you need this crowdsourcing data?", 
    "Good job team. This is what I've come to expect from you.", 
    "What does this question mean?",]
OOF_RESPONSES_P = [100, 20, 10, 20, 5, 7, 10, 1, 3, 1]

def setup(bot):
    bot.add_cog(Basic(bot))

class Basic(commands.Cog):
    """ All basic commands that don't require any other handlers can be found here."""
    def __init__(self,bot):
        self.bot = bot
        logging.debug("Basic Cog loaded")

    @commands.command(help="Help Text")
    async def hi(self, ctx):
        msg = "Hello {0.message.author.mention}".format(ctx)
        await ctx.send(msg)

    @commands.command(help="About this bot")
    async def about(self, ctx):
        msg = ("I am FourthBot v2.0.  I act as the 4th DM for the group.  You can ask "
            "me lots of things or use me to roll dice through discord, or use me to "
            "keep track of your characters, experience, spells, and treasure.  I am not "
            "finished yet though!  Use !help to see all of my current commands.")
        await ctx.send(msg)

    @commands.command(help="For those oofs that are bound to happen")
    async def oof(self, ctx):
        msg = random.choices(OOF_RESPONSES, weights=OOF_RESPONSES_P)[0]
        
        r = random.random()
        if r < UNOOF_PERCENT/100.0:
            msg = (msg[0:10] + "... No... You know what? Not this time. I am rewinding time "
                "to right before whatever "
                "caused this oof. Don't waste this moment of generosity. **UN:clap:OOF:clap:**")
        elif (r-UNOOF_PERCENT/100.0) < B_OOF_PERCENT/100.0:
            msg = msg.replace('b', ':b:')
            msg = msg.replace('B', ':b:')
        await ctx.send(msg)
    
    @commands.command(help="Roll Dice")
    async def roll(self, ctx):
        """ We will use regular expression matching for dice rolling:
        Addends are parts that can be added (or even subtracted):
        5d6, 14, d4, d100
        to match an int, use [0-9]+
        to match a dice roll, [1-9][0-9]*[dD][1-9][0-9]*
        in between rolls can be a + """
        #fullmatch = re.compile("(-?([0-9]+|[1-9][0-9]*[dD][1-9][0-9]*)([\+\-]([0-9]+|[1-9][0-9]*[dD][1-9][0-9]*))*")
        await ctx.send("Not implemented yet hold horses plox")
