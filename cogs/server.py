from ast import Str
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import traceback
import sys
import typing
# This is my own folder containing views
from Things import yesNo



class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    



    @commands.slash_command(name = 'add-member-role')
    @commands.has_permissions(manage_roles = True)
    async def add_member_role(
        self,
        inter:disnake.ApplicationCommandInteraction,
        member:disnake.Member=Param(
            name = 'member',
            description='member to add role to'
        ),
        role:disnake.Role=Param(
            name = 'role',
            description='Role to give'
        )):
        
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:
            if role != disnake.Role:
                try:
                    role = disnake.utils.get(inter.guild.roles, name=role)
                    await member.add_roles(role)
                    await inter.response.send_message('Added the role to {}.'.format(member.display_name))
                except:
                    await inter.response.send_message("This role doesn't exist. Try Again.")
                    return
            else:
                await member.add_roles(role)
                await inter.response.send_message('Added the role to {}.'.format(member.display_name))
        else:
            await inter.response.send_message('Your server admins have disabled this system.')
    
    








    @commands.slash_command(name='remove-member-role')
    @commands.has_permissions(manage_roles = True)
    async def remove_member_role(
        self,
        inter:disnake.ApplicationCommandInteraction,
        member:disnake.Member=Param(
            name = 'member',
            description='member to remove a role from'
        ),
        role:disnake.Role = Param(
            name='role',
            description='role to remove'
        )):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:
            if role != disnake.Role:
                try:

                    role = disnake.utils.get(inter.guild.roles, name=role)
                    await member.remove_roles(role)
                    await inter.response.send_message('Role removed from {}'.format(member.display_name))
                
                except:
                    await inter.response.send_message("This role doesn't exit")
                    return


            else:
                await member.remove_roles(role)
                await inter.response.send_message('Role removed from {}'.format(member.display_name))




        else:
            await inter.response.send_message('Your server admins have disabled this system.')













    @commands.slash_command(name='add-server-role')
    @commands.has_permissions(manage_roles = True)
    async def add_server_role(
        self,
        inter:disnake.ApplicationCommandInteraction,
        role:str=Param(
            name='role',
            description='name of role to add'
        )):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            role = await inter.guild.create_role(name = role)        
            await inter.response.send_message("{} role successfully created. Use `a'amr` to add the role to someone.".format(role.mention))
        else:
            await inter.response.send_message('Your server admins have disabled this system.')














    @commands.slash_command(name='remove-server-role')
    @commands.has_permissions(manage_roles = True)
    async def remove_server_role(
        self,
        inter:disnake.ApplicationCommandInteraction,
        role:disnake.Role=Param(
            name='role',
            description='role to remove'
        )):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:
            if role != disnake.Role:


                try:
                    role = disnake.utils.get(inter.guild.roles, name = role)
                    await role.delete()
                    await inter.response.send_message('The role has been deleted from the server.')
                except:
                    inter.response.send_message("This role doesn't Exist")
                    return

            else:
                await role.delete()
                await inter.response.send_message('The role has been deleted from the server.')
        else:
            await inter.response.send_message('Your server admins have disabled this system.')




    









    @commands.slash_command(name='add-channel')
    @commands.has_permissions(manage_channels = True)
    async def add_channel(
        self,
        inter:disnake.ApplicationCommandInteraction,
        channel:str=Param(
            name='channel-name',
            description='Name of new channel'

        ),
        category:str=Param(
            name='category-name',
            description='Category to add the channel to.'
        )):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            check = disnake.utils.get(inter.guild.categories, name=category)
            if check is None:
                await inter.response.send_message("The category provided doesn't exist. Would you like to make the channel still?", view = yesNo(channel))
            else:
                channel = await inter.guild.create_text_channel(name = channel, category=check)
                await channel.send(f'{inter.author.mention} Channel Created!')
        else:
            await inter.response.send_message('Your server admins have disabled this system.')
    @add_channel.error
    async def ac_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message('You dont have permission to do thisresponse.send_message')



















           
    @commands.slash_command(name = 'add-category')
    @commands.has_permissions(manage_channels = True)
    async def add_category(
        self,
        inter:disnake.ApplicationCommandInteraction,
        name:str=Param(name = 'category-name', description='name of the category to create')):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            cat = await inter.guild.create_category(name = name)
            await inter.response.send_message('Category {} added.'.format(cat.mention))

        else:

            await inter.response.send_message('Your server admins have disabled this system.')


    @add_category.error
    async def acat_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.channel.send('You dont have permission to do this.')
        
















    
    @commands.slash_command(name = 'delete-category')
    @commands.has_permissions(manage_channels = True)
    async def delete_category(
        self,
        inter:disnake.ApplicationCommandInteraction,
        name:str=Param(name='category-name', description='name of category to remove (must be typed exactly)')):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            cat = disnake.utils.get(inter.guild.categories, name = name)
            await cat.delete()
            await inter.response.send_message('Category deleted.')
        else:
            await inter.response.send_message('Your server admins have disabled this system.')





    @delete_category.error
    async def dcat_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.channel.send('You dont have permission to do this.')
        if isinstance(error, commands.CommandInvokeError):
            await inter.channel.send('This name does not exist in this server. Remember to type it exactly.')

    

















    @commands.slash_command(name='delete-channel')
    @commands.has_permissions(manage_channels = True)
    async def delete_channel(
        self,
        inter:disnake.ApplicationCommandInteraction,
        name:str=Param(name='channel-name', description='Name of channel to remove (must be spelled exactly)')):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:
            
            chan = disnake.utils.get(inter.guild.channels, name = name)
            if chan is None:
                await inter.response.send_message("This channel doesn't exist")
                return
            await chan.delete()
            await inter.response.send_message('Channel deleted.')
        else:
            await inter.response.send_message('Your server admins have disabled this system.')


    @delete_channel.error
    async def dc_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.channel.send('You dont have permission to do this.')



    @commands.slash_command()
    @commands.cooldown(rate = 1, per = 5.0)
    @commands.has_permissions(manage_messages = True)
    async def purge(
        self,
        inter:disnake.ApplicationCommandInteraction,
        amount:str = Param(5, name='amount', description='Amount of messages to purge (defaults to 5)')):
        if amount <= 25:

            await inter.message.delete()
            await inter.channel.purge(limit = amount)
        else:
            await inter.response.send_message('The maximum amount of messages you can purge is 25!')














    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print('I joined a new guild named {}!'.format(guild.name))
        em = disnake.Embed(title = 'Thank you for choosing Acrylic.',
        description = "Thank you so much for allowing me to be a part of your server. My creator worked long and hard for this.\nTo begin use the command `a'help` for a list of commands.")
        try:
            await guild.owner.send(embed = em)
            
        
        except disnake.Forbidden:
            await guild.system_channel.send(embed = em)
            

        

        else:
            return
    












    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.servers.execute('DELETE FROM systems WHERE guild_id = :guild_id', {'guild_id':guild.id})
        print('We are no longer apart of {}'.format(guild.name))
        





















    


            






    
    


def setup(bot):
    bot.add_cog(Server(bot))