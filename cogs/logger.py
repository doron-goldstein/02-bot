import discord


class Logger:
    def __init__(self, bot):
        self.bot = bot
        self.log_chan = bot.get_channel(413861854343856128)
        self.colors = {
            "edit": discord.Color.teal,
            "delete": discord.Color.dark_red
        }

    async def log_message(self, action, message, new_msg=None):
        embed = discord.Embed(title="Message " + action, description=f"", color=self.colors[action])
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.add_field(name="Content", value=message.content)
        if action == "edit":
            embed.add_field(name="Edited Content", value=new_msg.content)
        await self.log_chan.send(embed=embed)

    async def on_message_delete(self, message):
        await self.log_message("delete", message)

    async def on_message_edit(self, message, new_msg):
        await self.log_message("edit", message, new_msg)


def setup(bot):
    bot.add_cog(Logger(bot))
