import psutil
import disnake
from disnake.ext import commands





class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        servers = self.bot.servers
        created = str(guild.created_at.timestamp())
        
        await servers.execute('INSERT INTO guilds VALUES (:guild_id, :name, :time, :count)', {'guild_id':guild.id, 'name':guild.name, 'time':created[:-4], 'count':guild.member_count})


    @commands.command()
    async def botinfo(self, ctx):
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
        em.set_footer(icon_url=ctx.author.avatar.url, text='Serving you always!')
        await ctx.send(embed=em)

    @commands.command()
    async def guildinfo(self, ctx):
        em = disnake.Embed(
            title = "{}'s info".format(ctx.guild.name),
            description='''
            Name: {}
            Number of users: {}
            Created <t:{}:R>
            You joined <t:{}:R>
            Owner: {}
            '''.format(ctx.guild.name, ctx.guild.member_count, int(ctx.guild.created_at.timestamp()), int(ctx.author.joined_at.timestamp()), ctx.guild.owner.display_name)
            
        )
        await ctx.send(embed=em)
    
    @commands.command()
    async def userinfo(self, ctx, member:disnake.Member=None):
        if member is None:
            member = ctx.author
        
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
        await ctx.send(embed = em)
        





def setup(bot):
    bot.add_cog(Info(bot))