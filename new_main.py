import discord
from   discord.ext import commands


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Logged in as\n{0}\n{1}".format(bot.user.name,bot.user.id))
    bot.load_extension("Cogs.test")
bot.run('NDM4Mjg4NjYxMzk4NjgzNjUw.DcCb5A.gyiEoXkZyEnnByhjOXshRriRHXY')

