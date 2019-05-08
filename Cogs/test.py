import discord
from discord.ext import commands

test_help = """ This is a test command that simply repeats back what you say."""


class TestCog(commands.Cog):
    """ This is a test cog with only one test command"""
    
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(help=test_help)
    async def test(self, ctx, *, test : str):
        await ctx.send(test)

def setup(bot):
    bot.add_cog(TestCog(bot))