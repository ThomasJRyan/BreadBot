import json

import discord
from discord.ext import commands

class RoleCog(commands.Cog):
    """Any commands involving docstrings go here

    Commands:
        gamewith - Adds 'On Stream' role to a user
        donegame - Removes 'On Stream' role from all users
    """
    def __init__(self, bot):
        self.bot = bot
        with open('./config.json') as c:
            self.config = json.load(c)

    async def is_admin(ctx, hidden=True):
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

        await member.add_roles(role)
        await ctx.send("Member has been given the `On Stream` role!")

    @commands.command(name='donegame', aliases=['dg'])
    @commands.check(is_admin)
    async def done_game(self, ctx):
        if not self.config.get('stream_role'):
            await ctx.send('Error: `stream_role` not configured. Talk to your host.')
            return

        role = ctx.guild.get_role(self.config.get('stream_role'))

        for member in ctx.guild.members:
            if role in member.roles:
                await member.remove_roles(role)

        await ctx.send("All members have be stripped of the `On Stream` role")
        

def setup(bot):
    bot.add_cog(RoleCog(bot))