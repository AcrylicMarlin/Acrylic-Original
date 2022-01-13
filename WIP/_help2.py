import asyncio
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from enum import Enum


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






class HelpOptions(Enum):
	"""Contains _returnOptions

	Args:
		category (string): Category chosen by user
	"""	
	def __init__(self, category):
		self.category = category

	async def _returnOptions(self):
		"""Returns options based on provided category"""
		
		if self.category == 'Moderation':
			
			

			async with open('guild_data.db') as conn:
				async with conn.cursor() as cur:
					warn, mute = (await (await cur.execute('SELECt warn, mute FROM systems WHERE guild_id = :guild_id')).fetchone())


			if warn == 1 and mute == 1:
				return commands.option_enum({
					'Ban':'Ban',
					'Kick':'Kick',
					'Unban':'Unban',
					'Warn':'Warn',
					'Get Warns':'Get Warns',
					'Delete Warn':'Delete Warn',
					'Clear Warns':'Clear Warns',
					'Mute':'Mute',
					'Unmute':'Unmute'
				})
			if warn != 1 and mute == 1:
				return commands.option_enum({
					'Ban':'Ban',
					'Kick':'Kick',
					'Unban':'Unban',
					'Mute':'Mute',
					'Unmute':'Unmute'
				})
			if warn == 1 and mute != 1:
				return commands.option_enum({
					'Ban':'Ban',
					'Kick':'Kick',
					'Unban':'Unban',
					'Warn':'Warn',
					'Get Warns':'Get Warns',
					'Delete Warns':'Delete Warns',
					'Clear Warns':'Clear Warns'
				})
			if warn != 1 and mute != 1:
				return commands.option_enum({
					'Ban':'Ban',
					'Unban':'Unban',
					'Kick':'Kick'
				})
					
		
		elif self.category == 'Server':
			async with open('guild_data.db') as conn:
				async with conn.cursor() as cur:
					server = (await (await cur.execute('SELECT server FROM systems WHERE guild_id = :guild_id')).fetchone())[0]
					if server != 1:
						return {
							'Disabled':'Disabled'
						}
					else:
						return {
							'Add Category':'Add Category',
							'Add Channel':'Add Channel',
							'Delete Channel':'Delete Channel',
							'Delete Category':'Delete Category',
							'Add Member Role':'Add Member Role',
							'Add Server Role':'Add Server Role',
							'Remove Member Role':'Remove Member Role',
							'Purge':'Purge'
						}

			
		elif self.category == 'Setup':
			pass
		elif self.category == 'Info':
			return {
				'BotInfo':'BotInfo',
				'GuildInfo':'GuildInfo',
				'UserInfo':'UserInfo'
			}
		elif self.category == 'Economy':
			return {
				'Balance':'Balance',
				'Beg':'Beg',
				'Withdraw':'Withdraw',
				'Deposit':'Deposit'
			}
		elif self.category == 'Level':
			async with open('guild_data.db') as conn:
				async with conn.cursor() as cur:
					level = (await (await cur.execute('SELECT level FROM systems WHERE guild_id=:guild_id')).fetchone())[0]
					if level != 1:
						return {
							'Disabled':'Disabled'
						}
					else:
						return {
							'Stats':'Stats'
						}
		elif self.category == 'Configuration':
			return {
				'Config':'Config',
				'Enabled List':'Enabled List'
			}
		elif self.category == 'AFK':
			async with open('guild_data.db') as conn:
				async with conn.cursor() as cur:
					afk = (await (await cur.execute('SELECT afk FROM systems WHERE guild_id=:guild_id')).fetchone())[0]
					if afk != 1:
						return {
							'Disabled':'Disabled'
						}
					else:
						return {
							'AFK':'AFK'
						}







class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	@commands.slash_command(description = 'Gets help per command', guild_ids = test_guild)
	async def helpcommand(
		self,
		inter: disnake.ApplicationCommandInteraction,
		category: Param(choices={'Moderation':'Moderation', 'Server':'Server', 'Setup':'Setup', 'Info':'Info', 'Economy':'Economy', 'Level':'Level', 'Configuration':'Configuration', 'AFK':'AFK', 'Extra':'Extra'}),
		command: Param()
	):
		if category == 'Moderation':
			pass



















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