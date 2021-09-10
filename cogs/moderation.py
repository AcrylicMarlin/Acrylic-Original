import sys
import traceback
import discord
from discord.ext import commands
import datetime

'''
Tables
role_data (guild_id integer, member_role text, admin_role, mod_role)
afk (guild_id integer, afk_sys integer)
level (guild_id integer, level_sys integer)
mutes (guild_id int, user_id int, admin_id int, time int)
warns (guild_id int, user_id int, admin_id, reason text, time int)
level_data (guild_id int, user_id int, exp int, level int)
afk_data (user_id int NOT NULL UNIQUE, reason int, time int)
'''


class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    





    
    @commands.command(
        help = 'Warns a user for your reason.'
    )
    @commands.has_permissions(manage_guild = True)
    async def warn(self, ctx, member:discord.Member=None, *, reason=None):
        servers = self.bot.servers
        msg_time = ctx.message.created_at
        
        timestamp = str(msg_time.timestamp())
        
        guild = ctx.guild
        user = ctx.author
        if member == ctx.author:
            await ctx.send('You cannot warn yourself')
            return
        if member == self.bot.user:
            await ctx.send('You cannot warn the bot')
            return
        
        await servers.execute('INSERT INTO warns VALUES (:guild_id, :user_id, :admin_id, :reason, :time)', {'guild_id':guild.id, 'user_id':member.id, 'admin_id':user.id, 'reason':reason, 'time':timestamp[:-4]})
        await ctx.send('{} has been warned by {} for {}.'.format(member.display_name, ctx.author.display_name, reason))
        await member.send('You have been warned in {} for {}. Warn Issuer: {}'.format(ctx.guild.name, reason, user.display_name))
            

    
        






        
    @commands.command(
        aliases = ['getwarns', 'gw'],
        help = 'Gets the warns of a certain user.')
    @commands.has_permissions(manage_guild=True)
    async def get_warns(self, ctx, member:discord.Member=None):
        servers = self.bot.servers
        if member is None:
                await ctx.send('Specify a member.')
                return
        


             
        data = await servers.execute('SELECT admin_id, reason, time FROM warns WHERE guild_id = :guild_id AND user_id = :user_id',{'guild_id':ctx.guild.id, 'user_id':member.id})
        warns = await data.fetchall()
        i = 1
        em = discord.Embed(title = "***{}'s Warnings***".format(member.display_name))
        for item in warns:
            admin, warning, time = item
            admin = ctx.guild.get_member(admin)
            

            
            
            em.add_field(name='Warning {}'.format(i), value = '{} ~~{}  <t:{}:f>'.format(warning, admin.display_name, time), inline = False)
            i += 1
        # em.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=em)










    @commands.command(
        aliases = ['clearwarns', 'cw'],
        help = 'Clears the warns of a certain user. (You will be prompted to confirm if you would like to do this.)')
    @commands.has_guild_permissions(administrator=True)
    async def clear_warns(self, ctx, member:discord.Member=None):
        
        if member == ctx.author:
            await ctx.send("You can't clear your own warns.")
            return
        if member == self.bot.user:
            await ctx.send("You can't clear my warns if I can't be warned.")
            return
        if member == None:
            await ctx.send('Who are you clearing?')
            return
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await ctx.send("Are you sure you want to clear {}'s warns?".format(member.display_name))
        ms = await self.bot.wait_for('message', check = check)
        if ms.content == 'yes' or ms.content == 'Yes':
            await ctx.reply('Ok, just checking.')
            await msg.delete()
            await self.bot.servers.execute('DELETE FROM warns WHERE guild_id = :guild_id AND user_id = :user_id',{'guild_id':ctx.guild.id, 'user_id':member.id})

            try:
                await member.send('Your warns have been cleared in {}. You are a lucky person {}.'.format(ctx.guild.name, member.display_name))
                await ctx.send("Cleared {}'s warns.".format(member.display_name))
            except discord.Forbidden:
                await ctx.send("Cleared {}'s warns.".format(member.display_name))

        elif ms.content == 'no' or ms.content == 'No':
            await msg.delete()
            await ctx.reply('Thank god I asked right? XD')
        else:
            await msg.delete()
            await ctx.reply('I need a yes or a no. Canceling...')
            









    @commands.command(
        aliases = ['dw', 'delwarn', 'deletewarn'],
        help = 'Deletes a warn from a user.')
    @commands.has_permissions(manage_guild = True)
    async def delete_warn(self, ctx, member:discord.Member):
        servers = self.bot.servers

        
        try:
            await ctx.send('You have removed a warn from {}.'.format(member.display_name))
            await member.send('A warn has been removed from your list in {}. Use this chance wisely {}.'.format(ctx.guild.name, member.display_name))
        
        except discord.Forbidden:
            await ctx.send('You have removed a warn from {}.'.format(member.display_name))
            
        await servers.execute('''DELETE FROM warns WHERE guild_id = :guild_id AND user_id=:user_id AND time = (SELECT MAX(time) FROM warns)''', {'guild_id':ctx.guild.id, 'user_id':member.id})
        

    






    













    @commands.command(
        help = 'Kicks a user from the server.'
    )
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.Member=None, *, reason = None):
        if member == None:
            await ctx.send("I can't kick what I can't see")
            return
        if member == ctx.author:
            await ctx.send("You can't kick yourself.")
            return
        if reason == None:
            await ctx.send('Please give a reason for your action.')
            return

        await ctx.send("{} has been kicked for {}.".format(member.display_name, reason))
        try:

            await member.send('You have been kicked from {} for {}'.format(ctx.guild.name, reason))
        except discord.Forbidden:
            await ctx.send('Dm Failed')
        except discord.HTTPException:
            await ctx.send('Dm Failed')
        
        await ctx.guild.kick(member)
        










    @commands.command(
        help = 'Bans a user from the server.'
    )
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.Member, *, reason):
        if member == ctx.author:
            await ctx.send('You cannot ban yourself.')
            return
        if member == self.bot.user:
            await ctx.send('You cannot ban me mortal.')
            return
        if reason is None:
            await ctx.send('Why are you banning this person?')
            return
        try:
            await member.send('You were banned from {} for {}'.format(ctx.guild.name, reason))
            await ctx.send('{} was banned from {} for {}'.format(member.display_name, ctx.guild.name, reason))
        except discord.Forbidden:
            await ctx.send('{} was banned from {} for {}'.format(member.display_name, ctx.guild.name, reason))
        
        await ctx.guild.ban(member)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You either forgot to specify a member or forgot to give a reason.')
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('Member is not found.')
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        














    @commands.command(
        help = 'Unbans a user from a server.'
    )
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        await ctx.guild.unban(discord.Object(id=member))
        await ctx.send('They have unbanned.')
        user = self.bot.get_user(member)
        inv = await ctx.channel.create_invite()
        await user.send('You have been unbanned from {}. Here is a invite if you would like to rejoin.\n{}'.format(ctx.guild.name, inv.url))
    @unban.error
    async def unban_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Attempt to DM user of unban failed.')
            return
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Failed to DM user of Unban')
            return
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        

                    

    


    @commands.command(
        help = 'Mutes a user.'
    )
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member:discord.Member=None, * , reason=None):
        servers  = self.bot.servers
        c = await servers.execute('SELECT mute FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        mute = data[0]
        msg_time = ctx.message.created_at
        
        timestamp = str(msg_time.timestamp())
        if member == ctx.author:
            await ctx.send("You can't mute yourself.")
            return
        if member == None:
            await ctx.send("Specify who you would like to mute.")
            return
        if mute:
            await ctx.send('This member is already muted.')
        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name='Muted')

        if not muteRole:
            muteRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(muteRole, send_messages=False, read_message_history = False)

        await servers.execute('INSERT INTO mutes VALUES (:guild_id, :user_id, :admin_id, :reason, :time)',{'guild_id':ctx.guild.id, 'user_id':member.id, 'admin_id':ctx.author.id, 'reason':reason, 'time':timestamp[:-4]})
        await member.add_roles(muteRole, reason=reason)
        await ctx.send('{} was muted for {}.'.format(member.display_name, reason))
        await member.send('You were muted in server {} for {}.'.format(guild.name, reason))


    









    @commands.command(
        help = 'Unmutes a member.'
    )
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member:discord.Member=None):
        servers  = self.bot.servers
        c = await servers.execute('SELECT user_id FROM mutes WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':ctx.guild.id, 'user_id':member.id})
        mute = await c.fetchone()
        if member is None:
            await ctx.send("Specify a member to unmute.")
            return
        
        if not mute:
            await ctx.send('This member is not muted.')
            return

        await servers.execute('DELETE FROM mutes WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':ctx.guild.id, 'user_id':member.id})
        mutedRole = discord.utils.get(ctx.guild.roles, name = 'Muted')
        await member.remove_roles(mutedRole)

        await member.send('You were unmuted in {}'.format(ctx.guild.name))
        await ctx.send('{} was unmuted.'.format(member.display_name))
    
    












    

    @commands.command(
        aliases = ['gm', 'getmutes'],
        help = 'Gets all the muted users for this server.')
    @commands.has_permissions(manage_messages = True)
    async def get_mutes(self, ctx):
        servers  = self.bot.servers
        c = await servers.execute('SELECT user_id, admin_id, reason, time FROM mutes WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})

        data = await c.fetchall()
        em = discord.Embed(title = "{}'s mutes".format(ctx.guild.name))
        for item in data:
            user, admin, reason, time = item

            user = discord.utils.get(ctx.guild.members, id = user)
            admin = discord.utils.get(ctx.guild.members, id = admin)

            

            em.add_field(name = '{}'.format(user.display_name), value = "Muted at <t:{}:f> for {}. ~~{}".format(time, reason, admin.display_name), inline = False)

        if ctx.guild.icon is not None:
            em.set_thumbnail(url = ctx.guild.icon.url)
        await ctx.send(embed = em)



        

    



            





            





def setup(bot):
    bot.add_cog(Moderation(bot))
