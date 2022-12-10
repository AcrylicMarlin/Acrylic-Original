# pyright: reportOptionalMemberAccess = false, reportGeneralTypeIssues = false

import os
import traceback
import sys

import discord
from discord.ext import commands
import asqlite

from cogs import EXTENSIONS



class AcrylicBot(commands.Bot):
    def __init__(self, database:asqlite.Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = database

    

    async def on_ready(self):
        print("Logging in...")
        print(f"User count: {len(self.users)}")
        print(f"Guild count: {len(self.guilds)}")
        print(f"Connected to {self.user.name}#{self.user.discriminator} ({self.user.id})")
        print("Logged in!")
    

    async def setup_hook(self) -> None:
        async with self.database.cursor() as cur:
            schema = open("schema.sql", "r").read()
            schemas = schema.split(";")
            for s in schemas:
                await cur.execute(s)
            
        print('Database setup complete!')

        for e in EXTENSIONS:
            try:
                await self.load_extension(e)
            except Exception as e:
                print(f"Failed to load extension {e}", file=sys.stderr)
                traceback.print_exc()

    



async def main():
    async with asqlite.connect("database.db") as db:
        bot = AcrylicBot(db, command_prefix="a!", intents=discord.Intents.all())
        async with bot:
            await bot.start(os.environ.get("TOKEN"))








