import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from Things.Panels.mainPanel import HelpDropdown
from Things.Panels.extraPanel import ExtraMenu
from Things.Panels.infoPanel import InfoMenu
from Things.Panels.modPanel import ModMenu










class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.slash_command(
        description='Sends the full help panel'
    )
    async def help(
        self,
        inter:disnake.ApplicationCommandInteraction
    ):
        em = disnake.Embed(
            title = 'This is the help panel for my commands.',
            description= 'Please select a category from the dropdown menu below to get help.')

        await inter.response.send_message(embed=em, view=HelpDropdown())



def setup(bot):
    bot.add_cog(Help(bot))