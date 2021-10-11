import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import asqlite
from datetime import datetime
import random




class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    


    async def user_info_insert(self, user):
        async with asqlite.connect('Economy.db') as conn:
            async with conn.cursor() as cur:
                c = await cur.execute('SELECT user_id FROM users WHERE user_id = :user_id', {'user_id':user.id})
                data = await c.fetchone()
                

                if data is None:
                    await cur.execute('INSERT INTO users VALUES (:user_id, :username, :time)', {'user_id': user.id, 'username':user.display_name, 'time':round(datetime.now().timestamp())})
                    return False
                else:
                    return True
                    
                
    

    async def create_bank(self, user):
        if not (await self.user_info_insert(user)):


            async with asqlite.connect('Economy.db') as conn:
                async with conn.cursor() as cur:
                    await cur.execute('INSERT INTO bank VALUES (:user_id, 0, 100)', {'user_id':user.id})
        
    









    @commands.slash_command()
    async def balance(self,
    inter: disnake.ApplicationCommandInteraction,
    member:disnake.Member=Param(None, description = 'Member to see (You if blank)')):
        if member is None:
            member = inter.author
        

        await self.create_bank(member)
        
        async with asqlite.connect('Economy.db') as conn:
            async with conn.cursor() as cur:
                data = await (await cur.execute('SELECT cash, bank FROM bank WHERE user_id = :user_id', {'user_id':member.id})).fetchone()
                if data is None:
                    await inter.reply('Member {} has not been registered in my system.'.format(member.mention))
                    return
                cash, bank = data

        em = disnake.Embed(
            title="{}'s Balance".format(member.display_name),
            description='''
            ***Bank***: {}
            
            ***Cash***: {}'''.format(int(bank), int(cash))
        )
        em.set_footer(icon_url = self.bot.user.avatar.url, text=f'Serving {member.display_name}')
        await inter.send(embed = em)


    @commands.slash_command()
    async def beg(
        self,
        inter:disnake.ApplicationCommandInteraction):
        await self.create_bank(inter.author)
        chance = random.randrange(0, 101)

        if chance >= 50:
            money = random.randrange(0, 101)
            em = disnake.Embed(
                title='Someone gave you {}AC!'.format(money),
                description='''*Although you did get coins, there is big chance you won't, and you dont get very much.
                There are better ways to make money man.*'''
            )

            
            async with asqlite.connect('Economy.db') as conn:
                async with conn.cursor() as cur:
                    await cur.execute('UPDATE bank SET cash = (SELECT cash WHERE user_id = user_id) + :amount WHERE user_id = :user_id', {'user_id':inter.author.id, 'amount':money})
            await inter.send(embed = em)
        else:
            em = disnake.Embed(
                title = 'No coins for you.',
                description='No one was nice enough to give you any coins. There are better ways to get AC man.'
            )
            await inter.send(embed = em)

        
        
    @commands.slash_command()
    async def withdraw(self,
    inter:disnake.ApplicationCommandInteraction,
    amount: int = Param(name = 'amount', description = 'amount to withdraw')):
        await self.create_bank(inter.author)
        try:
            amount = int(amount)
            async with asqlite.connect('Economy.db') as conn:
                async with conn.cursor() as cur:
                    bank = (await (await cur.execute('SELECT bank FROM bank WHERE user_id = :user_id',{'user_id':inter.author.id})).fetchone())[0]
                    if int(bank) == 0:
                        await inter.reply('There is no money to pull out of your bank.')
                        return
                    if int(bank) < amount:
                        await inter.reply("You don't have that much money. I'm not a charity!")

                    else:
                        
                        await cur.execute('UPDATE bank SET cash =(SELECT cash FROM bank WHERE user_id = :user_id) + :amount, bank = (SELECT bank FROM bank WHERE user_id = :user_id) - :amount', {'amount':amount, 'user_id':inter.author.id})
                        await inter.reply('Withdrew {}AC'.format(amount))
        except ValueError:
            arg = ' '.join((inter.message.content.split(' '))[1:])
            if arg != 'max':

                await inter.reply('"{}" is not a number.'.format(arg))
                return
            else:
                async with asqlite.connect('Economy.db') as conn:
                    async with conn.cursor() as cur:
                        bank = (await (await cur.execute('SELECT bank FROM bank WHERE user_id = :user_id',{'user_id':inter.author.id})).fetchone())[0]
                        if int(bank) == 0:
                            await inter.reply('There is no money to pull out of your bank.')
                            return
                        

                        else:
                            amount = (await (await cur.execute('SELECT bank FROM bank WHERE user_id = :user_id', {'user_id':inter.author.id})).fetchone())[0]
                            await cur.execute('UPDATE bank SET cash =(SELECT cash FROM bank WHERE user_id = :user_id) + :amount, bank = (SELECT bank FROM bank WHERE user_id = :user_id) - :amount', {'amount':amount, 'user_id':inter.author.id})
                            await inter.reply('Withdrew {}AC'.format(amount))
                
              
        
        
    

                
        
                


                
                    
                
    @commands.slash_command()
    async def deposit(self,
    inter: disnake.ApplicationCommandInteraction,
    amount: int = Param(name = 'amount', description = 'amount to withdraw')):
        await self.create_bank(inter.author)
        try:
            amount = int(amount)
            async with asqlite.connect('Economy.db') as conn:
                async with conn.cursor() as cur:
                    cash = (await (await cur.execute('SELECT cash FROM bank WHERE user_id = :user_id',{'user_id':inter.author.id})).fetchone())[0]
                    if int(cash) == 0:
                        await inter.reply("You... don't have any money to give.")
                        return
                    elif int(cash) < amount:
                        await inter.reply("You don't have that much money on hand.")
                        return
                    else:
                        
                        await cur.execute('UPDATE bank SET cash =(SELECT cash FROM bank WHERE user_id = :user_id) - :amount, bank = (SELECT bank FROM bank WHERE user_id = :user_id) + :amount', {'amount':amount, 'user_id':inter.author.id})
                        await inter.reply('Depostied {}AC'.format(amount))
        except ValueError:
            arg = ' '.join((inter.message.content.split(' '))[1:])
            if arg != 'max':

                await inter.reply('"{}" is not a number.'.format(arg))
                return
            else:
                
                
                    
                async with asqlite.connect('Economy.db') as conn:
                    async with conn.cursor() as cur:
                        cash = (await (await cur.execute('SELECT cash FROM bank WHERE user_id = :user_id',{'user_id':inter.author.id})).fetchone())[0]
                        
                        if int(cash) == 0:
                            await inter.reply("You... don't have any money to give.")
                            return
                        
                        amount = (await (await cur.execute('SELECT cash FROM bank WHERE user_id = :user_id', {'user_id':inter.author.id})).fetchone())[0]
                        await cur.execute('UPDATE bank SET cash =(SELECT cash FROM bank WHERE user_id = :user_id) - :amount, bank = (SELECT bank FROM bank WHERE user_id = :user_id) + :amount', {'amount':amount, 'user_id':inter.author.id})
                        await inter.reply('Depostied {}AC'.format(amount))
                        
        

        
        

        
        
                


        

    
    




        


    


                    









def setup(bot):
    bot.add_cog(Economy(bot))