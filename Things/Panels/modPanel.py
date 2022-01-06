import disnake
from Things.Buttons.forwardBackButtons import forwardBackButtons


class OneOneModSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            
            disnake.SelectOption(
                label = 'Ban',
                description='Bans a member'
            ),
            disnake.SelectOption(
                label = 'Unban',
                description='Unbans a member using their id'
            ),
            disnake.SelectOption(
                label='Kick',
                description='Kicks a member'
            ),
            disnake.SelectOption(
                label = 'Warn',
                description='Warns a member for an infraction'
            ),
            disnake.SelectOption(
                label='Delete Warn',
                description='Deletes the most recent warn.'
            ),
            disnake.SelectOption(
                label = 'Get Warns',
                description='Get all of the warns'
            ),
            disnake.SelectOption(
                label = 'Clear Warns',
                description='Clears all warns from a user'
            ),
            disnake.SelectOption(
                label = 'Mute',
                description='Mutes a user'
            ),
            disnake.SelectOption(
                label = 'Unmute',
                description='Unmutes a user'
            ),
            disnake.SelectOption(
                label = 'Get Mutes',
                description='Gets all mutes for the server'
            )
            ]
        super().__init__(placeholder='Select the commands you need', options=options, min_values=1, max_values=1)

        async def callback(self, interaction:disnake.Interaction):
            if self.values[0] == 'Ban':
                em = disnake.Embed(
                    title = 'Ban [Member (Required)] [Reason (Optional)]',
                    description='Bans a member'
                )
                
            elif self.values[0] == 'Unban':
                em = disnake.Embed(
                    title = 'Unban [ID (Required)]',
                    description='Unbans a user using their ID.'
                )
                
            elif self.values[0] == 'Kick':
                em = disnake.Embed(
                    title = 'Kick [Member (Required)] [Reason (Optional)]',
                    description='Kicks a member'
                )
            elif self.values[0] == 'Warn':
                em = disnake.Embed(
                    title = 'Warn [Member (Required)] [Reason (Required)]',
                    description='Warns a member for an infraction you specify'
                )
            elif self.values[0] == 'Delete Warn':
                em = disnake.Embed(
                    title = 'Delete Warn [Member (Required)]',
                    description='Delete the most recent warn from a member'
                )
            elif self.values[0] == 'Get Warns':
                em = disnake.Embed(
                    title = 'Get Warns [Member (Required)]'
                )
            elif self.values[0] == 'Clear Warns':
                em = disnake.Embed(
                    title = 'Clear Warns [Member (Required)]',
                    description='''
                    Removes all warns from a user
                    ***DANGER*** *This command should not be used lightly. You will be prompted for confirmation.*'''
                )
            elif self.values[0] == 'Mute':
                em = disnake.Embed(
                    title = 'Mute [Member (Required)] [Reason (Optional)]',
                    description='Mutes a member'
                )
            elif self.values[0] == 'Unmute':
                em = disnake.Embed(
                    title = 'Unmute [Member (Required)]',
                    description='Umutes a muted member'
                )
            else:
                em = disnake.Embed(
                    title = 'Get Mutes',
                    description='Get all of the muted member in this server.'
                )
            await interaction.response.edit_message(embed = em, view = forwardBackButtons())

class OneZeroModSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label = 'Mute',
                description='Mutes a user'
            ),
            disnake.SelectOption(
                label = 'Unmute',
                description='Unmutes a user'
            ),
            disnake.SelectOption(
                label = 'Get Mutes',
                description='Gets all mutes for the server'
            ),
            disnake.SelectOption(
                label = 'Ban',
                description='Bans a member'
            ),
            disnake.SelectOption(
                label = 'Unban',
                description='Unbans a member using their id'
            ),
            disnake.SelectOption(
                label='Kick',
                description='Kicks a member'
            )
            
        ]
        super().__init__(placeholder='Select the commands you need', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == 'Ban':
            em = disnake.Embed(
                title = 'Ban [Member (Required)] [Reason (Optional)]',
                description='Bans a member'
            )
            
        elif self.values[0] == 'Unban':
            em = disnake.Embed(
                title = 'Unban [ID (Required)]',
                description='Unbans a user using their ID.'
            )
            
        elif self.values[0] == 'Kick':
            em = disnake.Embed(
                title = 'Kick [Member (Required)] [Reason (Optional)]',
                description='Kicks a member')
        elif self.values[0] == 'Mute':
            em = disnake.Embed(
                title = 'Mute [Member (Required)] [Reason (Optional)]',
                description='Mutes a member'
            )
        elif self.values[0] == 'Unmute':
            em = disnake.Embed(
                title = 'Unmute [Member (Required)]',
                description='Umutes a muted member'
            )
        else:
            em = disnake.Embed(
                title = 'Get Mutes',
                description='Get all of the muted member in this server.'
            )
        await interaction.response.edit_message(embed = em, view = forwardBackButtons())
class ZeroOneModSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label = 'Ban',
                description='Bans a member'
            ),
            disnake.SelectOption(
                label = 'Unban',
                description='Unbans a member using their id'
            ),
            disnake.SelectOption(
                label='Kick',
                description='Kicks a member'
            ),
            disnake.SelectOption(
                label = 'Warn',
                description='Warns a member for an infraction'
            ),
            disnake.SelectOption(
                label='Delete Warn',
                description='Deletes the most recent warn.'
            ),
            disnake.SelectOption(
                label = 'Get Warns',
                description='Get all of the warns'
            ),
            disnake.SelectOption(
                label = 'Clear Warns',
                description='Clears all warns from a user'
            )
        ]
        super().__init__(placeholder='Select the commands you need', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == 'Ban':
            em = disnake.Embed(
                title = 'Ban [Member (Required)] [Reason (Optional)]',
                description='Bans a member'
            )
            
        elif self.values[0] == 'Unban':
            em = disnake.Embed(
                title = 'Unban [ID (Required)]',
                description='Unbans a user using their ID.'
            )
            
        elif self.values[0] == 'Kick':
            em = disnake.Embed(
                title = 'Kick [Member (Required)] [Reason (Optional)]',
                description='Kicks a member')
        elif self.values[0] == 'Warn':
                em = disnake.Embed(
                    title = 'Warn [Member (Required)] [Reason (Required)]',
                    description='Warns a member for an infraction you specify'
                )
        elif self.values[0] == 'Delete Warn':
            em = disnake.Embed(
                title = 'Delete Warn [Member (Required)]',
                description='Delete the most recent warn from a member'
            )
        elif self.values[0] == 'Get Warns':
            em = disnake.Embed(
                title = 'Get Warns [Member (Required)]'
            )
        elif self.values[0] == 'Clear Warns':
            em = disnake.Embed(
                title = 'Clear Warns [Member (Required)]',
                description='''
                Removes all warns from a user
                ***DANGER*** *This command should not be used lightly. You will be prompted for confirmation.*'''
            )
        await interaction.response.send_message(embed = em, view = forwardBackButtons())

    
class ZeroZeroModSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label = 'Ban',
                description='Bans a member'
            ),
            disnake.SelectOption(
                label = 'Unban',
                description='Unbans a member using their id'
            ),
            disnake.SelectOption(
                label='Kick',
                description='Kicks a member'
            )
        ]
        super().__init__(placeholder='Select the commands you need', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == 'Ban':
            em = disnake.Embed(
                title = 'Ban [Member (Required)] [Reason (Optional)]',
                description='Bans a member'
            )
            
        elif self.values[0] == 'Unban':
            em = disnake.Embed(
                title = 'Unban [ID (Required)]',
                description='Unbans a user using their ID.'
            )
            
        elif self.values[0] == 'Kick':
            em = disnake.Embed(
                title = 'Kick [Member (Required)] [Reason (Optional)]',
                description='Kicks a member')
        await interaction.response.send_message(embed = em, view = forwardBackButtons())


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
a'warn [member] [reason]
'''



class ModMenu(disnake.ui.View):
    def __init__(self, inter, warn, mute):
        self.inter = inter
        self.warn = warn
        self.mute = mute

        if self.mute == 1 and self.warn == 1:
            self.add_item(OneOneModSelect())
        elif self.mute == 1 and self.warn == 0:
            self.add_item(OneZeroModSelect())
        elif self.mute == 0 and self.warn == 1:
            self.add_item(ZeroOneModSelect())
        else:
            self.add_item(ZeroZeroModSelect())


    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        msg = await self.inter.original_message()
        await msg.edit(view=self)