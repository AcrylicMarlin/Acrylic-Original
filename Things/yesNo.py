import disnake
class yesNo(disnake.ui.View):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(timeout=10)


    @disnake.ui.button(
        label='Yes',
        style=disnake.ButtonStyle.green,
        custom_id='yesNo:Yes'
    )
    async def yes(
        self,
        button:disnake.ui.Button,
        inter:disnake.Interaction):
        await inter.response.send('Ok')
        channel = await inter.guild.create_text_channel(name = self.channel)
        await channel.send(f'{inter.author.mention} Channel Created!')

    @disnake.ui.button(
        label='No',
        style=disnake.ButtonStyle.danger,
        custom_id='yesNo:No'
    )
    async def no(
        self,
        inter:disnake.Interaction,
        button:disnake.ui.Button
    ):
        await inter.response.send_message('Ok, retry the command.')

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        msg = await self.inter.original_message()
        await msg.edit(view=self)