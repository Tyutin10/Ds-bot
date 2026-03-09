from disnake.ext import commands
import disnake


class RoleDropdown(disnake.ui.Select):

    def __init__(self, options):

        self.options = options
        super().__init__(placeholder="Выберите роль", min_values=1, max_values=1, options=options[:25])

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
    def __init__(self, options):
        super().__init__(timeout=None)
        self.add_item(RoleDropdown(options))

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
    
    @commands.slash_command(description="Отправить меню ролей")
    @commands.has_permissions(administrator=True)
    async def role_menu(self, interaction: disnake.CommandInteraction):
        roles = [role for role in interaction.guild.roles]
        options = []
        
        for role in roles:
            
            match True:
                case _ if role.is_default():
                    continue

                case _ if role.permissions.administrator:
                    continue

                case _ if role.managed:
                    continue

                case _ if role.position >= interaction.guild.me.top_role.position:
                    continue

            options.append(disnake.SelectOption(label=role.name, value=str(role.id)))

        embed = disnake.Embed(title="🎭 Выбор ролей",description="Выберите роль для добавления/удаления",color=disnake.Color.blue())
        await interaction.response.send_message(embed=embed,view=RoleView(options), ephemeral=True)


def setup(bot):
    bot.add_cog(RoleManager(bot))
