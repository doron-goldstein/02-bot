import discord
from discord.ext import commands


class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 434836251766423564
        self.msg_id = 434842027692130304
        self.emoji_server_id = 417804713413836830

    async def cmdcheck(ctx):
        return ctx.author.id == 111158853839654912 or ctx.author.guild_permissions.manage_roles

    @commands.check(cmdcheck)
    @commands.command(hidden=True)
    async def addrole(self, ctx, role: discord.Role, emoji_name, url=None):
        """Adds a new role to the reaction role manager."""

        c = self.bot.get_channel(self.channel_id)
        msg = await c.get_message(self.msg_id)

        if emoji_name in self.bot.reaction_manager:
            return await ctx.send("Role has already been added!")
        if len(msg.reactions) == 20:
            return await ctx.send("Cannot add role! Too many roles exist. [Reaction reached 20 Emoji]")

        if url is None:
            if len(ctx.message.attachments) > 0:
                url = ctx.message.attachments[0].url
        resp = await self.bot.session.get(url)
        img = await resp.read()

        try:
            guild = self.bot.get_guild(self.emoji_server_id)
            emoji = await guild.create_custom_emoji(name=emoji_name, image=img)
        except:  # noqa
            return await ctx.send("Could not create emoji!")

        await msg.add_reaction(emoji)
        self.bot.reaction_manager[emoji_name] = role.id

        query = """
            INSERT INTO roles (emoji_name, role_id) VALUES ($1, $2)
        """
        
        await self.bot.pool.execute(query, emoji_name, role.id)
        await ctx.send(f"Added `{emoji_name}` as an assignable role!")

    async def on_raw_reaction_add(self, event):
        guild = self.bot.get_guild(event.guild_id)
        member = guild.get_member(event.user_id)
        if event.message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.bot.reaction_manager[event.emoji.name])
        if role in member.roles:
            return

        await member.add_roles(role)

    async def on_raw_reaction_remove(self, event):
        guild = self.bot.get_guild(event.guild_id)
        member = guild.get_member(event.user_id)
        if event.message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.bot.reaction_manager[event.emoji.name])
        if role not in member.roles:
            return

        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
