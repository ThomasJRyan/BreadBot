import os

import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', hidden=True)
    async def get_infor(self, ctx):
        await ctx.send("pong!")

def setup(bot):
    bot.add_cog(PingCog(bot))