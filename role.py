import discord
from discord.ext import commands
from discord.utils import get


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

class RoleManager:
    def __init__(self, bot):
        self.bot = bot
        self.roles = {}  # Хранилище ролей

    async def add_role(self, ctx, member: discord.Member, role_name: str):
        """Добавляет роль пользователю"""
        role = get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Роль {role_name} не найдена")
            return
        
        try:
            await member.add_roles(role)
            await ctx.send(f"Роль {role_name} успешно добавлена пользователю {member.name}")
        except Exception as e:
            await ctx.send(f"Ошибка при добавлении роли: {str(e)}")

    async def remove_role(self, ctx, member: discord.Member, role_name: str):
        """Удаляет роль у пользователя"""
        role = get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Роль {role_name} не найдена")
            return
        
        try:
            await member.remove_roles(role)
            await ctx.send(f"Роль {role_name} успешно удалена у пользователя {member.name}")
        except Exception as e:
            await ctx.send(f"Ошибка при удалении роли: {str(e)}")

    async def create_role(self, ctx, role_name: str, color: discord.Color = discord.Color.default()):
        """Создает новую роль"""
        try:
            await ctx.guild.create_role(name=role_name, colour=color)
            await ctx.send(f"Роль {role_name} успешно создана")
        except Exception as e:
            await ctx.send(f"Ошибка при создании роли: {str(e)}")

    async def delete_role(self, ctx, role_name: str):
        """Удаляет роль"""
        role = get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Роль {role_name} не найдена")
            return
        
        try:
            await role.delete()
            await ctx.send(f"Роль {role_name} успешно удалена")
        except Exception as e:
            await ctx.send(f"Ошибка при удалении роли: {str(e)}")

# Регистрация команд
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role_name: str):
    role_manager = RoleManager(bot)
    await role_manager.add_role(ctx, member, role_name)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role_name: str):
    role_manager = RoleManager(bot)
    await role_manager.remove_role(ctx, member, role_name)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def createrole(ctx, role_name: str, color: str = "default"):
    color_map = {
        "default": discord.Color.default(),
        "red": discord.Color.red(),
        "green": discord.Color.green(),
        "blue": discord.Color.blue()
    }
    
    role_color = color_map.get(color, discord.Color.default())
    role_manager = RoleManager(bot)
    await role_manager.create_role(ctx, role_name, role_color)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def deleterole(ctx, role_name: str):
    role_manager = RoleManager(bot)
    await role_manager.delete_role(ctx, role_name)

# Запуск бота
if __name__ == "__main__":
    bot.run('YOUR_BOT')