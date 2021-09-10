import discord
from discord.ext import commands



em = discord.Embed(
                title = 'Welcome Setup',
                description="Follow the Instructions"
            )

class welcomeLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    

    @commands.group()
    async def setup(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply('You gotta tell me what you want to setup.')
        
    @setup.command()
    async def welcome(self, ctx):
        
        em.add_field(name = 'Step One:', value='What channel would you like to have welcome/leave notifs? (The channel must be spelled exactly as it is spelled)')
        await ctx.reply(embed = em)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while True:

            msg = await self.bot.wait_for('message', check=check)
            channel = discord.utils.get(ctx.guild.channels, name = msg.content)
            if channel is None:
                await msg.reply("This channel doesn't exist, try again.")
                continue
            else:
                await msg.reply('Great Moving to the next step.')
                break

def setup(bot):
    bot.add_cog(welcomeLeave(bot))