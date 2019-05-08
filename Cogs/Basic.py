import discord
from discord.ext import commands

import logging

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
