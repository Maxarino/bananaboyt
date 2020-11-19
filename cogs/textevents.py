import discord
import json
import os
import random
from discord.ext import commands


class TextEvents(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if 'pog' in message.content.lower().replace(" ", "") \
                and message.author != self.bot.user:
            await message.add_reaction(':Pog:698454205744152628')

        if not message.author.bot:
            with open('users.json', 'r') as f:
                users = json.load(f)

            levelsystem = self.bot.get_cog('LevelSystem')

            await levelsystem.update_data(users, message.author)
            await levelsystem.add_xp(users, message.author, 5)
            await levelsystem.check_for_level_up(users, message.author, message.channel)

            with open('users.json', 'w') as f:
                json.dump(users, f)

        # await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        print(f'{member.name} has joined {member.guild}.\n')
        if not member.bot:
            await member.create_dm()
            await member.dm_channel.send(
                f'yo'
            )

        if member.guild.id == 643645122638249985:  # avacado server
            await member.add_roles(member.guild.get_role(717104002021589113))  # avacado role

        if not member.bot:
            with open('users.json', 'r') as f:
                users = json.load(f)

            levelsystem = self.bot.get_cog('LevelSystem')

            await levelsystem.update_data(users, member)

            with open('users.json', 'w') as f:
                json.dump(users, f)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f'{member.name} has left {member.guild}.\n')


def setup(bot):
    bot.add_cog(TextEvents(bot))
