import disnake
from Things.Buttons.forwardBackButtons import forwardBackButtons







class InfoSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                name = 'Guildinfo'
            ),
            disnake.SelectOption(
                name = 'Botinfo'
            ),
            disnake.SelectOptiont(
                name = 'Userinfo'
            )
        ]
        super().__init__(placeholder='Select the commands you need',options=options, min_values=1, max_values=1)
    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == 'Guildinfo':
            em = disnake.Embed(
                title='Guildinfo',
                description='Gets information pertaining to the guild this is called in.'
            )
        elif self.values[0] =='Botinfo':
            em = disnake.Embed(
                title = 'Botinfo',
                description='Gets the information pertaining to Acrylic'
            )
        else:
            em = disnake.Embed(
                title = 'Userinfo',
                description='Gets information on a user you ping or yourself if you choose not to provide a member'
            )
        await interaction.response.edit_message(embed=em, view = forwardBackButtons())

class InfoMenu(disnake.ui.View):
    def __init__(self, inter, timeout = 15.0):
        super().__init__(timeout=timeout)
        self.inter = inter

        self.add_item(InfoSelect())

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        msg = await self.inter.original_message()
        await msg.edit(view=self)


    