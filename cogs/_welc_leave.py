import discord
from discord.ext import commands





class welcomeLeave(commands.cog):
    def __init__(self, bot):
        self.bot = bot


    

    @commands.group()
    async def setup(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply('You gotta tell me what you want to setup.')
        
    @setup.command()
    async def welcome(self, ctx):
        em = discord.Embed(
            title = 'Welcome Setup',
            description="Follow the Instructions"
        )
        em.add_field(name = 'First: ')