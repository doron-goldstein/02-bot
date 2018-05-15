from discord.ext import commands
from utils.checks import mods_only


class Errors:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, err):
        # if hasattr(ctx.command, 'on_error'):  # should be ok to remove this
        #     return

        if isinstance(err, commands.CommandNotFound):
            return

        elif isinstance(err, commands.BadArgument):
            await ctx.send(f"Incorrect usage. Try `{ctx.prefix}help {ctx.command}` for more info.")

        elif isinstance(err, commands.NoPrivateMessage):
            await ctx.send(f"This command cannot be used in DMs.")

        elif isinstance(err, commands.CommandOnCooldown):
            if mods_only(ctx):
                return await ctx.reinvoke()
            await ctx.send(err.args[0], delete_after=5)
            await ctx.message.add_reaction("\N{HOURGLASS}")

        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(err.args[0])

        elif isinstance(err, commands.CheckFailure):
            return

        else:
            raise err


def setup(bot):
    bot.add_cog(Errors(bot))
