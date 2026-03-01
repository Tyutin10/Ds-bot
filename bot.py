import discord
from discord.ext import commands
import logging
from config import Config
import os
import asyncio

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

config = Config()
config.get_config('config.json')
print(config.test)

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Setup cogs

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Загружен cog: {filename[:-3]}')
            except Exception as e:
                print(f'Ошибка при загрузке {filename[:-3]}: {e}')

    
# Commands

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await bot.load_extension(f'cogs.{extension}')

# Events

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot: return print('Сообщение бота не учитывается')
    if message.content.lower() in ["здарова", "привет", "hi"]:
        await message.channel.send("Здарова лох)")
    await bot.process_commands(message)


async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.token)

asyncio.run(main())
bot.run(config.token, log_handler=handler, log_level=logging.DEBUG)
