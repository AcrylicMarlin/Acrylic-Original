import asyncio
import asqlite
import discord
from discord.ext import commands











async def get_enabled(guild):
    async with asqlite.connect('guild_data.db') as conn:
        async with conn.cursor() as cur:
            c = await cur.execute('SELECT afk, level, warn, mute, welcome, server FROM systems WHERE guild_id = :guild_id', {'guild_id':guild.id})
            data  = await c.fetchone()
            afk, level, warn, mute, welcome, server = data
            em = discord.Embed(
                title = 'Configuration Menu',
                description= 'Enable/Disable Systems'
            )
            if afk == 1:
                afk = ':white_check_mark:'
            else:
                afk = ':no_entry:'   
            if level == 1:
                level = ':white_check_mark:'
            else:
                level = ':no_entry:' 
            if warn == 1:
                warn = ':white_check_mark:'
            else:
                warn = ':no_entry:'  
            if mute == 1:
                mute = ':white_check_mark:'
            else:
                mute = ':no_entry:'  
            if welcome == 1:
                welcome = ':white_check_mark:'
            else:
                welcome = ':no_entry:'   
            if server == 1:
                server = ':white_check_mark:'
            else:
                server = ':no_entry:'
            em.add_field(name='\u200b', value='AFK System - {}'.format(afk), inline = False)
            em.add_field(name='\u200b', value='Level System - {}'.format(level), inline = False)
            em.add_field(name='\u200b', value='Warning System - {}'.format(warn), inline = False)
            em.add_field(name='\u200b', value='Muting System - {}'.format(mute), inline = False)
            em.add_field(name='\u200b', value='Welcoming/Goodbye System - {}'.format(welcome), inline = False)
            em.add_field(name='\u200b', value='Server Configuration System - {}'.format(server), inline = False)
            return em








