from ast import Str
import discord
from discord.ext import commands
import traceback
import sys
import typing
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



class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    



    @commands.command(
        aliases = ['amr', 'AMR'],
        help = 'Adds a role to a member.')
    @commands.has_permissions(manage_roles = True)
    async def add_member_role(self, ctx, member:discord.Member=None, *, name):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            if member is None:
                await ctx.send('Specify a member to add this role too.')
                return

            role = discord.utils.get(ctx.guild.roles, name = name)
            if not role:
                await ctx.send('Looks like the role you gave me does not exist. Try again.\n*Note: Make sure to write it exactly as it is spelled in the role list.*')
                return
            await member.add_roles(role)
            await ctx.send('Added the role to {}.'.format(member.display_name))
        else:
            await ctx.send('Your server admins have disabled this system.')
    
    








    @commands.command(
        aliases = ['rmr', 'RMR'],
        help = 'Removes a role from a member.')
    @commands.has_permissions(manage_roles = True)
    async def remove_member_role(self, ctx, member:discord.Member=None, *, name):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            if member is None:
                await ctx.send('Specify a member to remove this role from.')
                return
            role = discord.utils.get(ctx.guild.roles, name = name)
            if not role:
                await ctx.send('Looks like the role you gave me does not exist. Try again.\n*Note: Make sure to write it exactly as it is spelled in the role list.*')
                return
            await member.remove_roles(role)
            await ctx.send('Role removed from {}'.format(member.display_name))
        else:
            await ctx.send('Your server admins have disabled this system.')













    @commands.command(
        aliases = ['asr', 'ASR'],
        help = 'Adds a role to this server.')
    @commands.has_permissions(manage_roles = True)
    async def add_server_role(self, ctx, *, role):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            role = await ctx.guild.create_role(name = role)        
            await ctx.send("{} role successfully created. Use `a'amr` to add the role to someone.".format(role.mention))
        else:
            await ctx.send('Your server admins have disabled this system.')














    @commands.command(
        aliases = ['rsr', 'RSR'],
        help = 'Removes a role from this server.')
    @commands.has_permissions(manage_roles = True)
    async def remove_server_role(self, ctx, *, role):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            role = discord.utils.get(ctx.guild.roles, name = role)
            await role.delete()
            await ctx.send('The role has been deleted from the server.')
        else:
            await ctx.send('Your server admins have disabled this system.')




    









    @commands.command(
        aliases = ['addchannel', 'ac'],
        help = 'Adds a channel to the server. When using, If you only create a channel, pass the channel name (with dashes between each word) If you are adding to a category, pass [Channel-name], [Category Name]')
    @commands.has_permissions(manage_channels = True)
    async def add_channel(self, ctx, *, arg):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            if ',' in arg:
                channelName, category = arg.split(', ')
                category = discord.utils.get(ctx.guild.categories, name = category)

            else:
                channelName = arg
                category = None

            channel = await ctx.guild.create_text_channel(channelName, category = category)


            if category is None:
                await ctx.send('Text channel {} created.'.format(channel.mention))
            else:
                await ctx.send('Text channel {} created under the category {}.'.format(channel.mention, category.mention))
        else:
            await ctx.send('Your server admins have disabled this system.')
    @add_channel.error
    async def ac_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have permission to do this.')
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send('When you use this command, *Split the channel name and the category with a comma and a space with the channel name before the comma and the category after the space.\nIf there is no category dont add a comma.*')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You are missing the name of the channel.')
        



















           
    @commands.command(
        aliases = ['acat'],
        help = 'Adds a category to this server.')
    @commands.has_permissions(manage_channels = True)
    async def add_category(self, ctx, *, name):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            cat = await ctx.guild.create_category(name = name)
            await ctx.send('Category {} added.'.format(cat.mention))
        else:
            await ctx.send('Your server admins have disabled this system.')


    @add_category.error
    async def acat_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have permission to do this.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You forgot to tell me the name of the category.')
        
















    
    @commands.command(
        aliases = ['dcat'],
        help = 'Deletes a category from this server.')
    @commands.has_permissions(manage_channels = True)
    async def delete_category(self, ctx, *, name):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            cat = discord.utils.get(ctx.guild.categories, name = name)
            await cat.delete()
            await ctx.send('Category deleted.')
        else:
            await ctx.send('Your server admins have disabled this system.')





    @delete_category.error
    async def dcat_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have permission to do this.')
        if isinstance(error, commands.MissingRequiredArgument):
            
            await ctx.send('You forgot to tell me the name of the category.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('This name does not exist in this server. Remember to type it exactly.')
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    

















    @commands.command(
        aliases = ['dc'],
        help = 'Deletes a channel from this server.')
    @commands.has_permissions(manage_channels = True)
    async def delete_channel(self, ctx, *, name):
        c = await self.bot.servers.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        server = data[0]
        if server == 1:

            chan = discord.utils.get(ctx.guild.channels, name = name)
            await chan.delete()
            await ctx.send('Channel deleted.')
        else:
            await ctx.send('Your server admins have disabled this system.')


    @delete_channel.error
    async def dc_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have permission to do this.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You forgot to tell me the name of the channel.')
        if isinstance(error, AttributeError):
            await ctx.send('This channel does not exist. You must type it exactly as its named.')
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    


    @commands.command(
        help = 'Clears messages from a channel.'
    )
    @commands.cooldown(rate = 1, per = 5.0)
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = 5):
        if amount <= 25:

            await ctx.message.delete()
            await ctx.channel.purge(limit = amount)
        else:
            await ctx.send('The maximum amount of messages you can purge is 25!')














    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print('I joined a new guild named {}!'.format(guild.name))
        em = discord.Embed(title = 'Thank you for choosing Acrylic.',
        description = "Thank you so much for allowing me to be a part of your server. My creator worked long and hard for this.\nTo begin use the command `a'help` for a list of commands.")
        try:
            await guild.owner.send(embed = em)
            
        
        except discord.Forbidden:
            await guild.system_channel.send(embed = em)
            

        

        else:
            return
    












    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.servers.execute('DELETE FROM systems WHERE guild_id = :guild_id', {'guild_id':guild.id})
        print('We are no longer apart of {}'.format(guild.name))
        





















    


            






    
    


def setup(bot):
    bot.add_cog(Server(bot))