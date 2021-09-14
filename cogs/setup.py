import discord
from discord.ext import commands
import asqlite




class welcomeLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    

    @commands.group()
    async def setup(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply('You gotta tell me what you want to setup.')
        
    @setup.command()
    async def welcome(self, ctx):
        servers = self.bot.servers
        em = discord.Embed(
                title = 'Welcome Setup',
                description="Follow the Instructions"
            )
        
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
                
                async with asqlite.connect('guild_data.db') as conn:
                    async with conn.cursor() as cur:
                        await cur.execute('UPDATE config SET WLChannel = :channel WHERE guild_id = :guild_id', {'channel':str(channel), 'guild_id':msg.guild.id})

                
                
                await msg.reply('Great! Moving to the next step.')                
                break
        em1 = discord.Embed(
                title = 'Welcome Setup',
                description="Follow the Instructions"
            )
        em1.add_field(name='Step 2:', value='What is the role You would like to give to new members? (Same as before, Write the name exactly as it is spelled)')
        await ctx.send(embed=em1)
        while True:
            msg = await self.bot.wait_for('message', check=check)
            role = discord.utils.get(ctx.guild.roles, name = msg.content)
            if role is None:
                await msg.reply("This role does not exist, try again.")
                continue
            else:
                async with asqlite.connect('guild_data.db') as conn:
                    async with conn.cursor() as cur:
                        await cur.execute('UPDATE config SET memberRole = :role WHERE guild_id = :guild_id', {'role':str(role), 'guild_id':msg.guild.id})

                
                await msg.reply('Great! Welcome Setup is complete. Run this command again if anything changes.')
                break





    @commands.Cog.listener()
    async def on_member_join(self, member):
        servers = self.bot.servers
        c = await servers.execute('SELECT welcome FROM systems WHERE guild_id=:guild_id', {'guild_id':member.guild.id})
        data = await c.fetchone()
        welcome = data[0]
        if welcome == 1:
            c = await servers.execute('SELECT WLChannel FROM config WHERE guild_id = :guild_id', {'guild_id': member.guild.id})
            data = await c.fetchone()
            channelName = data[0]
            channel = discord.utils.get(member.guild.channels, name = channelName)
            if channel is None:
                try:

                    await member.guild.system_channel.send(
                    '''Welcome {} to {}!

                    *This message is being sent to this channel because you have not set up a welcome channel*'''.format(member.mention, member.guild.name))
                except AttributeError:
                    print('')
                c = await servers.execute('SELECT memberRole FROM config WHERE guild_id = :guild_id', {'guild_id':member.guild.id})
                data = await c.fetchone()
                roleName = data[0]
                role = discord.utils.get(member.guild.roles, name = roleName)
                if role is None:
                    try:
                        await member.guild.system_channel.send('*No role given because either you did not setup the welcome system or the role name changed and you need to reset it again*')
                    except AttributeError:
                        print('')
                else:
                    await member.add_roles(role)
            else:
                await channel.send('Welcome {} to {}'.format(member.mention, member.guild.name))
                c = await servers.execute('SELECT memberRole FROM config WHERE guild_id = :guild_id', {'guild_id':member.guild.id})
                data = await c.fetchone()
                roleName = data[0]
                role = discord.utils.get(member.guild.roles, name = roleName)
                if role is None:
                    try:
                        await member.guild.system_channel.send('*No role given because either you did not setup the welcome system or the role name changed and you need to reset it again*')
                    except AttributeError:
                        print('')
                else:
                    await member.add_roles(role)
        else:
            pass



    @commands.Cog.listener()
    async def on_member_remove(self, member):
        servers = self.bot.servers
        c = await servers.execute('SELECT welcome FROM systems WHERE guild_id=:guild_id', {'guild_id':member.guild.id})
        data = await c.fetchone()
        welcome = data[0]
        if welcome == 1:
            c = await servers.execute('SELECT WLChannel FROM config WHERE guild_id = :guild_id', {'guild_id': member.guild.id})
            data = await c.fetchone()
            channelName = data[0]
            channel = discord.utils.get(member.guild.channels, name = channelName)
            if channel is None:
                try:
                    await member.guild.system_channel.send('''{} has left the server. 

                    *This message is being sent to this channel because you have not set up a welcome channel*'''.format(member.mention))
                except AttributeError:
                    print('')

            else:
                await channel.send('{} has left the server.'.format(member.mention))
        
        else:
            pass




def setup(bot):
    bot.add_cog(welcomeLeave(bot))