class config_buttons(discord.ui.View):


    def __init__(self):
        super().__init__(timeout=None)
    configpanel = discord.Embed(title = 'Configuration Panel',
    description='Configure the servers systems here.')
    @discord.ui.button(label = 'AFK', style = discord.ButtonStyle.green, custom_id='config_buttons:afk')
    async def afk(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT afk FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                afk = data[0]
                if afk == 1:
                    await cur.execute('UPDATE systems SET afk = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                    
                else:
                    await cur.execute('UPDATE systems SET afk = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                    

        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))


    @discord.ui.button(label = 'Level', style = discord.ButtonStyle.green, custom_id='config_buttons:level')
    async def level(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT level FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                level = data[0]
                if level == 1:
                    await cur.execute('UPDATE systems SET level = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                else:
                    await cur.execute('UPDATE systems SET level = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))



    @discord.ui.button(label = 'Warn', style = discord.ButtonStyle.green, custom_id='config_buttons:warn')
    async def warn(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT warn FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                warn = data[0]
                if warn == 1:
                    await cur.execute('UPDATE systems SET warn = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                else:
                    await cur.execute('UPDATE systems SET warn = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))



    @discord.ui.button(label = 'Mute', style = discord.ButtonStyle.green, custom_id='config_buttons:mute')
    async def mute(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT mute FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                mute = data[0]
                if mute == 1:
                    await cur.execute('UPDATE systems SET mute = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                else:
                    await cur.execute('UPDATE systems SET mute = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))


    @discord.ui.button(label = 'Welcome', style = discord.ButtonStyle.green, custom_id='config_buttons:welcome')
    async def welcome(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT welcome FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                welcome = data[0]
                if welcome == 1:
                    await cur.execute('UPDATE systems SET welcome = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                else:
                    await cur.execute('UPDATE systems SET welcome = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))


    @discord.ui.button(label = 'Server', style = discord.ButtonStyle.green, custom_id='config_buttons:server')
    async def server(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT server FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                server = data[0]
                if server == 1:
                    await cur.execute('UPDATE systems SET server = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                else:
                    await cur.execute('UPDATE systems SET server = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))

    


    @discord.ui.button(label = 'Enable All', style=discord.ButtonStyle.primary, custom_id='config_buttons:enable_all')
    async def en_all(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT * from systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                guild, afk, level, warn, mute, welcome, server = data
                if afk == 0:
                    await cur.execute('UPDATE systems SET afk = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                

                if level == 0:
                    await cur.execute('UPDATE systems SET level = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if warn == 0:
                    await cur.execute('UPDATE systems SET warn = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if mute == 0:
                    await cur.execute('UPDATE systems SET mute = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if welcome == 0:
                    await cur.execute('UPDATE systems SET welcome = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if server == 0:
                    await cur.execute('UPDATE systems SET server = 1 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))


    @discord.ui.button(label = 'Disable All', style=discord.ButtonStyle.primary, custom_id='config_buttons:disable_all')
    async def dis_all(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT * from systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                guild, afk, level, warn, mute, welcome, server = data
                if afk == 1:
                    await cur.execute('UPDATE systems SET afk = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})               

                if level == 1:
                    await cur.execute('UPDATE systems SET level = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if warn == 1:
                    await cur.execute('UPDATE systems SET warn = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if mute == 1:
                    await cur.execute('UPDATE systems SET mute = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if welcome == 1:
                    await cur.execute('UPDATE systems SET welcome = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

                if server == 1:
                    await cur.execute('UPDATE systems SET server = 0 WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})

        await interaction.response.edit_message(embed=await get_enabled(interaction.message.guild))
    @discord.ui.button(label = 'Exit', style=discord.ButtonStyle.danger, custom_id='config_buttons:exit')
    async def exit(self, button:discord.ui.Button, interaction:discord.Interaction):
        msg = interaction.message
        await msg.delete()



class enter_config_buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    config_panel = discord.Embed(title = 'Configuration Panel',
    description='Configure the servers systems here.')
    @discord.ui.button(label = 'Configure', style = discord.ButtonStyle.primary, custom_id='enter_config_buttons:configure')
    async def configure(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT * from systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                config_panel = discord.Embed(title = 'Configuration Panel',
                    description='Configure the servers systems here.')
                guild, afk, level, warn, mute, welcome, server = data
                if afk == 1:
                    afk = ':white_check_mark:'
                else:
                    afk = ':no_entry:'

                if level == 1:
                    level = ':white_check_mark:'
                else:
                    level = ':no_entry:'

                if warn == 1:
                    warn = ':white_check_mark:'
                else:
                    warn = ':no_entry:'

                if mute == 1:
                    mute = ':white_check_mark:'
                else:
                    mute = ':no_entry:'

                if welcome == 1:
                    welcome = ':white_check_mark:'
                else:
                    welcome = ':no_entry:'

                if server == 1:
                    server = ':white_check_mark:'
                else:
                    server = ':no_entry:'
                config_panel.add_field(name='\u200b', value='AFK System - {}'.format(afk), inline = False)
                config_panel.add_field(name='\u200b', value='Level System - {}'.format(level), inline = False)
                config_panel.add_field(name='\u200b', value='Warning System - {}'.format(warn), inline = False)
                config_panel.add_field(name='\u200b', value='Muting System - {}'.format(mute), inline = False)
                config_panel.add_field(name='\u200b', value='Welcoming/Goodbye System - {}'.format(welcome), inline = False)
                config_panel.add_field(name='\u200b', value='Server Configuration System - {}'.format(server), inline = False)


                

                await interaction.response.edit_message(embed=config_panel, view = config_buttons())
                





    @discord.ui.button(label = 'Cancel', style=discord.ButtonStyle.danger, custom_id='enter_config_buttons:cancel')
    async def cancel(self, button:discord.ui.Button, interaction:discord.Interaction):
        msg = interaction.message
        await msg.delete()





class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    










    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        servers = self.bot.servers

        await servers.execute('INSERT INTO systems VALUES (:guild_id, 1, 1, 1, 1, 1, 1)', {'guild_id':guild.id, 'name':guild.name})













    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        servers = self.bot.servers

        await servers.execute('DELETE FROM systems WHERE guild_id = :guild_id', {'guild_id':guild.id})
        














    @commands.command(aliases = ['el'])
    
    async def enabled_list(self, ctx):
        servers = self.bot.servers

        
        c = await servers.execute('SELECT * FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        guild, afk, level, warn, mute, welcome, server = data
        em = discord.Embed(title = "{}'s Server Settings".format(ctx.guild.name))

        if afk == 1:
            afk = ':white_check_mark:'
        else:
            afk = ':no_entry:'
        if level == 1:
            level = ':white_check_mark:'
        else:
            level = ':no_entry:'
        if warn == 1:
            warn = ':white_check_mark:'
        else:
            warn = ':no_entry:'
        if mute == 1:
            mute = ':white_check_mark:'
        else:
            mute = ':no_entry:'
        if welcome == 1:
                welcome = ':white_check_mark:'
        else:
            welcome = ':no_entry:'
        if server == 1:
            server = ':white_check_mark:'
        else:
            server = ':no_entry:'
        em.add_field(name = 'AFK System', value = f'{afk}', inline = False)
        em.add_field(name = 'Leveling System', value = f'{level}', inline = False)
        em.add_field(name = 'Warn System', value = f'{warn}', inline = False)
        em.add_field(name = 'Mute System', value = f'{mute}', inline = False)
        em.add_field(name = 'Welcome System', value = f'{welcome}', inline = False)
        em.add_field(name = 'Server Configuration System', value = f'{server}', inline = False)





        if ctx.guild.icon is not None:
            em.set_thumbnail(url=ctx.guild.icon.url)
        
        

    

        await ctx.send(embed = em)
    











    @commands.command()
    @commands.has_permissions(administrator =  True)
    async def config(self, ctx):
        servers = self.bot.servers
        await ctx.message.delete()
        self.bot.add_view(enter_config_buttons())
        c = await servers.execute('SELECT afk, level, warn, mute, welcome, server FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
        data = await c.fetchone()
        afk, level, warn, mute, welcome, server = data
        if afk == 1:
            afk = ':white_check_mark:'
        else:
            afk = ':no_entry:'
        if level == 1:
            level = ':white_check_mark:'
        else:
            level = ':no_entry:'
        if warn == 1:
            warn = ':white_check_mark:'
        else:
            warn = ':no_entry:'
        if mute == 1:
            mute = ':white_check_mark:'
        else:
            mute = ':no_entry:'
        if welcome == 1:
            welcome = ':white_check_mark:'
        else:
            welcome = ':no_entry:'
        if server == 1:
            server = ':white_check_mark:'
        else:
            server = ':no_entry:'

        con = discord.Embed(title='Current Configuration.',
        description='This is your current system configuration for this server.')
        con.add_field(name='\u200b', value='AFK System - {}'.format(afk), inline = False)
        con.add_field(name='\u200b', value='Level System - {}'.format(level), inline = False)
        con.add_field(name='\u200b', value='Warning System - {}'.format(warn), inline = False)
        con.add_field(name='\u200b', value='Muting System - {}'.format(mute), inline = False)
        con.add_field(name='\u200b', value='Welcoming/Goodbye System - {}'.format(welcome), inline = False)
        con.add_field(name='\u200b', value='Server Configuration System - {}'.format(server), inline = False)
        await ctx.send(embed = con, view = enter_config_buttons())

        


    

def setup(bot):
    bot.add_cog(Configuration(bot))