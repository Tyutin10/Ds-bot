from disnake.ext import commands, tasks
import disnake


class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="получить список своих ролей")
    async def get_roles(self, interaction: disnake.CommandInteraction):
        rolenames = [role.name for role in interaction.user.roles[1:]]
        await interaction.response.send_message(f"your roles: {rolenames}", ephemeral=True)

    @commands.slash_command(name='забрать_роль', description='Отзыв роли у пользователя')
    async def take_role(self, interaction, member: disnake.Member, role: disnake.Role):
        await member.remove_roles(role)
        await interaction.response.send_message('Роль отозвана!')

def setup(bot):
    bot.add_cog(RoleManager(bot))
