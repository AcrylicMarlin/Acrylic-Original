
import discord
from discord.ext import commands


class test_buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Test0', style=discord.ButtonStyle.green, custom_id='test_buttons:test0')
    async def test0(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(content='Test 0 Button Pressed.')
    
    @discord.ui.button(label='Test1', style=discord.ButtonStyle.red, custom_id='test_buttons:test1')
    async def test1(self, button:discord.ui.Button, interaction:discord.Interaction):
        
        await interaction.response.edit_message(content='Test 1 Button Pressed.')

    @discord.ui.button(label='Test2', style=discord.ButtonStyle.blurple, custom_id='test_buttons:test2')
    async def test2(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(content='Test 2 Button Pressed.')
    
    @discord.ui.button(label='Stop', style=discord.ButtonStyle.danger, custom_id='test_buttons:stop')
    async def stop(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(content='Stopping...')
        msg = interaction.message
        await msg.delete(delay=3.0)
    
    
class test_stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_blank_embed(self, ctx):
        em = discord.Embed(title = '\u200b')
        await ctx.send(embed = em)

    @commands.command()
    async def test_buttons(self, ctx):
        view = test_buttons()
        await ctx.message.delete()

        msg = await ctx.send('Test Buttons', view = test_buttons())
        view.msg = msg


def setup(bot):
    bot.add_cog(test_stuff(bot))