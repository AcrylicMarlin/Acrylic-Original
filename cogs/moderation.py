import sys
import traceback
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import datetime



class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    





    
    @commands.slash_command()
    @commands.has_permissions(manage_guild = True)
    async def warn(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(
        name = 'member',
        description = 'member to warn'),
    reason:str = Param(
        None,
        name = 'reason',
        description = 'Reason for warn (defaults to None)')):
        servers = self.bot.servers
        
        
        timestamp = str(inter.message.created_at.timestamp())
        
        guild = inter.guild
        user = inter.author
        if member == inter.author:
            await inter.response.send_message('You cannot warn yourself')
            return
        if member == self.bot.user:
            await inter.response.send_message('You cannot warn the bot')
            return
        
        await servers.execute('INSERT INTO warns VALUES (:guild_id, :user_id, :admin_id, :reason, :time)', {'guild_id':guild.id, 'user_id':member.id, 'admin_id':user.id, 'reason':reason, 'time':timestamp[:-4]})
        await inter.response.send_message('{} has been warned by {} for {}.'.format(member.display_name, inter.author.display_name, reason))
        await member.send('You have been warned in {} for {}. Warn Issuer: {}'.format(inter.guild.name, reason, user.display_name))
            

    
        






        
    @commands.slash_command()
    @commands.has_permissions(manage_guild=True)
    async def get_warns(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(
        name = 'member',
        description = 'member to get warns for')):
        servers = self.bot.servers
        
        


             
        data = await servers.execute('SELECT admin_id, reason, time FROM warns WHERE guild_id = :guild_id AND user_id = :user_id',{'guild_id':inter.guild.id, 'user_id':member.id})
        warns = await data.fetchall()
        i = 1
        em = disnake.Embed(title = "***{}'s Warnings***".format(member.display_name))
        for item in warns:
            admin, warning, time = item
            admin = inter.guild.get_member(admin)
            

            
            
            em.add_field(name='Warning {}'.format(i), value = '{} ~~{}  <t:{}:f>'.format(warning, admin.display_name, time), inline = False)
            i += 1
        # em.set_thumbnail(url=member.avatar_url)
        await inter.response.send_message(embed=em)










    @commands.slash_command()
    @commands.has_guild_permissions(administrator=True)
    async def clear_warns(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(
        name = 'member',
        description = 'member to clear warns from')):
        
        if member == inter.author:
            await inter.response.send_message("You can't clear your own warns.")
            return
        if member == self.bot.user:
            await inter.response.send_message("You can't clear my warns if I can't be warned.")
            return
        def check(m):
            return m.author == inter.author and m.channel == inter.channel
        await inter.response.send_message("Are you sure you want to clear {}'s warns?".format(member.display_name))
        msg=await inter.original_message()
        ms = await self.bot.wait_for('message', check = check)
        if ms.content == 'yes' or ms.content == 'Yes':
            await inter.reply('Ok, just checking.')
            await msg.delete()
            await self.bot.servers.execute('DELETE FROM warns WHERE guild_id = :guild_id AND user_id = :user_id',{'guild_id':inter.guild.id, 'user_id':member.id})

            try:
                await member.send('Your warns have been cleared in {}. You are a lucky person {}.'.format(inter.guild.name, member.display_name))
                await inter.response.send_message("Cleared {}'s warns.".format(member.display_name))
            except disnake.Forbidden:
                await inter.response.send_message("Cleared {}'s warns.".format(member.display_name))

        elif ms.content == 'no' or ms.content == 'No':
            await msg.delete()
            await inter.channel.send('Thank god I asked right? XD')
        else:
            await msg.delete()
            await inter.channel.send('I need a yes or a no. Canceling...')
            









    @commands.slash_command()
    @commands.has_permissions(manage_guild = True)
    async def delete_warn(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(
        name='member',
        description='mamber to delete a warn from')):
        servers = self.bot.servers

        
        try:
            await inter.response.send_message('You have removed a warn from {}.'.format(member.display_name))
            await member.send('A warn has been removed from your list in {}. Use this chance wisely {}.'.format(inter.guild.name, member.display_name))
        
        except disnake.Forbidden:
            await inter.response.send_message('You have removed a warn from {}.'.format(member.display_name))
            
        await servers.execute('''DELETE FROM warns WHERE guild_id = :guild_id AND user_id=:user_id AND time = (SELECT MAX(time) FROM warns)''', {'guild_id':inter.guild.id, 'user_id':member.id})
        

    






    













    @commands.slash_command()
    @commands.has_permissions(kick_members = True)
    async def kick(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(
        name = 'member',
        description='member to kick'),
    reason:str = Param(
        None,
        name = 'reason',
        description='reason for kick (defaults to none)')):
        if member == inter.author:
            await inter.response.send_message("You can't kick yourself.")
            return
        

        await inter.response.send_message("{} has been kicked for {}.".format(member.display_name, reason))
        try:

            await member.send('You have been kicked from {} for {}'.format(inter.guild.name, reason))
        except disnake.Forbidden:
            await inter.response.send_message('Dm Failed')
        except disnake.HTTPException:
            await inter.response.send_message('Dm Failed')
        
        await inter.guild.kick(member)
        










    @commands.slash_command()
    @commands.has_permissions(ban_members = True)
    async def ban(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member = Param(
        name='name',
        description='member to ban'),
    reason:str = Param(
        None,
        name = 'reason',
        description='reason for banning (defaults to none)')):
        if member == inter.author:
            await inter.response.send_message('You cannot ban yourself.')
            return
        if member == self.bot.user:
            await inter.response.send_message('You cannot ban me mortal.')
            return
        
        try:
            await member.send('You were banned from {} for {}'.format(inter.guild.name, reason))
            await inter.response.send_message('{} was banned from {} for {}'.format(member.display_name, inter.guild.name, reason))
        except disnake.Forbidden:
            await inter.response.send_message('{} was banned from {} for {}'.format(member.display_name, inter.guild.name, reason))
        
        await inter.guild.ban(member)
    
    @ban.error
    async def ban_error(self, inter, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await inter.response.send_message('You either forgot to specify a member or forgot to give a reason.')
            return
        if isinstance(error, commands.MemberNotFound):
            await inter.response.send_message('Member is not found.')
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        














    @commands.slash_command(name='unban-by-id')
    @commands.has_permissions(ban_members = True)
    async def unbanID(self,
    inter:disnake.ApplicationCommandInteraction,
    member:int = Param(
        name = 'id',
        description = 'ID of the member')):
        await inter.guild.unban(disnake.Object(id=member))
        await inter.response.send_message('They have unbanned.')
        user = self.bot.get_user(member)
        inv = await inter.channel.create_invite()
        await user.send('You have been unbanned from {}. Here is a invite if you would like to rejoin.\n{}'.format(inter.guild.name, inv.url))
    @unbanID.error
    async def unban_error(self,inter,error):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message('Attempt to DM user of unban failed.')
            return
        if isinstance(error, commands.CommandInvokeError):
            await inter.response.send_message('Failed to DM user of Unban')
            return
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        
    @commands.slash_command(
        name = 'unban-by-name-discrim',
        description='Unbans by using this format: username#discriminator (do not ping)')
    @commands.has_permissions(ban_members = True)
    async def unbanUserDiscrim(
        self,
        inter:disnake.ApplicationCommandInteraction,
        member:str = Param(
            name = 'member',
            description='Username#Discriminator')):

        member_name, member_discrim = member.split('#')
        if len(member_discrim) != 4 : return await inter.response.send_message("The member needs to have a 4 digit discriminator")

        banList = await inter.guild.bans()
        for item in banList:
            if member_name == item.user.name and member_discrim == item.user.discriminator:
                await inter.guild.unban(item.user)
                await inter.response.send_message('{} was unbanned'.format(item.user.mention))
                inv = await inter.channel.create_invite()
                await item.user.send('You have been unbanned from {}. Here is a invite if you would like to rejoin.\n{}'.format(inter.guild.name, inv.url))
                break



   


    @commands.slash_command()
    @commands.has_permissions(manage_messages = True)
    async def mute(
        self,
        inter:disnake.ApplicationCommandInteraction,
        member:disnake.Member=Param(
            name = 'member',
            description = 'member to ban'),
        reason:str=Param(
            None,
            name = 'reason',
            description = 'reason for mute (defaults to None)'
        )):
        servers  = self.bot.servers
        c = await servers.execute('SELECT mute FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        mute = data[0]
        msg_time = inter.message.created_at
        
        timestamp = str(msg_time.timestamp())
        if member == inter.author:
            await inter.response.send_message("You can't mute yourself.")
            return
        if mute:
            await inter.response.send_message('This member is already muted.')
            return
        guild = inter.guild
        muteRole = disnake.utils.get(guild.roles, name='Muted')

        if not muteRole:
            muteRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(muteRole, send_messages=False, read_message_history = False)

        await servers.execute('INSERT INTO mutes VALUES (:guild_id, :user_id, :admin_id, :reason, :time)',{'guild_id':inter.guild.id, 'user_id':member.id, 'admin_id':inter.author.id, 'reason':reason, 'time':timestamp[:-4]})
        await member.add_roles(muteRole, reason=reason)
        await inter.response.send_message('{} was muted for {}.'.format(member.display_name, reason))
        await member.send('You were muted in server {} for {}.'.format(guild.name, reason))


    









    @commands.slash_command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self,
    inter:disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(
        name='member',
        description='member to unmute'
    )):
        servers  = self.bot.servers
        c = await servers.execute('SELECT user_id FROM mutes WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':inter.guild.id, 'user_id':member.id})
        mute = await c.fetchone()
        
        
        if not mute:
            await inter.response.send_message('This member is not muted.')
            return

        await servers.execute('DELETE FROM mutes WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':inter.guild.id, 'user_id':member.id})
        mutedRole = disnake.utils.get(inter.guild.roles, name = 'Muted')
        await member.remove_roles(mutedRole)

        await member.send('You were unmuted in {}'.format(inter.guild.name))
        await inter.response.send_message('{} was unmuted.'.format(member.display_name))
    
    












    

    @commands.slash_command(name='get-mutes')
    @commands.has_permissions(manage_messages = True)
    async def get_mutes(
        self,
        inter:disnake.ApplicationCommandInteraction):
        servers  = self.bot.servers
        c = await servers.execute('SELECT user_id, admin_id, reason, time FROM mutes WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})

        data = await c.fetchall()
        em = disnake.Embed(title = "{}'s mutes".format(inter.guild.name))
        for item in data:
            user, admin, reason, time = item

            user = disnake.utils.get(inter.guild.members, id = user)
            admin = disnake.utils.get(inter.guild.members, id = admin)

            

            em.add_field(name = '{}'.format(user.display_name), value = "Muted at <t:{}:f> for {}. ~~{}".format(time, reason, admin.display_name), inline = False)

        if inter.guild.icon is not None:
            em.set_thumbnail(url = inter.guild.icon.url)
        await inter.response.send_message(embed = em)



        

    



            





            





def setup(bot):
    bot.add_cog(Moderation(bot))
