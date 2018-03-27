import discord
from discord.ext import commands


class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 391490980249075722
        self.msg_id = 417823406617001987
        self.emoji_server_id = 417804713413836830
        # self.reaction_manager = {
        #     'SeXX': 407759891927924737,
        #     '02bounce': 402315991918575636,
        #     'strelizia': 392894112036159499,
        #     'argentea': 392894507424940034,
        #     'delphinium': 392894559853477899,
        #     'genista': 392894894999601153,
        #     'chlorophytum': 392894974234198026,
        #     'cah': 406564673345814542,
        #     'ThotPatrol': 405107014356697099,
        #     'BlueOni': 412069721832292372,
        #     '🎤': 416893959814512641,
        #     'klaxo': 403740756105363457,
        #     'terraria': 424639819852021763
        # }

    async def cmdcheck(ctx):
        return ctx.author.id == 111158853839654912

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

    async def on_raw_reaction_add(self, emoji, message_id, channel_id, user_id):
        guild = self.bot.get_channel(channel_id).guild
        member = guild.get_member(user_id)
        if message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.bot.reaction_manager[emoji.name])
        if role in member.roles:
            return

        await member.add_roles(role)

    async def on_raw_reaction_remove(self, emoji, message_id, channel_id, user_id):
        guild = self.bot.get_channel(channel_id).guild
        member = guild.get_member(user_id)
        if message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.bot.reaction_manager[emoji.name])
        if role not in member.roles:
            return

        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
