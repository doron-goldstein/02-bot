from discord.ext import commands


FRANXX_ID = 391483719803994113
BOT_CHANNEL = 391490499527311361


def restricted():
    """Restrict commands to #bot_channel"""
    async def predicate(ctx):
        if ctx.guild.id == FRANXX_ID:
            if ctx.channel.id == BOT_CHANNEL:
                return True
            return False
    return commands.check(predicate)
