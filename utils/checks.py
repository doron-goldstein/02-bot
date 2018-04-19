from discord.ext import commands


FRANXX_ID = 391483719803994113
BOT_CHANNEL = 391490499527311361


def super_check(check):
    async def predicate(ctx):
        if ctx.author.id == ctx.bot.owner_id:
            return True
        return check(ctx)
    return commands.check(predicate)


def restricted():
    """Restrict commands to #bot_channel"""
    async def predicate(ctx):
        if ctx.guild.id == FRANXX_ID:
            return ctx.channel.id == BOT_CHANNEL
        return True
    return commands.check(predicate)


def mods_only(ctx):
    perms = ctx.author.guild_permissions
    return perms.kick_members and perms.ban_members
