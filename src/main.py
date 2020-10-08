import os
import json
import pathlib
import asyncio

import discord
from discord.ext import commands

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

# Get configuration
with open('./config.json') as c:
    config = json.load(c)

# Reload all cogs when they change
class CogReloader(FileSystemEventHandler):
    def __init__(self, bot):
        self.bot = bot

    def on_modified(self, event):
        if type(event) == FileModifiedEvent:
            try:
                self.bot.unload_extension(
                    f"cogs.{event.src_path.split('/')[-1].split('.')[0]}")
            except Exception as e:
                print("Failed to unload cog: {}".format(e))

            try:
                self.bot.load_extension(
                    f"cogs.{event.src_path.split('/')[-1].split('.')[0]}")
            except Exception as e:
                print("Failed to load cog: {}".format(e))


# Bot description
description = "BiscottiBot - Bringing you freshly baked commands"

# Bot cogs
cog_files = os.listdir('./cogs')
cogs = [f"cogs.{cog.split('.')[0]}" for cog in cog_files]

# Global check
def global_check(ctx):
    return ctx.message.author.bot == False

# Create the bot
bot = commands.Bot(
    command_prefix='~',
    owner_id=config.get('owner'),
    description=description,
    activity=discord.Game("Use ~help for commands")
)

# Variables - Terrible practice. If you're reading this don't judge me too badly :(
bot.update_channel_id = None
bot.initial_role = None

# Start the show
if __name__ == '__main__':
    event_handler = CogReloader(bot)
    observer = Observer()
    observer.schedule(event_handler, './cogs')
    observer.start()

    bot.add_check(global_check)
    # bot.remove_command('help')
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print("Failed to load cog: {}".format(e))

# When everything is ready
@bot.event
async def on_ready():
    guild = None
    if config.get('server_id'):
        guild = bot.get_guild(config.get('server_id'))
    if config.get('update_channel'):
        bot.update_channel_id = bot.get_channel(config.get('update_channel'))
    if config.get('initial_role') and guild:
        bot.initial_role = guild.get_role(config.get('initial_role'))
    
    print("The bot is ready")


# Waiting to hear from the webhook
@bot.event
async def on_message(message):
    if message.channel == bot.update_channel_id:
        os.system('cd .. && git pull -q --no-edit && cd src/')
    await bot.process_commands(message)

# Add the `initial_role` when a member joins
@bot.event
async def on_member_join(member):
    await member.add_roles(bot.initial_role)

# Run the bot
bot.run(config.get('key'), bot=True, reconnect=True)