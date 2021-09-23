import disnake
from disnake.ext import commands
import asqlite

class backAndExitButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    
    
    @disnake.ui.button(
        label='Return',
        style=disnake.ButtonStyle.primary,
        custom_id='backAndExitButtons:return'
    )
    async def _return(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        em = disnake.Embed(
            title = 'This is the help panel for my commands.',
            description= '''
            This is a list of all my categories. Select a button to go to that category's list of commands
            (These panels change depending on which systems you have enabled. If you don't know what this means, see Configuration.)
            ***Moderation***
                *All of the moderation commands.*
                `a'help Moderation <command>`

            ***Server Configuration***
                *All of the server configuration commands.*
                `a'help Server <command>`

            ***Level***
                *All of the level commands and how this system works.*
                `a'help Level`

            ***AFK***
                *All of the afk commands and how this system works.*
                `a'help Afk`

            ***Configuration***
                *All of the configuration commands.*
                `a'help Configuration <command>`
            
            ***Extra Commands***
                *All of the extra commands.*
                `a'help Extra <command>`
                
                '''
                
            
        )
        em.set_footer(text="Use `a'help <category> <command>` to get help for a specific command.")
        await interaction.response.edit_message(embed = em, view=HelpButtons())

    @disnake.ui.button(
        label='Exit',
        style=disnake.ButtonStyle.danger,
        custom_id='backAndExitButtons:exit'
    )
    async def exit(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        msg = interaction.message
        await msg.delete()







    




         
    





class HelpButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label='Configuration',
        style=disnake.ButtonStyle.primary,
        custom_id='HelpButtons:Configuration'
    )
    async def config(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        config = disnake.Embed(
            title='Configuration Help',
            description='This is the help page for the configuration commands.'
        )
        config.add_field(name='Enabled Systems List', value="Lists the current server configuration. `a'el`")
        config.add_field(name="Configuration Panel", value="Shows a panel to configure the current system configuration for this server. `a'config`")
        await interaction.response.edit_message(embed=config, view=backAndExitButtons())






    @disnake.ui.button(
        label = 'AFK',
        style = disnake.ButtonStyle.primary,
        custom_id = 'AFKHelpButtons:AFK'
    )
    async def AFK(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT afk FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                en = data[0]
                if en == 1:

                    afk = disnake.Embed(
                        title='Afk help',
                        description='This system stores the afk for whatever reason you want.\nWhen you are pinged, I reply that you are afk for whatever reason since whatever time.\nOnce you speak, it removes the afk.\nYour afk is universal between servers I am in.'

                    )
                    afk.add_field(name='Afk Command', value="a'afk [Reason (Optional)]")
                    
                    await interaction.response.edit_message(embed=afk, view=backAndExitButtons())
                else:
                    afk =disnake.Embed(
                        title='**Afk help**',
                        description="***I'm sorry to inform you of this, but this system is disable for your system.***"

                    )
                    await interaction.response.edit_message(embed=afk, view=backAndExitButtons())




    @disnake.ui.button(
        label = 'Server',
        style = disnake.ButtonStyle.primary,
        custom_id='HelpButtons:server'
    )
    async def server(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT server FROM systems WHERE guild_id = :guild_id',{'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                server = data[0]
                if server == 1:
                    em = disnake.Embed(
                        title='Server Configuration Help',
                        description='This is the help panel for all of the server configuration commands and how to use them.'
                    )

                    em.add_field(name = "Add Category (`a'add_category <name>`, `a'acat <name>`)", value="Adds a category to this server.", inline = False)
                    em.add_field(name = "Add Channel (`a'add_channel <name>, <category (optional)>`, `a'ac <name>, <category (optional)>`)", value= "Adds a channel to this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.\nWhen adding a channel, if it goes under a category do channel-name, category name. Example: a'ac channel-name-example, category name example (comma and space must be used)", inline = False)
                    em.add_field(name = "Delete Channel (`a'dc <name>`, `a'delete_channel <name>`)", value= "Removes a channel from this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.", inline = False)
                    em.add_field(name = "Delete Category (`a'dcat <name>`, `a'delete_category <name>`)", value="Removes a channel from this server.", inline = False)
                    em.add_field(name = "Add Member Role (`a'amr <member> <role>`, `a'add_member_role <member> <role>`, `a'AMR <member> <role>`)", value = 'Adds a role to a member. (Must be spelled exactly as it is named. Case-sensitive.)', inline = False)
                    em.add_field(name = "Add Server Role (`a'asr <name> `, `a'add_server_role <name>`, `a'ASR <name>`)", value="Adds a role to this server.", inline = False)
                    em.add_field(name = "Remove Member Role (`a'rmr <member> <name>`, `a'remove_member_role <member> <name>`, `a'RMR <member> <name>`)", value="Removes a role from a member. (Must be spelled exactly as it is named. Case-sensitive.)", inline = False)
                    em.add_field(name = "Remove Server Role (`a'rsr <role>`, `a'remove_server_role <role>`, `a'RSR <role>`)", value= "Removes a role from a server. (Must be spelled exactly as it is named. Case-sensitive.)", inline = False)
                    em.add_field(name = "Purge (`a'purge <amount (Defaults at 5)>`)", value='Clears messages from the channel it is used in.', inline=False)
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())
                else:
                    em = disnake.Embed(
                        title='Server Configuration Help',
                        description='This is the help panel for all of the server configuration commands and how to use them.'
                    )
                    em.add_field(name = 'Disabled', value='This system has been disabled for this server.')
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())


    @disnake.ui.button(
        label='Moderation',
        style=disnake.ButtonStyle.primary,
        custom_id='HelpButtons:moderation'
    )    
    async def moderation(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT warn, mute FROM systems WHERE guild_id = :guild_id',{'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                warn, mute = data
                if warn == 1 and mute == 1:

                    em = disnake.Embed(
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
                    em.add_field(name = "Get Warns (`a'get_warns <member>`, `a'gm <member>`, `a'getwarns <member>`)", value=" Gets all the warns of a member. (Requires Manage Guild Perm)",inline=False)
                    em.add_field(name = "Delete Warn (`a'delete_warn <member>`, `a'deletewarn <member>`, `a'delwarn <member>`, `a'dw <member>`)",value="Deletes a warn from a user.",inline=False)
                    em.add_field(name = "Clear Warns (`a'clear_warns <member>`, `a'clearwarns <member>`, `a'cw <member>`)", value="Clears ***all*** warns from a user. You will be prompted to ensure you are wanting to do this.",inline=False)
                    em.add_field(name = "Mute (`a'mute <member> <reason>`)",value="Mutes a member for an infraction.",inline=False)
                    em.add_field(name = "Unmute (`a'unmute <member>`)", value="Unmutes a member.",inline=False)
                    em.set_footer(text='All systems Enabled!')
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())

                if mute == 1 and warn != 1:
                    em = disnake.Embed(
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
                    em = disnake.Embed(
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
                    em = disnake.Embed(
                        title='Moderation Help Panel',
                        description='This is the panel for all moderation commands and how to use them.'
                    )
                    em.add_field(name = "Kick (`a'kick <member> <reason>`)", value="Kicks a member from the server. (Requires Kick Members Perm)", inline = False)
                    em.add_field(name = "Ban (`a'ban <member> <reason>`)", value="Bans a member from the server. (Requires Bane Members Perm)", inline = False)
                    em.add_field(name = "Unban (`a'unban`)", value="Unbans a user from the server. Usage = a'unban member#discriminator", inline=False)
                    em.set_footer(text='Both the warn system and the mute system have been disabled by your admins.')
                    await interaction.response.edit_message(embed = em, view = backAndExitButtons())



    












    @disnake.ui.button(
        label = 'Level',
        style= disnake.ButtonStyle.primary,
        custom_id='HelpButtons:level'
    )
    async def level(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        async with asqlite.connect('guild_data.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT level FROM systems WHERE guild_id = :guild_id', {'guild_id':interaction.message.guild.id})
                data = await c.fetchone()
                lvl = data[0]
                if lvl == 1:
                    em = disnake.Embed(
                        title='Leveling Help Panel',
                        description='This is the help panel for the level commands and their usage.\nThis is not universal between servers. Everytime you send a message 2 exp is added.'
                    )
                    em.add_field(
                        name = "Stats (`a'stats <member (defaults to yourself)>`)",
                        value = 'Returns the stats of yourself or a member you mention.'
                    )
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())
                else:
                    em = disnake.Embed(
                        title='Leveling Help Panel',
                        description='This is the help panel for the level commands and their usage.'
                    )
                    em.add_field(
                        name = 'Sorry',
                        value='This system has been disable by your server admins.'
                    ) 
                    await interaction.response.edit_message(embed=em, view=backAndExitButtons())

    @disnake.ui.button(
        label= 'Extra',
        style=disnake.ButtonStyle.primary,
        custom_id='HelpButtons:extra'
    )
    async def extra(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        em = disnake.Embed(
            title='Extra Commands',
            description='Couple of extra fun commands.'
        )
        em.add_field(name="8Ball (`a'8ball <question>`, `a'8Ball <question>`, `a'8b <question>", value='Ask it a question and it gives you a wise answer.')
        em.add_field(name="Bruh (`a'bruh`)", value='Agrees with your bruh.')
        em.add_field(name="Ping (`a'ping`)", value= 'Returns the bots latency (ping).')
        await interaction.response.edit_message(embed=em, view=backAndExitButtons())



    @disnake.ui.button(
        label = 'Exit',
        style=disnake.ButtonStyle.danger,
        custom_id='HelpButtons:exit'
    )
    async def exit(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        msg = interaction.message
        await msg.delete()












class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot











    @commands.group()
    async def help(self, ctx):
        
        
        if ctx.invoked_subcommand is None:
            self.bot.add_view(backAndExitButtons())
            self.bot.add_view(HelpButtons())

            em = disnake.Embed(
            title = 'This is the help panel for my commands.',
            description= '''
            This is a list of all my categories. Select a button to go to that category's list of commands
            (These panels change depending on which systems you have enabled. If you don't know what this means, see Configuration.)
            ***Moderation***
                *All of the moderation commands.*
                `a'help Moderation <command>`

            ***Server Configuration***
                *All of the server configuration commands.*
                `a'help Server <command>`

            ***Level***
                *All of the level commands and how this system works.*
                `a'help Level`

            ***AFK***
                *All of the afk commands and how this system works.*
                `a'help Afk`

            ***Configuration***
                *All of the configuration commands.*
                `a'help Configuration <command>`
            
            ***Extra Commands***
                *All of the extra commands.*
                `a'help Extra <command>`
                
                '''
            )
            em.set_footer(text="Use `a'help <category> <command>` to get help for a specific command.")
            await ctx.send(embed=em, view=HelpButtons())


    @help.command()
    async def Afk(self, ctx):
        if ctx.invoked_subcommand is None:
            afk = disnake.Embed(
                    title='Afk help',
                    description='This system stores the afk for whatever reason you want.\nWhen you are pinged, I reply that you are afk for whatever reason since whatever time.\nOnce you speak, it removes the afk.\nYour afk is universal between servers I am in.'
                )
            afk.add_field(name='Afk Command', value="`a'afk [Reason (Optional)]`")
            await ctx.send(embed=afk)
    
    @help.group()
    async def Configuration(self,ctx):
        if ctx.invoked_subcommand is None:
            config = disnake.Embed(
            title='Configuration Help',
            description='These commands are for showing and configuring the systems you would like to use in the server.'
        )
        await ctx.send(embed = config)

    @Configuration.command()
    async def el(self, ctx):
        em = disnake.Embed(
            title='Enabled List',
            description="`a'el`. Shows a list of all systems and whether they are Online."
        )
        await ctx.send(embed =em)
    
    @Configuration.command()
    async def config(self, ctx):
        em = disnake.Embed(
            title='Configuration Panel',
            description="`a'config`. Brings up a panel to enabled and disable systems for this server."
        )
        await ctx.send(embed = em)



    @help.group()
    async def Server(self, ctx):
        if ctx.invoked_subcommand is None:
            em = disnake.Embed(
                    title='Server Configuration Help',
                    description='This Category has all the commands meant for configuring the server in different ways.'
                )
            await ctx.send(embed=em)
    '''
    a'add_category <name>
    a'add_channel <arg>
    a'add_member_role [member] <name>
    a'add_server_role <role>
    a'delete_category <name>
    a'delete_channel <name>
    a'purge [amount=5]
    a'remove_member_role [member] <name>
    a'remove_server_role <role>'''
    @Server.command()
    async def acat(self, ctx):
        emb = disnake.Embed(
                    title='Add Category',
                    description='Adds a category to this server.'
                )
        emb.add_field(name = 'Aliases', value = '`add_category`, `acat`')
        await ctx.send(embed = emb)
    @Server.command()
    async def add_category(self, ctx):
        em = disnake.Embed(
                    title='Add Category',
                    description='Adds a category to this server.'
                )
        em.add_field(name = 'Aliases', value = "(`a'add_category <name>`, `a'acat <name>`)")
        await ctx.send(embed = em)
    
    @Server.command()
    async def add_channel(self, ctx):
        

        em = disnake.Embed(
                    title='Add Channel',
                    description="Adds a channel to this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.\nWhen adding a channel, if it goes under a category do channel-name, category name. Example: a'ac channel-name-example, category name example (comma and space must be used)"
                )
        em.add_field(name = 'Aliases', value = "(`a'add_channel <name>, <category (optional)>`, `a'ac <name>, <category (optional)>`)")
        await ctx.send(embed=em)




    @Server.command()
    async def ac(self, ctx):
        

        em = disnake.Embed(
                    title='Add Channel',
                    description="Adds a channel to this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.\nWhen adding a channel, if it goes under a category do channel-name, category name. Example: a'ac channel-name-example, category name example (comma and space must be used)"
                )
        em.add_field(name = 'Aliases', value = "(`a'add_channel <name>, <category (optional)>`, `a'ac <name>, <category (optional)>`)")
        await ctx.send(embed=em)                                                                                                                                                                                                                                                                                                                                            

    @Server.command()
    async def delete_channel(self, ctx):
        

        em = disnake.Embed(
                    title='Delete Channel',
                    description="Removes a channel from this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example."
                )
        em.add_field(name = 'Aliases', value = "(`a'dc <name>`, `a'delete_channel <name>`)")
        await ctx.send(embed=em)




    @Server.command()
    async def dc(self, ctx):
        

        em = disnake.Embed(
                    title='Delete Channel',
                    description="Removes a channel from this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example."
                )
        em.add_field(name = 'Aliases', value = "(`a'dc <name>`, `a'delete_channel <name>`)")
        await ctx.send(embed=em)

    @Server.command()
    async def delete_category(self, ctx):
        

        em = disnake.Embed(
                    title='Delete Category',
                    description="Removes a category from this server."
                )
        em.add_field(name = 'Aliases', value = "(`a'dcat <name>`, `a'delete_category <name>`)")
        await ctx.send(embed=em)     



    @Server.command()
    async def dcat(self, ctx):
        

        em = disnake.Embed(
                    title='Delete Category',
                    description="Removes a category from this server."
                )
        em.add_field(name = 'Aliases', value = "(`a'dcat <name>`, `a'delete_category <name>`)")
        await ctx.send(embed=em)
    
    @Server.command()
    async def add_member_role(self, ctx):
        

        em = disnake.Embed(
                    title='Add Member Role',
                    description="Adds a role to a member. (Must be spelled exactly as it is named. Case-sensitive.)"
                )
        em.add_field(name = 'Aliases', value = "(`a'amr <member> <role>`, `a'add_member_role <member> <role>`, `a'AMR <member> <role>`)")
        await ctx.send(embed=em)
        
    @Server.command()
    async def amr(self, ctx):
        

        em = disnake.Embed(
                    title='Add Member Role',
                    description="Adds a role to a member. (Must be spelled exactly as it is named. Case-sensitive.)"
                )
        em.add_field(name = 'Aliases', value = "(`a'amr <member> <role>`, `a'add_member_role <member> <role>`, `a'AMR <member> <role>`)")
        await ctx.send(embed=em)
    
    @Server.command()
    async def AMR(self, ctx):
        

        em = disnake.Embed(
                    title='Add Member Role',
                    description="Adds a role to a member. (Must be spelled exactly as it is named. Case-sensitive.)"
                )
        em.add_field(name = 'Aliases', value = "(`a'amr <member> <role>`, `a'add_member_role <member> <role>`, `a'AMR <member> <role>`)")
        await ctx.send(embed=em)
    


    @Server.command()
    async def add_server_role(self, ctx):
        

        em = disnake.Embed(
                    title='Add Server Role',
                    description="Adds a role to the server."
                )
        em.add_field(name = 'Aliases', value = "(`a'asr <name> `, `a'add_server_role <name>`, `a'ASR <name>`)")
        await ctx.send(embed=em)

    @Server.command()
    async def asr(self, ctx):
        

        em = disnake.Embed(
                    title='Add Server Role',
                    description="Adds a role to the server."
                )
        em.add_field(name = 'Aliases', value = "(`a'asr <name> `, `a'add_server_role <name>`, `a'ASR <name>`)")
        await ctx.send(embed=em)



    @Server.command()
    async def ASR(self, ctx):
        

        em = disnake.Embed(
                    title='Add Server Role',
                    description="Adds a role to the server."
                )
        em.add_field(name = 'Aliases', value = "(`a'asr <name> `, `a'add_server_role <name>`, `a'ASR <name>`)")
        await ctx.send(embed=em)

    @Server.command()
    async def remove_member_role(self, ctx):
        

        em = disnake.Embed(
                    title='Remove Member Role',
                    description="Removes a role from a member. (Must be spelled exactly. Case-Sensitive)"
                )
        em.add_field(name = 'Aliases', value = "(`a'rmr <member> <name>`, `a'remove_member_role <member> <name>`, `a'RMR <member> <name>`)")
        await ctx.send(embed=em)

    @Server.command()
    async def rmr(self, ctx):
        

        em = disnake.Embed(
                    title='Remove Member Role',
                    description="Removes a role from a member. (Must be spelled exactly. Case-Sensitive)"
                )
        em.add_field(name = 'Aliases', value = "(`a'rmr <member> <name>`, `a'remove_member_role <member> <name>`, `a'RMR <member> <name>`)")
        await ctx.send(embed=em)

    @Server.command()
    async def RSM(self, ctx):
        

        em = disnake.Embed(
                    title='Remove Member Role',
                    description="Removes a role from a member. (Must be spelled exactly. Case-Sensitive)"
                )
        em.add_field(name = 'Aliases', value = "(`a'rmr <member> <name>`, `a'remove_member_role <member> <name>`, `a'RMR <member> <name>`)")
        await ctx.send(embed=em)


    @Server.command()
    async def remove_server_role(self, ctx):
        

        em = disnake.Embed(
                    title='Remove Server Role',
                    description="Removes a role from this server."
                )
        em.add_field(name = 'Aliases', value = "(`a'rsr <role>`, `a'remove_server_role <role>`, `a'RSR <role>`)")
        await ctx.send(embed=em)


    @Server.command()
    async def rsr(self, ctx):
        

        em = disnake.Embed(
                    title='Remove Server Role',
                    description="Removes a role from this server."
                )
        em.add_field(name = 'Aliases', value = "(`a'rsr <role>`, `a'remove_server_role <role>`, `a'RSR <role>`)")
        await ctx.send(embed=em)


    @Server.command()
    async def RSR(self, ctx):
        

        em = disnake.Embed(
                    title='Remove Server Role',
                    description="Removes a role from this server."
                )
        em.add_field(name = 'Aliases', value = "(`a'rsr <role>`, `a'remove_server_role <role>`, `a'RSR <role>`)")
        await ctx.send(embed=em)

    
    @Server.command()
    async def purge(self, ctx):
        em = disnake.Embed(
            title = 'Purge',
            description='Removes messages from the channel it is used in. The default amount is 5.'
        )
        await ctx.send(embed=em)
    



    @help.group()
    async def Moderation(self, ctx):
        if ctx.invoked_subcommand is None:
            em = disnake.Embed(
                title='Moderation Category',
                description='The Moderation category of commands are used for Moderation, such as banning, warning, muting, etc.'
            )
            await ctx.send(embed=em)
    


    '''
    a'ban <member> <reason>
    a'clear_warns [member]
    a'delete_warn <member>
    a'get_mutes
    a'get_warns [member]
    a'kick [member] [reason]
    a'mute [member] [reason]
    a'unban <member>
    a'unmute [member]
    a'warn [member] [reason]'''




    @Moderation.command()
    async def ban(self, ctx):
        em = disnake.Embed(
            title = 'Ban',
            description="Bans a user from the server\n(`a'ban <member> <reason>`)"
        )
        await ctx.send(embed=em)

    
    @Moderation.command()
    async def unban(self, ctx):
        em = disnake.Embed(
            title='Unban',
            description="Unbans a member\n(`a'unban`)"
        )
        await ctx.send(embed=em)
    

    @Moderation.command()
    async def kick(self, ctx):
        em = disnake.Embed(
            title = 'Kick',
            description="Kicks a user from the server\n(`a'kick <member> <reason>`)"
        )
        await ctx.send(embed=em)

    @Moderation.command(aliases = ['cw', 'clearwarns'])
    async def clear_warns(self, ctx):
        em = disnake.Embed(
            title = 'Clear Warns',
            description="Clears all of a users warns. This is a very sensitive command and you will be prompted before using.]\n (`a'clear_warns <member>`, `a'clearwarns <member>`, `a'cw <member>`)"
        )
        await ctx.send(embed=em)

    
    @Moderation.command(aliases = ['dw', 'delwarn', 'deletewarn'])
    async def delete_warn(self, ctx):
        em = disnake.Embed(
            title = 'Delete Warn',
            description="Delete a warn from a member.\n(`a'delete_warn <member>`, `a'deletewarn <member>`, `a'delwarn <member>`, `a'dw <member>`)"
        )
        await ctx.send(embed=em)

    @Moderation.command()
    async def warn(self, ctx):
        em = disnake.Embed(
            title = 'Warn',
            description="Warns a member for your reason.\n(`a'warn <member> <reason>)"
        )
        await ctx.send(embed=em)

    

    @Moderation.command(aliases = ['gw', 'getwarns'])
    async def get_warns(self, ctx):
        em = disnake.Embed(
            title = 'Get Warns',
            description="Gets all of a member's warns.\n(`a'get_warns <member>`, `a'gm <member>`, `a'getwarns <member>`)"
        )
        await ctx.send(embed=em)
    
    @Moderation.command()
    async def mute(self, ctx):
        em = disnake.Embed(
            title = 'Mute',
            description="Mutes a member.\n(`a'mute <member> <reason>`)"
        )
        await ctx.send(embed=em)
    
    @Moderation.command()
    async def Unmute(self, ctx):
        em = disnake.Embed(
            title = 'Unmute',
            description="Unmutes a member.\n(`a'Unmute <member>`)"
        )
        await ctx.send(embed=em)
    

    @help.command()
    async def level(self, ctx):
        em = disnake.Embed(
            title='Level Category and System',
            description='The level system adds every user in your server as they speak. There is only one command.'

        )
        em.add_field(
            name = 'Stats',
            value="Shows the stats of your self or a member you mention.\n(`a'stats <member (defaults to yourself)>`"
        )
        await ctx.send(embed = em)
    
    @help.group()
    async def Info(self, ctx):
        if ctx.invoked_subcommand is None:
            em = disnake.Embed(
                title='Information',
                description='Commands that give useful information'
            )
            await ctx.send(embed=em)
    
    @Info.command()
    async def guildinfo(self, ctx):
        em = disnake.Embed(
            title='Gives Guild Information',
            description="`a'guildinfo`"
        )
        await ctx.send(embed=em)

    @Info.command()
    async def botinfo(self, ctx):
        em = disnake.Embed(
            title='Gives Bot Information',
            description="`a'botinfo`"
        )
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Help(bot))