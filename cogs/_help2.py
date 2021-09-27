import asyncio
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param


test_guild = [859565691597226016]

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
        


    
    

    
        






class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.slash_command(description = 'Gets help per command', guild_ids = test_guild)
    async def helpcommand(
        self,
        inter: disnake.ApplicationCommandInteraction,
        category: str = Param(name = 'category', description = 'Which category of commands do you need?'),
        command: str = Param(name = 'command', description='Which command do you need?')
    ):
        if category == 'Moderation':
            


















    @commands.slash_command(
        description='Sends the full help panel',
        guild_ids=test_guild
    )
    async def help(
        self,
        inter:disnake.ApplicationCommandInteraction
    ):
        em = disnake.Embed(
            title = 'This is the help panel for my commands.',
            description= 'Please select a category from the dropdown menu below to get help.')
        
        await inter.response.send_message(embed=em, view=HelpDropdown(inter))
        
        
        
        
        
        
        








def setup(bot):
    bot.add_cog(Help(bot))