import discord
from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', hidden=True)
    async def help(self, ctx):

        embed = discord.Embed(color=discord.Color.gold(), title='Help')

        bot_commands = []
        for command in self.bot.commands:
            if command.cog is not None:
                bot_commands.append(command)
        sorted_bot_commands = sorted(bot_commands, key=lambda x: (x.cog_name, x.name))

        for command in sorted_bot_commands:
            formatted_params = ''
            for param in command.clean_params:
                if param != 'extension':
                    formatted_params += f'<{param}> '
            if not command.hidden:
                embed.add_field(name=f'.{command.name} {formatted_params}', value=f'{command.help}', inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='ping', hidden=True)
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        show_ping = discord.Embed(color=discord.Color.gold(), description=f'{ping}ms')
        await ctx.send(embed=show_ping)

    @commands.command(name='id', help='returns id of member')
    async def id(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        show_id = discord.Embed(color=discord.Color.gold(), description=f'{member.id}')
        show_id.set_author(name='User ID')
        show_id.set_footer(text=f'{member}', icon_url=f'{member.avatar_url}')
        await ctx.send(embed=show_id)

    @commands.command(name='avatar', help='returns avatar of member')
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        show_avatar = discord.Embed(color=discord.Color.gold())
        show_avatar.set_image(url=f'{member.avatar_url}')
        show_avatar.set_footer(text=f'{member}', icon_url=f'{member.avatar_url}')
        await ctx.send(embed=show_avatar)

    @commands.command(name='poll', help='creates a poll with maximum 5 options')
    async def poll(self, ctx, *args):

        if 3 <= len(args) <= 6:

            embed = discord.Embed(color=discord.Color.gold(), title=f'{args[0]}')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.description = f':one: {args[1]}\n\n:two: {args[2]}'

            if len(args) >= 4:
                embed.description += f'\n\n:three: {args[3]}'

                if len(args) >= 5:
                    embed.description += f'\n\n:four: {args[4]}'

                    if len(args) >= 6:
                        embed.description += f'\n\n:five: {args[5]}'

            msg = await ctx.send(embed=embed)

            await msg.add_reaction('1⃣')
            await msg.add_reaction('2⃣')

            if len(args) >= 4:
                await msg.add_reaction('3⃣')

                if len(args) >= 5:
                    await msg.add_reaction('4⃣')

                    if len(args) >= 6:
                        await msg.add_reaction('5⃣')

        elif len(args) < 3:

            embed = discord.Embed(color=discord.Color.light_grey())
            embed.add_field(name='You did not include enough arguments to make a poll.',
                            value='An example of a proper use of the command is: \n .poll "Are you Canadian?" Yes No')
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(color=discord.Color.light_grey())
            embed.add_field(name='You included too many arguments to make a poll.',
                            value='An example of a proper use of the command is: \n .poll "Are you Canadian?" Yes No')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
