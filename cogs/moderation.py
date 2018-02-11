# import discord
from discord.ext.commands import command


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.lockdown_msg = None

    async def __local_check(self, ctx):
        perms = ctx.author.guild_permissions
        return perms.kick_members and perms.ban_members

    @command(aliases=['silence', 'gag'], hidden=True)
    async def lockdown(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        self.lockdown_msg = await ctx.send("This channel is now under lockdown!")

    @command(aliases=['ungag'], hidden=True)
    async def unlock(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
        await self.lockdown_msg.delete() if self.lockdown_msg else None
        await ctx.send("This channel is no longer under lockdown.", delete_after=10)


def setup(bot):
    bot.add_cog(Moderation(bot))
