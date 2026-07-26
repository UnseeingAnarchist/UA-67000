import discord
from discord.ext import commands
import os
import logging
from dotenv import load
import json
import counting
import stalking

load('.env')

token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler('discord.log', mode='w')
counting_manager = counting.Counting()
stalking_manager = stalking.StalkingManager('stalkers.json')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready to go. Good job, little piggy!")

@bot.event
async def on_message(message):
    print("On message fired, piggy.")
    await counting_manager.run(message, bot)
    await bot.process_commands(message)

@bot.event
async def on_presence_update(before, after):
    await stalking_manager.check_status(before, after, bot)
        
@bot.event
async def on_user_update(before, after):
    await stalking_manager.check_profile_changes(before, after, bot)            

@bot.command()
async def stalk(ctx):
    await stalking_manager.stalk_command(ctx, bot)

@bot.command()
async def unstalk(ctx):
    await stalking_manager.unstalk_command(ctx, bot)

@bot.command()
async def stalking(ctx):
    await stalking_manager.list_command(ctx, bot)
        
bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
