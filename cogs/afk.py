import disnake
from disnake.ext import commands


'''
Tables
role_data (guild_id integer, member_role text, admin_role, mod_role)
afk (guild_id integer, afk_sys integer)
level (guild_id integer, level_sys integer)
mutes (guild_id int, user_id int, admin_id int)
warns (guild_id int, user_id int, admin_id, int, reason text, time int, id int)
level_data (guild_id int, user_id int, exp int, level int)
afk_data (user_id int NOT NULL UNIQUE, reason int, time int)
'''


class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot








    @commands.command(help = 'Sets your afk.')
    async def afk(self, ctx, *, reason='AFK'):
        servers = self.bot.servers
        c = await servers.execute('SELECT afk FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        afk = data[0]
        if afk == 1:

            msg_time = ctx.message.created_at
            timestamp = str(msg_time.timestamp())
            try:
                await ctx.author.edit(nick = 'AFK~'+ ctx.author.display_name)
                await ctx.send('{} Your afk is now set.'.format(ctx.author.mention))
                await servers.execute("INSERT INTO afk_data VALUES (:user_id, :reason, :time)", {'user_id':ctx.author.id, 'reason':reason, 'time':int(timestamp[:-4])})
            except disnake.Forbidden:
                await ctx.send('{} Your afk is now set.'.format(ctx.author.mention))
                await servers.execute("INSERT INTO afk_data VALUES (:user_id, :reason, :time)", {'user_id':ctx.author.id, 'reason':reason, 'time':int(timestamp[:-4])})
        else:
            await ctx.send('Your server admins have disabled this system.')
        
        
        








    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        servers = self.bot.servers
        
        c = await servers.execute('SELECT afk FROM systems WHERE guild_id = :guild_id', {'guild_id':message.guild.id})
        data = await c.fetchone()
        afk = data[0]
        if afk == 1:
            author = message.author

            if message.content.startswith('`afk'):
                return
            if message.author.bot:
                return
            if message.guild is None:
                print(message.content)
                return

            c = await servers.execute('SELECT * FROM afk_data WHERE user_id = :user_id', {'user_id':author.id})
            afk = await c.fetchone()



            if not afk:
                for mention in message.mentions:
                    c = await servers.execute('SELECT * FROM afk_data WHERE user_id = :user_id',{'user_id':mention.id})
                    data = await c.fetchone()
                    if not data:
                        return
                    user, reason, time = data
                    await message.channel.send('{} has been afk since <t:{}:R> because: {}'.format(mention.display_name, time, reason))


            else:
                user, reason, time = afk

                try:

                    await author.edit(nick = author.display_name[4:])
                    await message.channel.send('I have removed your afk {}. Welcome back!'.format(author.mention))
                    await servers.execute('DELETE FROM afk_data WHERE user_id = :user_id', {'user_id':author.id})

                except disnake.Forbidden:
                    await message.channel.send('I have removed your afk {}. Welcome back!'.format(author.mention))
                    await servers.execute('DELETE FROM afk_data WHERE user_id = :user_id', {'user_id':author.id})
        else:
            
            return 
        
        
            
            
        
        
                    
                
        

        




def setup(bot):
    bot.add_cog(AFK(bot))