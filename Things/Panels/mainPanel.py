import disnake
from disnake.ext import commands
from disnake.ext.commands import Param






class HelpSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label='Moderation',
                description='Moderation Help',

            ),
            disnake.SelectOption(
                label='Server Configuration',
                description='Server Configuration Help'
            ),
            disnake.SelectOption(
                label='Information',
                description='Information Help'
            ),
            disnake.SelectOption(
                label='Setup',
                description='Setup Help'
            ),
            disnake.SelectOption(
                label='AFK',
                description='AFK System Help'
            ),
            disnake.SelectOption(
                label='Level',
                description='Level System Help'
            ),
            disnake.SelectOption(
                label='Economy',
                description='Economy System Help'
            ),
            disnake.SelectOption(
                label = 'Configuration',
                description = 'System Configuration Help'
            ),
            disnake.SelectOption(
                label = 'Help',
                description = 'Command Help'
            ),
            disnake.SelectOption(
                label = 'Extra',
                description = 'Extra Commands Help'
            )
        ]



        super().__init__(placeholder='Select the category you want to see.', min_values=1, max_values=1, options= options)


    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        if self.values[0] == 'Moderation':
            pass
        elif self.values[0] == 'Server Configuration':
            pass
        elif self.values[0] == 'Information':
            pass
        elif self.values[0] == 'Setup':
            pass
        elif self.values[0] == 'AFK':
            pass
        elif self.values[0] == 'Level':
            pass
        elif self.values[0] == 'Economy':
            pass
        elif self.values[0] == 'Configuration':
            pass
        elif self.values[0] == 'Help':
            pass
        elif self.values[0] == 'Extra':
            pass
        await interaction.response.edit_message(content = f'{self.values[0]}')




class HelpDropdown(disnake.ui.View):
    def __init__(self, inter, timeout = 15.0):
        super().__init__(timeout=timeout)
        self.inter = inter

        self.add_item(HelpSelect())

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        msg = await self.inter.original_message()
        await msg.edit(view=self)