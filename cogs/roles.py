from disnake.ext import commands, tasks
import disnake


class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="получить список своих ролей")
    async def get_roles(self, interaction: disnake.CommandInteraction):
        rolenames = [role.name for role in interaction.user.roles[1:]]
        await interaction.response.send_message(f"your roles: {rolenames}", ephemeral=True)

            

def setup(bot):
    bot.add_cog(RoleManager(bot))
