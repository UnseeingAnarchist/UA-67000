import discord
from discord.ext import commands
import os
import logging
from dotenv import load
import json
import counting
import stalking
import AdminSettings

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
settings_manager = AdminSettings.SettingsManager(bot)

@bot.event
async def on_ready():
    print("Bot is ready to go. Good job, little piggy!")

@bot.event
async def on_message(message):
    print("On message fired, piggy.")
    if not message.author.bot:
        print("The author was not a bot")
        await counting_manager.run(message, bot, settings_manager)
        await bot.process_commands(message)
    else:
        print("The author of this message was a bot")

@bot.event
async def on_presence_update(before, after):
    await stalking_manager.check_status(before, after, bot)
        
@bot.event
async def on_user_update(before, after):
    await stalking_manager.check_profile_changes(before, after, bot)            

@bot.command()
async def stalk(ctx):
    guild_id_str = str(ctx.guild.id)
    if guild_id_str in settings_manager.servers:
        if 'stalking_consent_enabled' in settings_manager.servers[guild_id_str]:
            if 'stalking_consent_roll_id' in settings_manager.servers[guild_id_str]:
                if settings_manager.servers[guild_id_str]['stalking_consent_enabled']:
                    if ctx.guild.get_role(settings_manager.servers[guild_id_str]['stalking_consent_roll_id']) in ctx.author.roles:
                        if ctx.guild.get_role(settings_manager.servers[guild_id_str]['stalking_consent_roll_id']) in ctx.message.mentions[0].roles:
                            await stalking_manager.stalk_command(ctx, bot)
                        else:
                            await ctx.send(f"{ctx.message.mentions[0].display_name} hasn't consented to being stalked, you little peeping tom!")
                    else:
                        await ctx.send("You haven't even given consent to be stalked, so you can't stalk anyone!")
                else:
                    await stalking_manager.stalk_command(ctx, bot)
            else:
                await stalking_manager.stalk_command(ctx, bot)
        else:
            await stalking_manager.stalk_command(ctx, bot)
    else:
        await stalking_manager.stalk_command(ctx, bot)


@bot.command()
async def unstalk(ctx):
    await stalking_manager.unstalk_command(ctx, bot)

@bot.command()
async def stalking(ctx):
    await stalking_manager.list_command(ctx, bot)

@bot.command()
async def adminrole(ctx):
    print("adminrole command fired.")
    print(ctx.author.guild_permissions.manage_guild)
    if ctx.author.guild_permissions.manage_guild:
        print(f"Author has manage guild permission\nserver id: {ctx.guild.id}\nAuthor mentioned: {ctx.message.role_mentions[0]}")
        settings_manager.change_admin_roll(str(ctx.guild.id), ctx.message.role_mentions[0].id)
        await ctx.send(f"The admin roll is now {ctx.message.role_mentions[0].name}.")
    print("adminrole command ran")    

@bot.command()
async def countingchannel(ctx):
    print("Countingchannel command fired.")
    guild_id_str = str(ctx.guild.id)
    if guild_id_str in settings_manager.servers:
        if ctx.guild.get_role(settings_manager.servers[guild_id_str]['admin_roll_id']) in ctx.author.roles:
            settings_manager.set_counting_channel(str(ctx.guild.id), ctx.message.channel_mentions[0].id)
            await ctx.send(f"The counting channel is now set to {ctx.message.channel_mentions[0].name}.")

@bot.command()
async def stalkingconsentrole(ctx):
    guild_id_str = str(ctx.guild.id)
    if ctx.guild.get_role(settings_manager.servers[guild_id_str]['admin_roll_id']) in ctx.author.roles:
        settings_manager.change_stalking_consent_roll(guild_id_str, ctx.message.role_mentions[0].id)
        await ctx.send(f"The stalking consent role is now set to {ctx.message.role_mentions[0].name}.")
        
@bot.command()
async def stalkingconsent(ctx, value):
    guild_id_str = str(ctx.guild.id)
    if ctx.guild.get_role(settings_manager.servers[guild_id_str]['admin_roll_id']) in ctx.author.roles:
        if value.lower() == 'enable':
            settings_manager.set_stalking_consent(guild_id_str, True)
            await ctx.send("Stalking consent features are now enabled!")
        elif value.lower() == 'disable':
            settings_manager.set_stalking_consent(guild_id_str, False)
            await ctx.send("Stalking consent features are now disabled!")


bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
