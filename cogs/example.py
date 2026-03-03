from disnake.ext import commands
from disnake.ext.commands import Bot, Cog
import disnake



class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("example cog loaded")

    @commands.slash_command()
    async def sosal(self, interaction: disnake.CommandInteraction):
        await interaction.response.send_message("yes", ephemeral=True)

def setup(bot: Bot):
   bot.add_cog(Example(bot))
