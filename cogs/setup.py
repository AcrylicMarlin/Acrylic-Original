import disnake
from disnake.ext import commands
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
        em = disnake.Embed(
                title = 'Welcome Setup',
                description="Follow the Instructions"
            )
        
        em.add_field(name = 'Step One:', value='What channel would you like to have welcome/leave notifs {Input "none" to make one, Input "skip" to move on, Input the name of the channel if it exists}? (The channel must be spelled exactly as it is spelled)')
        await ctx.reply(embed = em)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while True:
            msg = await self.bot.wait_for('message', check=check)
            if msg.content == 'none':
                await ctx.send('Would you like me to make one?')
                msg = await self.bot.wait_for('message', check=check)
                if msg.content == 'yes':
                    await ctx.send('What is the name you would like to give it?')
                    msg = await self.bot.wait_for('message', check=check)
                    name = msg.content.replace(' ', '-')

                    channel = await ctx.guild.create_text_channel(name = name)
                    await ctx.send('Channel created as {}'.format(channel.mention))
                    async with asqlite.connect('guild_data.db') as conn:
                        async with conn.cursor() as cur:
                            await cur.execute('UPDATE config SET WLChannel = :channel WHERE guild_id = :guild_id', {'channel':str(channel), 'guild_id':msg.guild.id})
                    break

            elif msg.content == 'skip':
                await msg.reply('Moving to next step')
                break
            
            else:

                channel = disnake.utils.get(ctx.guild.channels, name = msg.content)
                if channel is None:
                    await msg.reply("This channel doesn't exist, try again.")
                    continue
                else:

                    async with asqlite.connect('guild_data.db') as conn:
                        async with conn.cursor() as cur:
                            await cur.execute('UPDATE config SET WLChannel = :channel WHERE guild_id = :guild_id', {'channel':str(channel), 'guild_id':msg.guild.id})



                    await msg.reply('Great! Moving to the next step.')                
                    break
        em1 = disnake.Embed(
                title = 'Welcome Setup',
                description="Follow the Instructions"
            )
        em1.add_field(name='Step 2:', value='What is the role You would like to give to new members? (Same as before, Write the name exactly as it is spelled)')
        await ctx.send(embed=em1)
        while True:
            msg = await self.bot.wait_for('message', check=check)
            if msg.content == 'skip':
                await msg.reply('Great! Welcome Setup is complete. Run this command again if anything changes.')
                break
            else:

                role = disnake.utils.get(ctx.guild.roles, name = msg.content)
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
            channel = disnake.utils.get(member.guild.channels, name = channelName)
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
                role = disnake.utils.get(member.guild.roles, name = roleName)
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
                role = disnake.utils.get(member.guild.roles, name = roleName)
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
            channel  = disnake.utils.get(member.guild.channels, name = channelName)
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