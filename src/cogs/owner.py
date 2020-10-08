import os
import json

import discord
from discord.ext import commands

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('./config.json') as c:
            self.config = json.load(c)

    @commands.command(name='test', hidden=True)
    @commands.is_owner()
    async def test_command(self, ctx):
        print(bot.update_channel_id)
        print(self.config.get('update_channel'))
        print(bot.get_channel(self.config.get('update_channel')))

    @commands.command(name='owninfo', hidden=True)
    @commands.is_owner()
    async def get_infor(self, ctx):
        for role in ctx.guild.roles:
            await ctx.send(f"{role}, {role.id}")

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            try:
                self.bot.unload_extension("cogs.{}".format(cog))
            except:
                pass
            self.bot.load_extension("cogs.{}".format(cog))
        except Exception as e:
            await ctx.send('**`ERROR:\n{}`**'.format(e))
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot):
    bot.add_cog(OwnerCog(bot))