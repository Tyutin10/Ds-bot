import discord
from discord.ext import commands
import logging
from config import Config

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

config = Config()
config.get_config('config.json')
print(config.test)

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot("/", intents=intents)

@bot.event
async def on_ready():
    print("Я родился!")

@bot.event
async def on_message(message):
    if message.author.bot: return print('Сообщение бота не учитывается')

    if message.content.lower() in ["здарова", "привет", "hi"]:
        await message.channel.send("Здарова лох)")

bot.run(config.token, log_handler=handler, log_level=logging.DEBUG)
