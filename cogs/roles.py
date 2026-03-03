import discord
from discord.ext import commands
from discord.utils import get


class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = {}
        print("RoleManager cog initialized!")

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

    @commands.command(name="addrole")
    @commands.has_permissions(manage_roles=True)
    async def addrole_cmd(self, ctx, member: discord.Member, role_name: str):
        await self.add_role(ctx, member, role_name)

    @commands.command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def removerole_cmd(self, ctx, member: discord.Member, role_name: str):
        await self.remove_role(ctx, member, role_name)

    @commands.command(name="createrole")
    @commands.has_permissions(manage_roles=True)
    async def createrole_cmd(self, ctx, role_name: str, color: str = "default"):
        color_map = {
            "default": discord.Color.default(),
            "red": discord.Color.red(),
            "green": discord.Color.green(),
            "blue": discord.Color.blue()
        }
        role_color = color_map.get(color, discord.Color.default())
        await self.create_role(ctx, role_name, role_color)

    @commands.command(name="deleterole")
    @commands.has_permissions(manage_roles=True)
    async def deleterole_cmd(self, ctx, role_name: str):
        await self.delete_role(ctx, role_name)


async def setup(bot):
    await bot.add_cog(RoleManager(bot))
