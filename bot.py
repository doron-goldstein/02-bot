import asyncio
import os
import ssl
from datetime import datetime

import aiohttp
import aioredis
import asyncpg
import discord
from discord.ext import commands
from ruamel.yaml import YAML


startup_extensions = ["fun", "moderation", "admin", "franxx", "logger", "roles", "errors", "spook]
extensions = ["cogs." + ext for ext in startup_extensions]
yaml = YAML()
config = None
try:
    with open("config.yaml") as f:
        config = yaml.load(f)
        token = config["token"]
        db = config["db"]
        redis = (config["redis_addr"], config["redis_pw"])
        img_auth = config["img_auth"]
        dev = True
except:  # noqa
    token = os.environ.get("TOKEN")
    db = os.environ.get("DATABASE_URL")
    redis = (os.environ.get("REDIS_ADDR"), os.environ.get("REDIS_PW"))
    img_auth = os.environ.get("WOLKE_TOKEN")
    dev = False


async def get_prefix(bot, msg):
    return commands.when_mentioned_or("d>")(bot, msg) if dev else commands.when_mentioned_or(">", "02 ")(bot, msg)


class ZeroTwo(commands.Bot):
    def __init__(self):
        game = discord.Game(name="with my Darling~ <3")
        super().__init__(command_prefix=get_prefix,
                         description="Zero Two Bot for the Darling in the FranXX server",
                         activity=game)
        self.owner_id = 111158853839654912
        self._config = config
        self.img_auth = "Wolke " + img_auth
        self.pool = None
        self.redis = None
        self.session = None

    async def close(self):
        print("Cleaning up...")
        await self.pool.close()
        await self.session.close()
        self.redis.close()
        await self.redis.wait_closed()
        await super().close()

    async def block_dms(self, ctx):
        return ctx.guild is not None

    async def on_ready(self):
        self.check(self.block_dms)  # haha yes
        if self.pool is None:
            self.pool = await asyncpg.create_pool(db, ssl=ssl.SSLContext(), loop=self.loop)

        if self.redis is None:
            self.redis = await aioredis.create_redis_pool("redis://" + redis[0], password=redis[1],
                                                          minsize=5, maxsize=10, loop=self.loop)

        if self.session is None:
            self.session = aiohttp.ClientSession()

        role_query = """
            SELECT * FROM mute_roles
        """
        emoji_query = """
            SELECT * FROM reaction_roles
        """
        config_query = """
            SELECT * FROM config
        """
        mute_query = """
            SELECT * FROM mute_states
        """
        spamguard_query = """
            SELECT channel_id FROM spamguard_blacklist
        """

        async with self.pool.acquire() as conn:
            self.muted_roles = {g: r for g, r in await conn.fetch(role_query)}
            self.reaction_manager = {e: r for e, r in await conn.fetch(emoji_query)}
            self.config = {g: {'do_welcome': w, 'echo_mod_actions': m} for g, w, m in await conn.fetch(config_query)}
            self.muted_members = {r['member_id']: dict(r) for r in await conn.fetch(mute_query)}
            self._spamguard_blacklist = [r['channel_id'] for r in await conn.fetch(spamguard_query)]

        await self.handle_mutes()
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
        self.error_handler = self.get_cog('Errors').on_command_error
        print("~-~-~-~")

    async def handle_mutes(self):
        for m_id, d in self.muted_members.items():
            if not d['muted']:
                continue
            self.loop.create_task(self.ensure_unmute(m_id, d))

    async def ensure_unmute(self, m_id, data):
        now = datetime.utcnow()
        end = data['mute_timeout']
        if end is None:
            return

        if end < now:  # mute time passed
            reason = "Auto-unmuted."
            guild = self.get_guild(data['guild_id'])
            if guild is None:
                return
            mod = guild.me
            original_mod = guild.get_member(data['muter_id'])
            member = guild.get_member(m_id)
            cog = self.get_cog('Moderation')
            await cog._do_unmute(member, reason=reason, mod=mod, guild=guild)
            embed = discord.Embed(title="Member Auto-unmuted", timestamp=datetime.now())
            embed.add_field(name="Original Moderator", value=str(original_mod))
            embed.set_author(name=f"{member} / {member.id}", icon_url=member.avatar_url)
            if guild == cog.log_chan.guild:
                await cog.log_chan.send(embed=embed)

        else:  # wait, then try again
            await asyncio.sleep((end - now).total_seconds())
            await self.ensure_unmute(m_id, data)

    async def make_haste(self, text, *, raw=False):
        url = "https://hastebin.com/"
        resp = await self.session.post("https://hastebin.com/documents", data=text)
        data = await resp.json()
        if raw:
            return url + "raw/" + data['key']
        return url + data['key']

    async def on_message(self, message):  # allow case-insensitive commands
        ctx = await self.get_context(message)
        if ctx.author.bot:
            return
        if ctx.prefix is not None:
            ctx.command = self.all_commands.get(ctx.invoked_with.lower())
            await self.invoke(ctx)


ZeroTwo().run(token)
