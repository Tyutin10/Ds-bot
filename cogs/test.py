import discord 
from discord.ext import commands

# test-cog

class Test(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx):
        await ctx.send('test_new')

async def setup(bot):
    await bot.add_cog(Test(bot))