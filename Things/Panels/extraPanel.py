import disnake
from Things.Buttons.forwardBackButtons import forwardBackButtons







class ExtraSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label = 'Ping'
            ),
            disnake.SelectOption(
                name = '8Ball'
            ),
            disnake.SelectOption(
                name = 'Bruh'
            )
        ]
        super().__init__(placeholder='Select the commands you need', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == 'Ping':
            em = disnake.Embed(
                title = 'Ping',
                description="Returns the Bot's latency (ping)."
            )
        elif self.values[0] == '8Ball':
            em = disnake.Embed(
                title='8Ball',
                description='Ask a question and Acrylic will give you a wise answer'
            )
        else:
            em = disnake.Embed(
                title = 'Bruh',
                description='First command Acrylic ever responded to. Agrees with your bruh.'
            )
        await interaction.response.edit_message(embed = em, view = forwardBackButtons())
        


class ExtraMenu(disnake.ui.View):
    def __init__(self, inter, timeout = 15.0):
        super().__init__(timeout=timeout)
        self.inter = inter

        self.add_item(ExtraSelect())

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        msg = await self.inter.original_message()
        await msg.edit(view=self)
