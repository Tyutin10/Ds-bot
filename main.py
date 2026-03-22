import disnake
from disnake.ext.commands import InteractionBot
import logging
from config import Config
import os
from db import create_user

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

config = Config()
config.get_config('config.json')

intents = disnake.Intents.all()
bot = InteractionBot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ BOT logged as {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print(f"📊 Servers: {len(bot.guilds)}")

    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:  
                await create_user(member.id, str(member))
    print("✅ Все существующие пользователи добавлены в БД")

@bot.event
async def on_member_join(member):
    if not member.bot:
        await create_user(member.id, str(member))
        print(f"Добавлен новый пользователь: {member}")

for file in os.listdir(r"./cogs"):
    if file.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"✅ Loaded {file}")
        except Exception as e:
            print(f"❌ Failed to load {file}: {e}")

bot.run(config.token)
