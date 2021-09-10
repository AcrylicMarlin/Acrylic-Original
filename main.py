import discord
from discord.ext import commands
import os
import asyncio
import asqlite
import traceback
import sys
import postbin
from dotenv import load_dotenv
load_dotenv
os.chdir('C:\\Users\\justi\\OneDrive\\Documents\\Acrylic')
bot = commands.Bot(command_prefix="a'", intents = discord.Intents.all())


bot.help_command = None





async def initialise():
    await bot.wait_until_ready()
    bot.servers = await asqlite.connect('guild_data.db')

    for guild in bot.guilds:
        c = await bot.servers.execute('SELECT * FROM systems WHERE guild_id = :guild_id', {'guild_id':guild.id})
        data = await c.fetchone()
        if data is None:
            await bot.servers.execute('INSERT INTO systems VALUES (:guild_id, 1, 1, 1, 1, 1, 1)', {'guild_id':guild.id})

    

    
    
    
    
    




@bot.event
async def on_ready():
    print(
'''{} is online
I am connected to {} servers.'''.format(bot.user.name, len(bot.guilds)))

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('{} does not exist as a command.'.format(ctx.message.content))
        return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Member does not exist in this server.')
        return
    if isinstance(error, commands.RoleNotFound):
        await ctx.send('This role does not exist in this server.')
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error, delete_after = 3.0)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing something in this command.')
        return
    if isinstance(error, commands.CommandInvokeError):
        error = getattr(error, 'original', error)
        if isinstance(error, AttributeError):
            await ctx.send('You forgot something in this command.')
            return
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

   


@bot.command(hidden = True)
async def test(ctx):
    em = discord.Embed(
            title = 'This is the help panel for my commands.',
            description= '''
            This is a list of all my categories. Select a button to go to that category's list of commands.
            *(These panels change depending on which systems you have enabled. If you don't know what this means, see Configuration.)*
            
            ***Moderation***
                *All of the moderation commands.*

            ***Server Configuration***
                *All of the server configuration commands.*

            ***Level***
                *All of the level commands and how this system works.*

            ***AFK***
                *All of the afk commands and how this system works.*

            ***Configuration***
                *All of the configuration commands.*
            
            ***Extra Commands***
                *All of the extra commands.*'''
            
        )
    await ctx.send(embed=em)


async def db_schema(*tables):
    n = "\n"
    schema = await (
        await bot.warn_db.execute(
            f"SELECT sql FROM sqlite_master"
            + (
                " WHERE name IN ({})".format(
                    ", ".join(f"'{table}'" for table in tables)
                )
                if tables
                else ""
            )
        )
    ).fetchall()
    return f"```sql\n{n.join([''.join(x) for x in schema if any(x) and not x[0].startswith('sqlite_autoindex')])}```"

bot.db_schema = db_schema

@bot.command(hidden = True)
@commands.is_owner()
async def schema(ctx: commands.Context, *tables):
    s = await bot.db_schema('warn_data')
    await ctx.send(
        embed=discord.Embed(
            title="Schema" + (" for " + ", ".join(tables) if tables else ""),
            description=s if len(s) <= 4096 else await postbin.postAsync(s),
            color=discord.Color.random(),
        )
    )






for cog in os.listdir('./cogs'):
    if cog.endswith('.py') and not cog.startswith('_'):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded:")
            raise e



bot.loop.create_task(initialise())

bot.run(os.environ.get('TOKEN'))
