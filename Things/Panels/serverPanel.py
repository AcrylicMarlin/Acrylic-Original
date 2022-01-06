import disnake

'''
em.add_field(name = "Add Category (`a'add_category <name>`, `a'acat <name>`)", value="Adds a category to this server.", inline = False)
em.add_field(name = "Add Channel (`a'add_channel <name>, <category (optional)>`, `a'ac <name>, <category (optional)>`)", value= "Adds a channel to this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.\nWhen adding a channel, if it goes under a category do channel-name, category name. Example: a'ac channel-name-example, category name example (comma and space must be used)", inline = False)
em.add_field(name = "Delete Channel (`a'dc <name>`, `a'delete_channel <name>`)", value= "Removes a channel from this server. When using, remember that the channel name must have dashes between words. For example: a'ac new-channel-example.", inline = False)
em.add_field(name = "Delete Category (`a'dcat <name>`, `a'delete_category <name>`)", value="Removes a channel from this server.", inline = False)
em.add_field(name = "Add Member Role (`a'amr <member> <role>`, `a'add_member_role <member> <role>`, `a'AMR <member> <role>`)", value = 'Adds a role to a member. (Must be spelled exactly as it is named. Case-sensitive.)', inline = False)
em.add_field(name = "Add Server Role (`a'asr <name> `, `a'add_server_role <name>`, `a'ASR <name>`)", value="Adds a role to this server.", inline = False)
em.add_field(name = "Remove Member Role (`a'rmr <member> <name>`, `a'remove_member_role <member> <name>`, `a'RMR <member> <name>`)", value="Removes a role from a member. (Must be spelled exactly as it is named. Case-sensitive.)", inline = False)
em.add_field(name = "Remove Server Role (`a'rsr <role>`, `a'remove_server_role <role>`, `a'RSR <role>`)", value= "Removes a role from a server. (Must be spelled exactly as it is named. Case-sensitive.)", inline = False)
em.add_field(name = "Purge (`a'purge <amount (Defaults at 5)>`)", value='Clears messages from the channel it is used in.', inline=False)'''


class serverSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label = 'Add Category'
            ),
            disnake.SelectOption(
                label = 'Add Channel'
            ),
            disnake.SelectOption(
                label = 'Add Member Role'
            ),
            disnake.SelectOption(
                label = 'Add Server Role'
            ),
            disnake.SelectOption(
                label = 'Delete Category'
            ),
            disnake.SelectOption(
                label = 'Delete Channel'
            ),
            disnake.SelectOption(
                label = 'Remove Member Role'
            ),
            disnake.SelectOption(
                label = 'Remove Server Role'
            ),
            disnake.SelectOption(
                label = 'Purge'
            )
        ]
        super().__init__(options=options, placeholder='Select the commands you need',min_values=1, max_values=1)

    async def callback(self, interaction:disnake.Interaction):
        if self.values[0] == 'Add Category':
            em = disnake.Embed(
                title = 'Add Category [Name (Required)]',
                description=''
            )
        elif self.values[0] == 'Add Channel':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Add Member Role':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Add Server Role':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Delete Category':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Delete Channel':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Remove Member Role':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Remove Server Role':
            em = disnake.Embed(
                title = ''
            )
        elif self.values[0] == 'Purge':
            em = disnake.Embed(
                title = ''
            )
