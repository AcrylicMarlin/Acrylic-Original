import disnake
from disnake.ext import commands
import asqlite
from dotenv import load_dotenv
import os
load_dotenv()
guild_id = int(os.environ.get("TEST_GUILD"))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(guild_ids=[guild_id])
    async def help(self, inter:disnake.ApplicationCommandInteraction):
        pageContentLimit = 5
        slash = {}
        for command in self.bot.application_commands:
            slash[command.body.name] = {
                'Cog' : command.cog,
                'Desc' : command.body.description}
        print(slash)
        inter.response.send_message('Completed')

def setup(bot):
    bot.add_cog(Help(bot))