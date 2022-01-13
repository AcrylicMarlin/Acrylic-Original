import discord
from discord.ext import commands
import sqlite3



conn = sqlite3.connect(':memory:')
c = conn.cursor()


c.execute('''CREATE TABLE User_Warnings (
User_id integer,
Admin text,
Time text,
Warning text)''')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def warn(self,ctx,member:discord.Member=None, *, reason=None):
        if member == None:
            await ctx.send('Specify a member.')
            return
        if member == self.bot.user:
            await ctx.send('You warn the bot.')
            return
        if member == ctx.author:
            await ctx.send("You can't warn yourself.")
            return
        if reason == None:
            await ctx.send('Please give a reason.')
            return
        
        with conn:
            c.execute('INSERT INTO User_Warnings VALUES (:User_id, :Admin, datetime("now"), :Warning)', {'User_id': member.id, 'Admin': ctx.author.display_name, 'Warning': reason})
        await ctx.send('{} has been warned for {}'.format(member.display_name, reason))

    @commands.command(aliases = ['getwarns', 'warnings'])
    @commands.has_permissions(manage_messages = True)
    async def get_warns(self, ctx, member:discord.Member=None):
        if member == self.bot.user:
            await ctx.send('Not possible because I cannot be warned.')
            return
        
        member_warns = c.execute('SELECT Warning, Admin, Time FROM User_Warnings WHERE User_id = :User_id', {'User_id':member.id}).fetchall()

        

        em = discord.Embed(
            title = "{}'s Warnings".format(member.display_name),
            color = discord.Color.random()
        )

        i = 1
        for item in member_warns:
            warn, admin, time = item

            
            
            
            em.add_field(name = 'Warning {}'.format(i), value = 'Warning given by {} for {}. {}'.format(admin, warn, time), inline = False)
            
            i += 1
        
            

        await ctx.send(embed = em)
            
        

    @commands.command()
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
        
        with conn:
            c.execute("DELETE FROM User_Warnings WHERE User_id = :User_id", {'User_id':member.id})

        await ctx.send("{}'s warns have been removed.".format(member.display_name))

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = 5):
        await ctx.channel.purge(amount = amount)

    @commands.command()
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
        await member.send('You have been kicked from {} for {}'.format(ctx.guild.name, reason))
        
        await ctx.guild.kick(member)
        

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.Member=None, *, reason):
        if member == ctx.author:
            await ctx.send('You cannot ban yourself.')
            return
        if member == self.bot.user:
            await ctx.send('You cannot ban me mortal.')
            return
        if reason is None:
            await ctx.send('Why are you banning this person?')
            return
        
        await member.send('You were banned from {} for {}'.format(ctx.guild.name, reason))
        await ctx.send('{} was banned from {} for {}'.format(member.display_name, ctx.guild.name, reason))
        await ctx.guild.ban(member, reason = reason)
        
        


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.banned_users

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send('{} was unbanned from {}.'.format(member, ctx.guild.name))


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member:discord.Member=None, * , reason=None):
        if member == ctx.author:
            await ctx.send("You can't mute yourself.")
            return
        if member == None:
            await ctx.send("Specify who you would like to mute.")
            return

        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name='Muted')

        if not muteRole:
            muteRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(muteRole, speak=False, send_message = False, read_message_history = False)

        await member.add_roles(muteRole, reason=reason)
        await ctx.send('{} was muted for {}.'.format(member.display_name, reason))
        await member.send('You were muted in server {} for {}.'.format(guild.name, reason))


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send("Specify a member to unmute.")
            return

        mutedRole = discord.utils.get(ctx.guild.roles, name = 'Muted')
        await member.remove_roles(mutedRole)
        await member.send('You were unmuted in {}'.format(ctx.guild.name))
        await ctx.send('{} was unmuted.'.format(member.display_name))
        




        





            


    



def setup(bot):
    bot.add_cog(Moderation(bot))