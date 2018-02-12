import discord
from discord.ext.commands import command
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.lockdown_msg = {}
        self.log_chan = {391483719803994113: self.bot.get_channel(410189085714546698)}
        self.mute_role = discord.utils.get(self.bot.get_guild(391483719803994113).roles, id=392897098875404289)
        self.embed_colors = {
            "kick": 0xffa500,
            "ban": 0xff0000,
            "warn": 0xffff00,
            "mute": 0xa52a2a,
            "unmute": 0x73dcff
        }

    async def __local_check(self, ctx):
        perms = ctx.author.guild_permissions
        return perms.kick_members and perms.ban_members

    async def log_action(self, action, *, member, reason=None, mod=None):
        embed = discord.Embed(title=f"Member {action}", description=reason, color=self.embed_colors[action])
        embed.add_field(name="Moderator", value=mod)
        embed.set_author(name=f"{member} / {member.id}", icon_url=member.avatar_url)
        if not self.log_chan.get(member.guild.id):
            return
        await self.log_chan[member.guild.id].send(embed=embed)

    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.BadArgument):
            await ctx.send(f"Incorrect usage. Try `{ctx.prefix}help {ctx.command}` for more info.")
        else:
            raise err

    @command(aliases=['silence', 'gag'], hidden=True)
    async def lockdown(self, ctx):
        await ctx.message.delete()
        self.lockdown_msg[ctx.guild.id] = await ctx.send("This channel is now under lockdown!")
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

    @command(aliases=['ungag'], hidden=True)
    async def unlock(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
        if self.lockdown_msg.get(ctx.guild.id):
            await self.lockdown_msg[ctx.guild.id].delete()
        await ctx.send("This channel is no longer under lockdown.", delete_after=10)

    @command(hidden=True)
    async def kick(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        await ctx.guild.kick(target, reason=reason)
        await self.log_action("kick", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True)
    async def ban(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        await target.ban()
        await self.log_action("ban", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True)
    async def mute(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        await target.add_roles(self.mute_role)
        await self.log_action("mute", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True)
    async def unmute(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        await target.remove_roles(self.mute_role)
        await self.log_action("unmute", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True)
    async def warn(self, ctx, target: discord.Member, *, warning=None):
        await ctx.message.delete()
        try:
            if warning is None:
                await target.send(f"You've received a warning from {ctx.author}!")
            else:
                await target.send(f"You've received a warning from {ctx.author}:\n \"{warning}\"")
                await self.log_action("warn", member=target, reason=warning, mod=ctx.author)
        except:  # noqa
            await ctx.author.send(f"Could not send a warning to `{target}`.\n"
                                  "They may have DMs disables, or have blocked me.\n\n"
                                  f"Warning text was:\n{warning}")


def setup(bot):
    bot.add_cog(Moderation(bot))
