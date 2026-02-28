import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("Example cog initialized")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

async def setup(bot):
    await bot.add_cog(Example(bot))
