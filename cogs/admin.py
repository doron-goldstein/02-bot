import inspect
from contextlib import redirect_stdout
from io import StringIO
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
            "bot": ctx.bot
        }
        env.update(globals())

        code = code.strip("`")
        code = code.lstrip("py\n")
        fmt = "async def e():\n"
        fmt += "\n".join(["    " + ln for ln in code.split("\n")])
        out = StringIO()

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
            return await ctx.send(f"```py\n{result}```")
        except:  # noqa
            try:
                exec(fmt, env)
                with redirect_stdout(out):
                    result = await env["e"]()
            except Exception as e:
                result = ''.join(format_exception(None, e, e.__traceback__))
        stdout = out.read()
        if stdout is not "" or result is not None:
            await ctx.send(f"```py\n{out.read()}\n{result}```")


def setup(bot):
    bot.add_cog(Admin(bot))
