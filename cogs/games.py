import discord
import random
from discord.ext import commands


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coinflip', help='flips a coin', aliases=['cf'])
    async def coinflip(self, ctx):
        embed = discord.Embed(color=discord.Color.gold())

        result = random.randint(0, 1)

        if result == 0:
            embed.set_image(url=f'https://cdn.discordapp.com/attachments/254009811216105473/779829162097377290/tails.png')
            embed.set_footer(text='Tails')
        else:
            embed.set_image(url=f'https://cdn.discordapp.com/attachments/254009811216105473/779829170154897473/heads.png')
            embed.set_footer(text='Heads')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Games(bot))
