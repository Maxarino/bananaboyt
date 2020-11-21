import discord
import os
try:
    import hiddentoken
except:
    pass
from discord.ext import commands, tasks

token = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

# EVENTS


@bot.event
async def on_ready():

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception:
                print(f'\nCouldn\'t load cog {filename[:-3]}')

    print(f'\nSuccessfully logged in as {bot.user}\n')
    print(f'{bot.user} is connected to the following servers:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print()

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game('LittleBigPlanet 2'))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You don\'t have the correct role for this command.')


# COMMANDS


def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 151715434306076672  # My User ID
    return commands.check(predicate)


@bot.command(name='load', hidden=True, aliases=['ld'])
@is_me()
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'The extension {extension} has been loaded successfully.')
    except Exception:
        await ctx.send(f'Error loading the cog {extension}.')


@bot.command(name='unload', hidden=True, aliases=['unld'])
@is_me()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'The extension {extension} has been unloaded successfully.')
    except Exception:
        await ctx.send(f'Error unloading the cog {extension}.')


@bot.command(name='reload', hidden=True, aliases=['rld'])
@is_me()
async def reload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'The extension {extension} has been reloaded successfully.')
    except Exception:
        await ctx.send(f'Error reloading the cog {extension}.')


@bot.command(name='stop', hidden=True)
@is_me()
async def stop(ctx):
    await bot.logout()


if __name__ == '__main__':
    try:
        bot.run(hiddentoken.token)
    except:
        bot.run(str(token))