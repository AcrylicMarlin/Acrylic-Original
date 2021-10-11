import psutil
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param





class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        servers = self.bot.servers
        created = str(guild.created_at.timestamp())
        
        await servers.execute('INSERT INTO guilds VALUES (:guild_id, :name, :time, :count)', {'guild_id':guild.id, 'name':guild.name, 'time':created[:-4], 'count':guild.member_count})


    @commands.slash_command()
    async def botinfo(self, inter):
        mem = psutil.virtual_memory()
        '''Displays information on Acrylic'''
        em = disnake.Embed(
            title='My Info',
            description=f'''
            *My Version*: 2.0
            *Discord API Version*: {disnake.__version__}
            *My Prefix*: Slash Commands B)
            *Hardware Usage*: 
                Cpu: {psutil.cpu_percent()}%
                Memory: {mem[2]}%
            *Servers I'm in*: {len(self.bot.guilds)}
            *Users I'm Serving*: {len(set(self.bot.users))}'''
        )
        em.set_thumbnail(url=self.bot.user.avatar.url)
        em.set_footer(icon_url=inter.author.avatar.url, text='Serving you always!')
        await inter.send(embed = em)

    @commands.slash_command()
    async def guildinfo(self, inter):
        em = disnake.Embed(
            title = "{}'s info".format(inter.guild.name),
            description='''
            Name: {}
            Number of users: {}
            Created <t:{}:R>
            You joined <t:{}:R>
            Owner: {}
            '''.format(inter.guild.name, inter.guild.member_count, int(inter.guild.created_at.timestamp()), int(inter.author.joined_at.timestamp()), inter.guild.owner.display_name)
            
        )
        await inter.send(embed=em)
    
    @commands.slash_command()
    async def userinfo(self,
     inter,
     member:disnake.Member = Param(name = 'member', description = 'Ping the member you would like to see.') ):
        if member is None:
            member = inter.author
        
        mappedList = list(map(lambda x: x.mention, member.roles[1:]))
        roles = ', '.join(list(map(lambda x: x.strip("'"), mappedList)))

        em = disnake.Embed(
            title="{}'s Information",
            description='''
            Name: {}
            Joined Discord <t:{}:R>
            Joined this server <t:{}:R>
            Roles:
            {}

            '''.format(member.display_name, int(member.created_at.timestamp()), int(member.joined_at.timestamp()), roles)
        )
        await inter.send(embed = em)
        





def setup(bot):
    bot.add_cog(Info(bot))