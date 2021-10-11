import random
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param




test_guild = [859565691597226016]
class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.slash_command(
        description='Gets the bots ping'
        )
    async def ping(
        self,
        inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f'Pong! `{int(round(self.bot.latency, 2) * 100)} ms`')










    @commands.slash_command(
        description = 'Agrees with your bruh.'
    )
    async def bruh(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.send_message('Fr')










    @commands.slash_command(
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