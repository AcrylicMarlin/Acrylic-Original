    # @commands.command()
    # @commands.has_permissions(administrator = True)
    # async def config(self, ctx):
    #     servers = self.bot.servers


    #     c = await servers.execute('SELECT * FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #     data = await c.fetchone()
    #     guild, afk, level, warn, mute, welcome, server = data

    #     if afk == 1:
    #         afk = ':white_check_mark:'
    #     else:
    #         afk = ':x:'
        
    #     if level == 1:
    #         level = ':white_check_mark:'
    #     else:
    #         level = ':x:'

    #     if warn == 1:
    #         warn = ':white_check_mark:'
    #     else:
    #         warn = ':x:'

    #     if mute == 1:
    #         mute = ':white_check_mark:'

    #     else:
    #         mute = ':x:'
    #     if welcome == 1:
    #         welcome = ':white_check_mark:'
    #     else:
    #         welcome = ':x:'

    #     if server == 1:
    #         server = ':white_check_mark:'
    #     else:
    #         server = ':x:'
            
        
    #     em = discord.Embed(title = 'Configuration Panel',
    #         description = 'This is where you enable and disable certain systems.\n:one: - Afk System{}\n:two: - Leveling System {}\n:three: - Warn System {}\n:four: - Mute System {}\n:five: - Welcome/Leave System {}\n:six: - Server Configuration System {}'.format(afk, level, warn, mute, welcome, server))
            
            
    #     em.add_field(name = 'Select Each number to enable/disable.', value = 'Select X when finished')
    #     msg = await ctx.send(embed = em)
    #     await msg.add_reaction('1️⃣')
    #     await msg.add_reaction('2️⃣')
    #     await msg.add_reaction('3️⃣')
    #     await msg.add_reaction('4️⃣')
    #     await msg.add_reaction('5️⃣')
    #     await msg.add_reaction('6️⃣')
    #     await msg.add_reaction('❌')

        
    #     while True:

    #         reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣','❌']
    #         def check(reaction, user):
    #             return user == ctx.author and str(reaction.emoji) in reactions
            
        
    #         try:
    #             reaction, user = await self.bot.wait_for('reaction_add', timeout = 60, check=check)
    #         except asyncio.TimeoutError:
    #             await ctx.send('Menu timed out, deleting.', delete_after = 5)
    #             await msg.clear_reactions()
    #             await msg.delete()
    #         if str(reaction.emoji) == '1️⃣':
    #             if afk == ':x:':
                   
    #                 await servers.execute('UPDATE systems SET afk = 1 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #             else:
                    
    #                 await servers.execute('UPDATE systems SET afk = 0 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #         elif str(reaction.emoji) == '2️⃣':
    #             if level == ':x:':
                    
    #                 await servers.execute('UPDATE systems SET level = 1 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #             else:
                    
    #                 await servers.execute('UPDATE systems SET level = 0 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
                
    #         elif str(reaction.emoji) == '3️⃣':
    #             if warn == ':x:':
                    
    #                 await servers.execute('UPDATE systems SET warn = 1 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #             else:
                    
    #                 await servers.execute('UPDATE systems SET warn = 0 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #         elif str(reaction.emoji) == '4️⃣':
    #             if mute == ':x:':
                    
    #                 await servers.execute('UPDATE systems SET mute = 1 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #             else:
                    
    #                 await servers.execute('UPDATE systems SET mute = 0 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #         elif str(reaction.emoji) == '5️⃣':
    #             if welcome == ':x:':
                    
    #                 await servers.execute('UPDATE systems SET welcome = 1 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #             else:

    #                 await servers.execute('UPDATE systems SET welcome = 0 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #         elif str(reaction.emoji) == '6️⃣':
    #             if server == ':x:':
                    
    #                 await servers.execute('UPDATE systems SET server = 1 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #             else:
                    
    #                 await servers.execute('UPDATE systems SET server = 0 WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #                 await reaction.remove(ctx.author)
    #         elif str(reaction.emoji) == '❌':
    #             await msg.delete()
    #             await ctx.send('Setup complete.')
    #             break
            
    #         c = await servers.execute('SELECT * FROM systems WHERE guild_id = :guild_id', {'guild_id':ctx.guild.id})
    #         data = await c.fetchone()
    #         guild, afk, level, warn, mute, welcome, server = data

    #         if afk == 1:
    #             afk = ':white_check_mark:'
    #         else:
    #             afk = ':x:'

    #         if level == 1:
    #             level = ':white_check_mark:'
    #         else:
    #             level = ':x:'

    #         if warn == 1:
    #             warn = ':white_check_mark:'
    #         else:
    #             warn = ':x:'

    #         if mute == 1:
    #             mute = ':white_check_mark:'

    #         else:
    #             mute = ':x:'
    #         if welcome == 1:
    #             welcome = ':white_check_mark:'
    #         else:
    #             welcome = ':x:'

    #         if server == 1:
    #             server = ':white_check_mark:'
    #         else:
    #             server = ':x:'    





    #         em1 = discord.Embed(title = 'Configuration Panel',
    #         description = 'This is where you enable and disable certain systems.\n:one: - Afk System{}\n:two: - Leveling System {}\n:three: - Warn System {}\n:four: - Mute System {}\n:five: - Welcome/Leave System {}\n:six: - Server Configuration System {}'.format(afk, level, warn, mute, welcome, server))
    #         await msg.edit(embed=em1)