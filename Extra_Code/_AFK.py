import discord
from discord.ext import commands
import aiosqlite

conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('''CREATE TABLE Afk_Users (
    User_id integer,
    Reason text)''')


class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def afk(self, ctx, *, reason=None):
        

        with conn:
            c.execute("INSERT INTO Afk_Users VALUES (:User_id, :Reason)", {'User_id' : ctx.author.id, 'Reason':reason})
        
        await ctx.send('{} I have set your AFK: {}'.format(ctx.author.mention, reason))

    @commands.Cog.listener()
    async def on_message(self, message):
        afk = c.execute('SELECT * FROM Afk_Users WHERE User_id = :User_id',{'User_id': message.author.id}).fetchall()
        if not afk:
            return
        
        if message.author.id in afk:
            await message.channel.send('Your AFK has been removed {}. Welcome back!'.format(message.author.mention))
            with conn:
                c.execute('DELETE * FROM Afk_Users WHERE User_id = :User_id', {'User_id':message.author.id})


        
        else:
            mentions = message.mentions
            for mention in mentions:
                users = c.execute('SELECT User_id FROM Afk_Users').fetchall()
                if mention.id in users:
                    users, reason = c.execute('SELECT User_id Reasons FROM Afk_Users').fetchall()
                    await message.channel.send('{} is afk because: {}'.format(mention.display_name, reason))

    
def setup(bot):
    bot.add_cog(AFK(bot))