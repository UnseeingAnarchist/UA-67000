import discord
from discord.ext import commands
import os
import logging
from dotenv import load
import json

load('.env')

token = os.getenv('DISCORD_TOKEN')
with open('stalkers.json', 'r') as stalkers_file:
    stalkers = json.load(stalkers_file)

stalkers = {int(key): value for key, value in stalkers.items()}

handler = logging.FileHandler('discord.log', mode='w')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready to go. Good job, little piggy!")

@bot.event
async def on_message(message):
    if message.channel.name == 'counting':
        messages = [m async for m in message.channel.history(limit=2)]
        previous = messages[1]
        current = messages[0]

        try:
            previous = int(previous.content)
            current = int(current.content)
        
            if current != previous + 1:
                await message.delete()
            else:
                print("Congrats, piggy! Your not as dumb as you look, oink oink!")

        except ValueError:
            print("the message is not a number, piggy!")
            await message.delete()
    await bot.process_commands(message)

@bot.command()
async def stalk(ctx):
    if len(ctx.message.mentions) == 0:
        await ctx.send("You need to mension someone to watch, you crazy stalker!")
        return
    if len(ctx.message.mentions) == 1:
        stalker = ctx.author.id
        target = ctx.message.mentions[0].id
        if stalker not in stalkers:
            stalkers[stalker] = []
        if target not in stalkers[stalker]:
            stalkers[stalker].append(target)
            await ctx.send(f"{ctx.author.name} is now stalking {ctx.message.mentions[0].name}")
        else:
            await ctx.send("You are already stalking this user!")
    with open('stalkers.json', 'w') as stalkers_file:
        json.dump(stalkers, stalkers_file, indent=4)
    await bot.process_commands()
        

bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
