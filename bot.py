import json
import logging
import os
import ssl

import asyncpg
import discord
from discord.ext import commands
from ruamel.yaml import YAML

startup_extensions = ["fun", "moderation", "admin", "franxx"]
extensions = ["cogs." + ext for ext in startup_extensions]

yaml = YAML()
try:
    with open("config.yaml") as f:
        config = yaml.load(f)
        token = config["token"]
        db = config["db"]
except:  # noqa
    token = os.environ.get("TOKEN")
    db = os.environ.get("DATABASE_URL")

logging.basicConfig(level=logging.INFO)


class ZeroTwo(commands.Bot):
    def __init__(self):
        game = discord.Game(name="with my Darling~ <3")
        super().__init__(command_prefix=commands.when_mentioned_or("d>"),
                         description="Zero Two Bot for the Darling in the FranXX server",
                         game=game)
        self.pool = None

    async def close(self):
        print("Cleaning up...")
        await self.pool.close()
        await super().close()

    async def on_ready(self):
        if self.pool is None:
            # open a connection pool to the database
            self.pool = await asyncpg.create_pool(db, ssl=ssl.SSLContext(), loop=self.loop)
        query = """
            SELECT * FROM mute
        """
        self.muted_roles = {g: r for g, r in await self.pool.fetch(query)}

        print("Ready!")
        print(self.user.name)
        print(self.user.id)
        print("~-~-~-~")
        print("Cogs loaded:")
        for i, ext in enumerate(extensions):
            try:
                self.load_extension(ext)
                print(f"Loaded {startup_extensions[i]}.")
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {ext}\n{exc}')
        print("~-~-~-~")

    async def on_message(self, message):  # allow case-insensitive commands
        ctx = await self.get_context(message)
        if ctx.prefix is not None:
            ctx.command = self.all_commands.get(ctx.invoked_with.lower())
            await self.invoke(ctx)


ZeroTwo().run(token)
