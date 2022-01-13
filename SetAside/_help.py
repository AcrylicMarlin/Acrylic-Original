
import discord
from discord.ext import commands
import asqlite
class backAndExitButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    
    
    @discord.ui.button(
        label='Return',
        style=discord.ButtonStyle.primary,
        custom_id='backAndExitButtons:return'
    )
    async def _return(self, button:discord.ui.Button, interaction:discord.Interaction):
        em = discord.Embed(
            title = 'This is the help panel for my commands.',
            description= '''
            This is a list of all my categories. Select a button to go to that category's list of commands
            (These panels change depending on which systems you have enabled. If you don't know what this means, see Configuration.)
            ***Moderation***
                *All of the moderation commands.*

            ***Server Configuration***
                *All of the server configuration commands.*

            ***Level***
                *All of the level commands and how this system works.*

            ***AFK***
                *All of the afk commands and how this system works.*

            ***Configuration***
                *All of the configuration commands.*
            
            ***Extra Commands***
                *All of the extra commands.*'''
            
        )
        await interaction.response.edit_message(embed = em, view=HelpButtons())

    @discord.ui.button(
        label='Exit',
        style=discord.ButtonStyle.danger,
        custom_id='backAndExitButtons:exit'
    )
    async def exit(self, button:discord.ui.Button, interaction:discord.Interaction):
        msg = interaction.message
        await msg.delete()







    




         
    





class HelpButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label='Configuration',
        style=discord.ButtonStyle.primary,
        custom_id='HelpButtons:Configuration'
    )
    async def config(self, button:discord.ui.Button, interaction:discord.Interaction):
        config = discord.Embed(
            title='Configuration Help',
            description='This is the help page for the configuration commands.'
        )
        config.add_field(name='Enabled Systems List', value="Lists the current server configuration. `a'el`")
        config.add_field(name="Configuration Panel", value="Shows a panel to configure the current system configuration for this server. `a'config`")
        await interaction.response.edit_message(embed=config, view=backAndExitButtons())






    @discord.ui.button(
        label = 'AFK',
        style = discord.ButtonStyle.primary,
        custom_id = 'AFKHelpButtons:AFK'
    )
    async def AFK(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT afk FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                en = data[0]
                if en == 1:

                    afk = discord.Embed(
                        title='Afk help',
                        description='This system stores the afk for whatever reason you want.\nWhen you are pinged, I reply that you are afk for whatever reason since whatever time.\nOnce you speak, it removes the afk.\nYour afk is universal between servers I am in.'

                    )
                    afk.add_field(name='Afk Command', value="a'afk [Reason (Optional)]")
                    
                    await interaction.response.edit_message(embed=afk, view=backAndExitButtons())
                else:
                    afk = discord.Embed(
                        title='**Afk help**',
                        description="***I'm sorry to inform you of this, but this system is disable for your system.***"

                    )
                    await interaction.response.edit_message(embed=afk, view=backAndExitButtons())




    @discord.ui.button(
        label = 'Server',
        style = discord.ButtonStyle.primary,
        custom_id='HelpButtons:server'
    )
    async def server(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT server FROM systems WHERE guild_id = :guild_id',{'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                server = data[0]
                if server == 1:
                    em = discord.Embed(
                        title='Server Configuration Help',
                        description='This is the help panel for all of the server configuration commands and how to use them.'
                    )

                    em.add_field(name = "Add Category (`a'add_category <name>`, `a'acat <name>`)", value="Adds a category to this server.", inline = False)
                    em.add_field(name = "Add Channel (`a'add_channel <name>, <category (optional)>`, `a'ac <name>, <category (optional)>`)", value= "Adds a channel to this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.\nWhen adding a channel, if it goes under a category do channel-name, category name. Example: a'ac channel-name-example, category name example (comma and space must be used)", inline = False)
                    em.add_field(name = "Delete Channel (`a'dc <name>`, `a'delete_channel <name>`)", value= "Removes a channel from this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.", inline = False)
                    em.add_field(name = "Add Category (`a'dcat <name>`, `a'delete_category <name>`)", value="Removes a channel from this server.", inline = False)
                    em.add_field(name = "Add Member Role (`a'amr <member> <role>`, `a'add_member_role <member> <role>`, `a'AMR <member> <role>`)", value = 'Adds a role to a member. (Must be spelt exactly as it is named. Case-sensitive.)', inline = False)
                    em.add_field(name = "Add Server Role (`a'asr <name> `, `a'add_server_role <name>`, `a'ASR <name>`)", value="Adds a role to this server.", inline = False)
                    em.add_field(name = "Remove Member Role (`a'rmr <member> <name>`, `a'remove_member_role <member> <name>`, `a'RMR <member> <name>`)", value="Removes a role from a member. (Must be spelled exactly as it is named. Case-sensitive.)", inline = False)
                    em.add_field(name = "Remove Server Role (`a'rsr <role>`, `a'remove_server_role <role>`, `a'RSR <role>`)", value= "Removes a role from a server. (Must be spelled exactly as it is named. Case-sensitive.)", inline = False)
                    em.add_field(name = "Purge (`a'purge <amount (Defaults at 5)>`)", value='Clears messages from the channel it is used in.', inline=False)
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())
                else:
                    em = discord.Embed(
                        title='Server Configuration Help',
                        description='This is the help panel for all of the server configuration commands and how to use them.'
                    )
                    em.add_field(name = 'Disabled', value='This system has been disabled for this server.')
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())


    @discord.ui.button(
        label='Moderation',
        style=discord.ButtonStyle.primary,
        custom_id='HelpButtons:moderation'
    )    
    async def moderation(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT warn, mute FROM systems WHERE guild_id = :guild_id',{'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                warn, mute = data
                if warn == 1 and mute == 1:

                    em = discord.Embed(
                        title='Moderation Help Panel',
                        description='This is the panel for all moderation commands and how to use them.'
                    )
                    '''
                    a'ban <member> <reason>
                    a'clear_warns [member]
                    a'delete_warn <member>
                    a'get_mutes
                    a'get_warns [member]
                    a'kick [member] [reason]
                    a'mute [member] [reason]
                    a'purge [amount=5]
                    a'unban <member>
                    a'unmute [member]
                    a'warn [member] [reason]'''

                    em.add_field(name = "Kick (`a'kick <member> <reason>`)", value="Kicks a member from the server. (Requires Kick Members Perm)", inline = False)
                    em.add_field(name = "Ban (`a'ban <member> <reason>`)", value="Bans a member from the server. (Requires Bane Members Perm)", inline = False)
                    em.add_field(name = "Unban (`a'unban`)", value="Unbans a user from the server. Usage = a'unban member#discriminator")
                    em.add_field(name = "Warn (`a'warn <member> <reason>)", value="Warns a member for an infraction. (Requires Manage Guild Perm)", inline = False)
                    em.add_field(name = "Get Warns (`a'get_warns <member>`, `a'gm <member>`)", value=" Gets all the warns of a member. (Requires Manage Guild Perm)",inline=False)
                    em.add_field(name = "Delete Warn (`a'delete_warn <member>`, `a'deletewarn <member>`, `a'delwarn <member>`, `a'dw <member>`)",value="Deletes a warn from a user.",inline=False)
                    em.add_field(name = "Clear Warns (`a'clear_warns <member>`, `a'clearwarns <member>`, `a'cw <member>`", value="Clears ***all*** warns from a user. You will be prompted to ensure you are wanting to do this.",inline=False)
                    em.add_field(name = "Mute (`a'mute <member> <reason>`)",value="Mutes a member for an infraction.",inline=False)
                    em.add_field(name = "Unmute (`a'unmute <member>`)", value="Unmutes a member.",inline=False)
                    em.set_footer(text='All systems Enabled!')
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())

                if mute == 1 and warn != 1:
                    em = discord.Embed(
                        title='Moderation Help Panel',
                        description='This is the panel for all moderation commands and how to use them.'
                    )

                    em.add_field(name = "Kick (`a'kick <member> <reason>`)", value="Kicks a member from the server. (Requires Kick Members Perm)", inline = False)
                    em.add_field(name = "Ban (`a'ban <member> <reason>`)", value="Bans a member from the server. (Requires Bane Members Perm)", inline = False)
                    em.add_field(name = "Unban (`a'unban`)", value="Unbans a user from the server. Usage = a'unban member#discriminator",inline=False)
                    em.add_field(name = "Mute (`a'mute <member> <reason>`)",value="Mutes a member for an infraction.",inline=False)
                    em.add_field(name = "Unmute (`a'unmute <member>`)", value="Unmutes a member.",inline=False)
                    em.set_footer(text='The warn system has been disabled by your admins.')
                    await interaction.response.edit_message(embed = em, view = backAndExitButtons())
                
                if mute != 1 and warn == 1:
                    em = discord.Embed(
                        title='Moderation Help Panel',
                        description='This is the panel for all moderation commands and how to use them.'
                    )
                    em.add_field(name = "Kick (`a'kick <member> <reason>`)", value="Kicks a member from the server. (Requires Kick Members Perm)", inline = False)
                    em.add_field(name = "Ban (`a'ban <member> <reason>`)", value="Bans a member from the server. (Requires Bane Members Perm)", inline = False)
                    em.add_field(name = "Unban (`a'unban`)", value="Unbans a user from the server. Usage = a'unban member#discriminator")
                    em.add_field(name = "Warn (`a'warn <member> <reason>`)", value="Warns a member for an infraction. (Requires Manage Guild Perm)", inline = False)
                    em.add_field(name = "Get Warns (`a'get_warns <member>`, `a'gm <member>`)", value=" Gets all the warns of a member. (Requires Manage Guild Perm)",inline=False)
                    em.add_field(name = "Delete Warn (`a'delete_warn <member>`, `a'deletewarn <member>`, `a'delwarn <member>`, `a'dw <member>`)",value="Deletes a warn from a user.",inline=False)
                    em.add_field(name = "Clear Warns (`a'clear_warns <member>`, `a'clearwarns <member>`, `a'cw <member>`", value="Clears ***all*** warns from a user. You will be prompted to ensure you are wanting to do this.",inline=False)
                    em.set_footer(text='The mute system has been disabled by your admins.')
                    await interaction.response.edit_message(embed = em, view = backAndExitButtons())
                if mute != 1 and warn != 1:
                    em = discord.Embed(
                        title='Moderation Help Panel',
                        description='This is the panel for all moderation commands and how to use them.'
                    )
                    em.add_field(name = "Kick (`a'kick <member> <reason>`)", value="Kicks a member from the server. (Requires Kick Members Perm)", inline = False)
                    em.add_field(name = "Ban (`a'ban <member> <reason>`)", value="Bans a member from the server. (Requires Bane Members Perm)", inline = False)
                    em.add_field(name = "Unban (`a'unban`)", value="Unbans a user from the server. Usage = a'unban member#discriminator", inline=False)
                    em.set_footer(text='Both the warn system and the mute system have been disabled by your admins.')
                    await interaction.response.edit_message(embed = em, view = backAndExitButtons())



    












    @discord.ui.button(
        label = 'Level',
        style= discord.ButtonStyle.primary,
        custom_id='HelpButtons:level'
    )
    async def level(self, button:discord.ui.Button, interaction:discord.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT level FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                lvl = data[0]
                if lvl == 1:
                    em = discord.Embed(
                        title='Leveling Help Panel',
                        description='This is the help panel for the level commands and their usage.\nThis is not universal between servers. Everytime you send a message 2 exp is added.'
                    )
                    em.add_field(
                        name = "Stats (`a'stats <member (defaults to yourself)>`)",
                        value = 'Returns the stats of yourself or a member you mention.'
                    )
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())
                else:
                    em = discord.Embed(
                        title='Leveling Help Panel',
                        description='This is the help panel for the level commands and their usage.'
                    )
                    em.add_field(
                        name = 'Sorry',
                        value='This system has been disable by your server admins.'
                    ) 
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())

    @discord.ui.button(
        label= 'Extra',
        style=discord.ButtonStyle.primary,
        custom_id='HelpButtons:extra'
    )
    async def extra(self, button:discord.ui.Button, interaction:discord.Interaction):
        em = discord.Embed(
            title='Extra Commands',
            description='Couple of extra fun commands.'
        )
        em.add_field(name="8Ball (`a'8ball <question>`, `a'8Ball <question>`, `a'8b <question>", value='Ask it a question and it gives you a wise answer.')
        em.add_field(name="Bruh (`a'bruh`)", value='Agrees with your bruh.')
        em.add_field(name="Ping (`a'ping`)", value= 'Returns the bots latency (ping).')
        await interaction.response.edit_message(embed=em, view=backAndExitButtons())



    @discord.ui.button(
        label = 'Exit',
        style=discord.ButtonStyle.danger,
        custom_id='HelpButtons:exit'
    )
    async def exit(self, button:discord.ui.Button, interaction:discord.Interaction):
        msg = interaction.message
        await msg.delete()












class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot











    @commands.group()
    async def help(self, ctx):
        
        if ctx.invoked_subcommand is None:

            em = discord.Embed(
                title = 'This is the help panel for my commands.',
                description= '''
                This is a list of all my categories. Select a button to go to that category's list of commands
                (These panels change depending on which systems you have enabled. If you don't know what this means, see Configuration.)
                ***Moderation***
                    *All of the moderation commands.*

                ***Server Configuration***
                    *All of the server configuration commands.*

                ***Level***
                    *All of the level commands and how this system works.*

                ***AFK***
                    *All of the afk commands and how this system works.*

                ***Configuration***
                    *All of the configuration commands.*

                ***Extra Commands***
                    *All of the extra commands.*'''

            )
            await ctx.send(embed=em, view=HelpButtons())





        

def setup(bot):
    bot.add_cog(Help(bot))