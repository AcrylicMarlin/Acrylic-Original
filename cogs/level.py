import math
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import asyncio


class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot








    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        servers  = self.bot.servers
        user = message.author
        guild = message.guild
        if message.author == self.bot.user:
            return
        # lvl_amt = lvl*100 + lvl*50
        cur = await servers.execute('SELECT level FROM systems WHERE guild_id = :guild_id', {'guild_id':message.guild.id})
        data = await cur.fetchone()
        level_sys = data[0]
        if level_sys == 1:

        
            c = await servers.execute('SELECT exp, level FROM level_data WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':guild.id, 'user_id':user.id})


            try:
                level = await c.fetchone()
            except AttributeError:
                print('New User in level_data.')
                level = []

            if not level:
                await servers.execute('INSERT INTO level_data VALUES (:guild_id, :user_id, 0, 1)', {'guild_id':guild.id, 'user_id':user.id})
                
            else:

                xp, lvl = level
                plus = lvl//2
                if plus == 0:
                    xp += 2
                else:
                    xp+=plus

                await servers.execute('UPDATE level_data SET exp = :exp WHERE guild_id = :guild_id AND user_id = :user_id',{'exp':xp, 'guild_id':guild.id, 'user_id':user.id})
                


            cur = await servers.execute('SELECT exp, level FROM level_data WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':guild.id, 'user_id':user.id})
            data = await cur.fetchone()
            xp, lvl = data

            if xp == ((lvl*100)+(lvl*50)):
                await message.channel.send('You have done it {}. Congrats on reaching level {}.'.format(user.mention, lvl+1), delete_after = 10)
                await servers.execute('UPDATE level_data SET level = :level WHERE guild_id = :guild_id AND user_id = :user_id', {'level':lvl+1, 'guild_id':guild.id, 'user_id':user.id})

            else:
                return

        else:
            
            return


    @commands.slash_command()
    async def stats(
        self,
        inter:disnake.ApplicationCommandInteraction,
        member:disnake.Member=Param(None, name = 'member', description = 'person you want to see (defaults to yourself)')):
        servers  = self.bot.servers
        cur = await servers.execute('SELECT level FROM systems WHERE guild_id = :guild_id', {'guild_id':inter.guild.id})
        data = await cur.fetchone()
        level_sys = data[0]
        if level_sys == 1:
            if member is None:

                c = await servers.execute('SELECT exp, level FROM level_data WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':inter.guild.id, 'user_id':inter.author.id})
                data = await c.fetchone()
                xp,lvl=data
                em = disnake.Embed(
                    title="{}'s Level Stats".format(inter.author.display_name),
                    )

                exp_left =(lvl*100+lvl*50) - xp
                em.set_thumbnail(url=inter.author.avatar.url)
                em.set_footer(text = 'Your Stats', icon_url=self.bot.user.avatar.url)
                em.add_field(name='\u200b', value='Your are level {}.'.format(lvl), inline=False)
                em.add_field(name='\u200b', value='Exp left to next rank {}'.format(exp_left), inline=False)
                await inter.response.send_message(embed=em)
            else:
                c = await servers.execute('SELECT exp, level FROM level_data WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':inter.guild.id, 'user_id':member.id})
                data = await c.fetchone()
                xp,lvl=data
                em = disnake.Embed(
                    title="{}'s Level Stats".format(member.display_name),
                    )

                exp_left =(lvl*100+lvl*50) - xp
                em.set_thumbnail(url=member.avatar.url)
                em.set_footer(text = "{}'s Stats".format(member.display_name), icon_url=self.bot.user.avatar.url)
                em.add_field(name='\u200b', value='Your are level {}.'.format(lvl), inline=False)
                em.add_field(name='\u200b', value='Exp left to next rank {}'.format(exp_left), inline=False)
                await inter.response.send_message(embed=em)

        else:
            await inter.response.send_message('Your admins have disabled this system for this server.')







    @commands.Cog.listener()
    async def on_member_remove(self, member):
        servers = self.bot.servers
        cur = await servers.execute('SELECT level FROM systems WHERE guild_id = :guild_id', {'guild_id':member.guild.id})
        data = await cur.fetchone()
        level_sys = data[0]
        if level_sys == 1:
            await servers.execute('DELETE FROM level_data WHERE guild_id = :guild_id AND user_id = :user_id', {'guild_id':member.guild.id, 'user_id':member.id})
            
        else:
            return




def setup(bot):
    bot.add_cog(level(bot))


            


    


    
