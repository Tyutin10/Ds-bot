import discord
from discord.ext import commands
import logging
import json
with open("config.json", "r") as json_file:
    a = json.load(json_file)

token = (a["token"])

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

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

bot.run(token, log_handler=handler, log_level=logging.DEBUG)