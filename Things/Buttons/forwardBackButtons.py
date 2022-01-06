import disnake
from Things.Panels.mainPanel import HelpDropdown


class forwardBackButtons(disnake.ui.View):
    def __init__(self, timeout = 15):
        super().__init__(timeout = timeout)

    
    @disnake.ui.button(
        label = 'Back',
        style=disnake.ButtonStyle.danger,
        custom_id = 'forwardBackButtons:Back'
    )
    async def back(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        em = disnake.Embed(
            title = 'This is the help panel for my commands.',
            description= 'Please select a category from the dropdown menu below to get help.')
        await interaction.response.edit_message(embed = em, view = HelpDropdown())
    
    @disnake.ui.button(
        label = 'End',
        style = disnake.ButtonStyle.secondary,
        custom_id='forwardBackButtons:End'
    )
    async def end(self, button:disnake.ui.Button, interaction:disnake.Interaction):
        msg = await interaction.original_message()
        await msg.delete()

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        msg = await self.inter.original_message()
        await msg.edit(view=self)
