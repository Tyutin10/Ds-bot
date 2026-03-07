from disnake.ext import commands
import disnake

SELF_ROLES = [
    1479154920761589972,  # Chill
    1479154874112544922,  # Working
    1479154801450156223   # Afk
]

class RoleDropdown(disnake.ui.Select):
    def __init__(self, guild):

        options = []

        for role_id in SELF_ROLES:
            role = guild.get_role(role_id)
            if role:
                options.append(disnake.SelectOption(label=role.name,value=str(role.id)))

        super().__init__(placeholder="Выберите роль",min_values=1,max_values=1,options=options)

    async def callback(self, interaction: disnake.MessageInteraction):

        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"❌ Роль {role.mention} снята",ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Роль {role.mention} выдана",ephemeral=True)

class RoleView(disnake.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.add_item(RoleDropdown(guild))

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name='my_roles', description="Получить список своих ролей")
    async def get_roles(self, interaction: disnake.CommandInteraction):
        rolenames = [role.mention for role in interaction.user.roles if role.name != "@everyone"]
        await interaction.response.send_message(f"Твои роли: {', '.join(rolenames)}", ephemeral=True)

    @commands.slash_command(name="roles", description="Показать все роли сервера")
    async def roles(self, interaction: disnake.CommandInteraction):
        roles = interaction.guild.roles[::-1] 
        role_list = []
        for role in roles:
            if role.name != "@everyone":
                role_list.append(f"{role.mention} | ID: `{role.id}`")
        roles_text = "\n".join(role_list)
        if len(roles_text) > 1800: 
            roles_text = roles_text[:1800] + "\n..."
        await interaction.response.send_message(f"📋 **Роли сервера ({len(role_list)}):**\n{roles_text}", ephemeral=True)

    # @commands.slash_command(name='remove_role', description='Снятие роли')
    # async def take_role(self, interaction: disnake.CommandInteraction, role: disnake.Role):
    #     if role not in interaction.user.roles:
    #         await interaction.response.send_message("У тебя нет такой роли!", ephemeral=True)
    #         return
    #     await interaction.user.remove_roles(role)
    #     await interaction.response.send_message(f'Роль отозвана!', ephemeral=True)

    # @commands.slash_command(name='add_roles', description="Полуение роли")
    # async def addrole(self, interaction: disnake.CommandInteraction, role: disnake.Role):
    #     if role in interaction.user.roles:
    #         await interaction.response.send_message("У тебя уже есть такая роль!", ephemeral=True)
    #         return
    #     if role.permissions.administrator or role >= interaction.guild.me.top_role or role.managed:
    #         await interaction.response.send_message("У вас нет доступа к этой роли!", ephemeral=True)
    #         return
    #     await interaction.user.add_roles(role)
    #     await interaction.response.send_message(f"Роль получена!", ephemeral=True)
    
    @commands.slash_command(description="Отправить меню ролей")
    @commands.has_permissions(administrator=True)
    async def role_menu(self, interaction: disnake.CommandInteraction):
        embed = disnake.Embed(title="🎭 Выбор ролей",description="Выберите роль для добавления/удаления",color=disnake.Color.blue())
        await interaction.response.send_message(embed=embed,view=RoleView(interaction.guild), ephemeral=True)


def setup(bot):
    bot.add_cog(RoleManager(bot))
