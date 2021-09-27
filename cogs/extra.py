import random
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param



'''
Tables
role_data (guild_id integer, member_role text, admin_role, mod_role)
afk (guild_id integer, afk_sys integer)
level (guild_id integer, level_sys integer)
mutes (guild_id int, user_id int, admin_id int)
warns (guild_id int, user_id int, admin_id, int, reason text, time int, id int)
level_data (guild_id int, user_id int, exp int, level int)
afk_data (user_id int NOT NULL UNIQUE, reason int, time int)
'''
test_guild = [859565691597226016]
class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.slash_command(
        guild_ids = test_guild,
        description='Gets the bots ping'
        )
    async def ping(
        self,
        inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f'Pong! `{int(round(self.bot.latency, 2) * 100)} ms`')










    @commands.slash_command(
        guild_ids=test_guild,
        description = 'Agrees with your bruh.'
    )
    async def bruh(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.send_message('Fr')










    @commands.slash_command(
        guild_ids=test_guild,
        name = '8ball',
        description = 'Ask a question and it gives you an answer.')
    async def magicBall(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question: str = Param(name = 'question', description = 'Input your question')
    ):
        responses = ['It is certain',
                        'It is decidedly so',
                        'Without a doubt',
                        'Yes, definitely',
                        'You may rely on it',
                        'As I see it, yes',
                        'Most likely',
                        'Outlook good',
                        'Yes',
                        'Signs point to yes',
                        'Reply hazy try again',
                        'Ask again later',
                        'Better not tell you now',
                        'Cannot predict now',
                        'Concentrate and ask again',
                        "Don't count on it",
                        'My reply is no',
                        'My sources say no',
                        'Outlook not so good',
                        'Very doubtful']
        choice = random.choice(responses)

        embed = disnake.Embed(
            title = '***Magic 8Ball***',
            description = 'Your question was:\n**{}**.\nYour answer is:\n*{}*'.format(question, choice))
        
        await inter.response.send_message(embed = embed)


        
    

    



    
        
        
    
def setup(bot):
    bot.add_cog(Extra(bot))