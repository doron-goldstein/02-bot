import json

import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands import command


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.log_chan = self.bot.get_channel(413010299776532490)
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
        embed = discord.Embed(title=f"Member {action}", description=reason)
        embed.color = self.embed_colors[action]
        embed.timestamp = datetime.now()

        embed.add_field(name="Moderator", value=mod)
        embed.set_author(name=f"{member} / {member.id}", icon_url=member.avatar_url)
        if member.guild.id == 391483719803994113:
            await self.log_chan.send(embed=embed)

    async def on_guild_channel_create(self, channel):
        if channel.guild.id in self.bot.muted_roles:
            r_id = self.bot.muted_roles[channel.guild.id]
            role = discord.utils.get(channel.guild.roles, id=r_id)
            await channel.set_permissions(role, send_messages=False)

    async def on_command_error(self, ctx, err):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(err, commands.CommandNotFound):
            return
        if isinstance(err, commands.BadArgument):
            await ctx.send(f"Incorrect usage. Try `{ctx.prefix}help {ctx.command}` for more info.")
        if isinstance(err, commands.NoPrivateMessage):
            await ctx.send(f"This command cannot be used in DMs.")
        else:
            raise err

    @command(hidden=True)
    async def lock(self, ctx):
        await ctx.message.delete()
        msg = await ctx.send("This channel is now under lockdown!")
        perms = ctx.channel.overwrites_for(ctx.guild.default_role)

        query = """
            INSERT INTO lockdown (channel_id, message_id, perms) VALUES ($1, $2, $3)
        """
        await self.bot.pool.execute(query, ctx.channel.id, msg.id, json.dumps(perms._values))

        perms.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)

    @command(hidden=True)
    async def unlock(self, ctx):
        await ctx.message.delete()
        query = """
            DELETE FROM lockdown WHERE channel_id=$1 RETURNING *
        """
        recs = await self.bot.pool.fetchrow(query, ctx.channel.id)
        if not recs:
            return

        channel_id, msg_id, perms = recs
        msg = await self.bot.get_channel(channel_id).get_message(msg_id)
        await msg.delete()

        perms = discord.PermissionOverwrite(**json.loads(perms))
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        await ctx.send("This channel is no longer under lockdown.", delete_after=10)

    @command(hidden=True)
    async def kick(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        await target.kick(reason=reason)
        await self.log_action("kick", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True)
    async def ban(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        await target.ban(reason=reason, delete_message_days=0)
        await self.log_action("ban", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True, aliases=['gag'])
    async def mute(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        r_id = self.bot.muted_roles.get(ctx.guild.id)
        if not r_id:
            role = await ctx.guild.create_role(name="Muted")
            r_id = role.id
            self.bot.muted_roles[ctx.guild.id] = r_id
            for c in ctx.guild.text_channels:
                await c.set_permissions(role, send_messages=False)

            query = """
                INSERT INTO mute (guild_id, role_id) VALUES ($1, $2)
            """
            await self.bot.pool.execute(query, ctx.guild.id, role.id)

        role = discord.utils.get(ctx.guild.roles, id=r_id)
        await target.add_roles(role)
        await self.log_action("mute", member=target, reason=reason, mod=ctx.author)

    @command(hidden=True, aliases=['ungag'])
    async def unmute(self, ctx, target: discord.Member, *, reason=None):
        await ctx.message.delete()
        r_id = self.bot.muted_roles[ctx.guild.id]
        if r_id:
            role = discord.utils.get(ctx.guild.roles, id=r_id)
            if role:
                await target.remove_roles(role)
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

    @command(hidden=True, aliases=['prune', 'p'])
    async def purge(self, ctx, count: int, *users: discord.Member):
        await ctx.message.delete()
        if count > 100:
            await ctx.send(f"You are about to purge {count}. Are you sure you want to purge these many messages? (y/n)")

            def check(m):
                (m.content.lower() == 'y' or m.content.lower() == 'n') and m.author == ctx.message.author
            try:
                reply = await self.bot.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                return await ctx.send("Cancelled purge.")
            if not reply or reply.content.lower().strip() == 'n':
                return await ctx.send("Cancelled purge.")
            else:
                await ctx.message.delete()
        try:
            await ctx.channel.purge(limit=count, check=lambda message: message.author in users if users else True)
        except discord.HTTPException:
            await ctx.send("Something went wrong! Could not purge.")


def setup(bot):
    bot.add_cog(Moderation(bot))
