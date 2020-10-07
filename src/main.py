import os
import json
import pathlib
import asyncio

import discord
from discord.ext import commands

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

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
                self.bot.load_extension(
                    f"cogs.{event.src_path.split('/')[-1].split('.')[0]}")
            except Exception as e:
                print("Failed to load cog: {}".format(e))


# Bot description
description = "BreadBot - For doing things for the Bakery"

# Bot cogs
cog_files = os.listdir('./cogs')
cogs = [f"cogs.{cog.split('.')[0]}" for cog in cog_files]

# Global check
def global_check(ctx):
    return ctx.message.author.bot == False

# Create the bot
bot = commands.Bot(
    command_prefix='~',
    owner_id=160941453671923722,
    description=description,
    activity=discord.Game("Use ~help for commands")
)

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
    print("The bot is ready")


# Run the bot
bot.run(config['key'], bot=True, reconnect=True)