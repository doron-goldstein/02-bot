class Story:
    def __init__(self, bot):
        self.bot = bot
        self.channel = bot.get_channel(542389702792183828)

    async def on_message(self, message):
        if message.channel != self.channel:
            return

        perms = message.author.guild_permissions
        if (perms.kick_members and perms.ban_members) or message.author.id == 111158853839654912:
            return

        if "".join(message.content.split()) != message.content:
            await message.delete()
            return

        if len(message.content) > 45:
            await message.delete()
            return

        history = await self.channel.history(limit=2).flatten()
        author = history[1].author
        if author == message.author:
            await message.delete()


def setup(bot):
    bot.add_cog(Story(bot))
