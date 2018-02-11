import os
import logging
# import ssl

# import asyncpg
import discord
from discord.ext import commands

startup_extensions = ["fun", "moderation"]
extensions = ["cogs." + ext for ext in startup_extensions]
try:
    with open("token") as f:
        token = f.readline()
except:  # noqa
    token = os.environ.get("TOKEN")
logging.basicConfig(level=logging.INFO)


class ZeroTwo(commands.Bot):
    def __init__(self):
        game = discord.Game(name="with my Darling~ <3")  # playing with my Darling~ <3
        super().__init__(command_prefix=commands.when_mentioned_or("02 ", ">"),
                         description="Zero Two Bot for the Darling in the FranXX server",
                         game=game)

    async def close(self):
        await self.pool.close()  # close database pool
        await super().close()

    async def on_ready(self):
        # database if needed
        # self.pool = await asyncpg.create_pool(os.environ["DATABASE_URL"], ssl=ssl.SSLContext(), loop=self.loop)
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
