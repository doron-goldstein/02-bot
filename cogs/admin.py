import inspect
from contextlib import redirect_stdout
from io import StringIO
import time
from traceback import format_exception

from discord.ext import commands

# eval imports
import asyncio  # noqa
import discord  # noqa
import os  # noqa
import sys  # noqa


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, ext):
        ext = "cogs." + ext
        try:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            await ctx.author.send(f"Failed to reload cog: `{ext}`\n    {exc}")
        else:
            await ctx.message.add_reaction("\N{OK HAND SIGN}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        env = {
            "ctx": ctx,
            "message": ctx.message,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "author": ctx.author,
            "bot": ctx.bot,
            "history": await ctx.history().flatten()
        }
        env.update(globals())

        code = code.strip("`")
        code = code.replace("py\n", "")
        fmt = "async def e():\n"
        fmt += "\n".join(["    " + ln for ln in code.split("\n")])
        out = StringIO()

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
            res = f"```py\n{result}```"
            if len(res) > 2000:
                return await ctx.send("Result was too large, hasted:\n" + self.bot.make_haste(res))
            else:
                return await ctx.send(res)

        except:  # noqa
            try:
                exec(fmt, env)
                with redirect_stdout(out):
                    result = await env["e"]()
            except Exception as e:
                result = ''.join(format_exception(None, e, e.__traceback__, chain=False))
        stdout = out.read()
        if stdout is not "" or result is not None:
            res = f"```py\n{out.read()}\n{result}```"
            if len(res) > 2000:
                await ctx.send("Result was too large, hasted:\n" + self.bot.make_haste(res))
            else:
                await ctx.send(res)

    @commands.command(hidden=True)
    async def ping(self, ctx):
        before = time.monotonic()
        msg = await ctx.send("Pinging... \N{TABLE TENNIS PADDLE AND BALL}")
        after = time.monotonic()
        ping = round((after - before) * 1000, 2)
        await msg.edit(content=f"\N{TABLE TENNIS PADDLE AND BALL} Pong! **{ping}**ms")


def setup(bot):
    bot.add_cog(Admin(bot))
