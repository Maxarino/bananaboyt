import discord
import json
import os
import random
from discord.ext import commands


class LevelSystem(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='xp', help='displays the amount of xp points <member> has acquired', aliases=['exp', 'experience'])
    async def xp(self, ctx, *, member: discord.Member = None):

        b = False
        if member is None:
            member = ctx.author
            b = True

        with open('users.json', 'r') as f:
            users = json.load(f)

            if f'{member.id}' in users[f'{member.guild.id}']:
                embed = discord.Embed(color=discord.Color.gold())
                if b:
                    embed.description = f"you have **{users[f'{member.guild.id}'][f'{member.id}']['xp']} xp**."
                else:
                    embed.description = f"{member.name} has **{users[f'{member.guild.id}'][f'{member.id}']['xp']} xp**."
                await ctx.send(embed=embed)

    @commands.command(name='level', help='displays the current level of <member>', aliases=['lvl'])
    async def level(self, ctx, *, member: discord.Member = None):

        b = False
        if member is None:
            member = ctx.author
            b = True

        with open('users.json', 'r') as f:

            users = json.load(f)

            if f'{member.id}' in users[f'{member.guild.id}']:
                embed = discord.Embed(color=discord.Color.gold())
                if b:
                    embed.description = f"you are **level {users[f'{member.guild.id}'][f'{member.id}']['level']}**."
                else:
                    embed.description = f"{member.name} is **level {users[f'{member.guild.id}'][f'{member.id}']['level']}**."
                await ctx.send(embed=embed)

    @commands.command(name='leaderboard', help='displays server chat leaderboard', aliases=['lb'])
    async def leaderboard(self, ctx):

        with open('users.json', 'r') as f:

            users = json.load(f)[f'{ctx.guild.id}']
            leaderboards = []
            for key, value in users.items():
                leaderboards.append(LeaderBoardPosition(key, value['level'], value['xp']))
            num_members = len(leaderboards)

            top = sorted(leaderboards, key=lambda x: x.xp, reverse=True)

            embed = discord.Embed(color=discord.Color.gold())
            embed.description = ""

            places = ["one", "two", "three", "four", "five"]
            for (i, place) in enumerate(places):
                if num_members >= i + 1:
                    user_id = self.bot.get_user(int(top[i].userid))
                    embed.description += f':{place}: {user_id} | **level {top[i].level}**\n\n'
                else:
                    break

            await ctx.send(embed=embed)

    async def update_data(self, users: dict, user: discord.Member):

        if f'{user.guild.id}' not in users:
            users[f'{user.guild.id}'] = {}
        if f'{user.id}' not in users[f'{user.guild.id}']:
            users[f'{user.guild.id}'][f'{user.id}'] = {}
            users[f'{user.guild.id}'][f'{user.id}']['xp'] = 0
            users[f'{user.guild.id}'][f'{user.id}']['level'] = 1

    async def add_xp(self, users: dict, user: discord.Member, xp: int):
        users[f'{user.guild.id}'][f'{user.id}']['xp'] += xp

    async def check_for_level_up(self, users: dict, user: discord.Member, channel: discord.TextChannel):

        xp = users[f'{user.guild.id}'][f'{user.id}']['xp']
        level_start = users[f'{user.guild.id}'][f'{user.id}']['level']
        level_end = int(xp ** (1/4))

        if level_start < level_end:
            embed = discord.Embed(color=discord.Color.gold())
            users[f'{user.guild.id}'][f'{user.id}']['level'] = level_end
            level_up_messages = ['is now', 'leveled up to', 'just advanced to']
            embed.description = f'{user.name} {random.choice(level_up_messages)} **level {level_end}**!'
            await channel.send(embed=embed)


class LeaderBoardPosition:

    def __init__(self, userid, level, xp):
        self.userid = userid
        self.level = level
        self.xp = xp


def setup(bot):
    bot.add_cog(LevelSystem(bot))
