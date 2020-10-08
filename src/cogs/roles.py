import json

import discord
from discord.ext import commands


class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('./config.json') as c:
            self.config = json.load(c)

    async def is_admin(ctx, hidden=True):
        # print(ctx.author.guild_permissions.administrator)
        return ctx.author.guild_permissions.administrator

    @commands.command(name='gamewith', aliases=['gw'])
    @commands.check(is_admin)
    async def game_with(self, ctx, member: discord.Member = None):
        if not self.config.get('stream_role'):
            await ctx.send('Error: `stream_role` not configured. Talk to your host.')
            return
        if not member:
            await ctx.send('Usage: `~gamewith <@member>`')
            return

        role = ctx.guild.get_role(self.config.get('stream_role'))

        if role in member.roles:
            await ctx.send('Member already has this role')
            return

        await member.add_roles([role])
        await ctx.send("Member has been given the `On Stream` role!")

        

def setup(bot):
    bot.add_cog(RoleCog(bot))