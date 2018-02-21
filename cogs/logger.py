import discord


class Logger:
    def __init__(self, bot):
        self.bot = bot
        self.log_chan = bot.get_channel(413889551740960790)
        self.colors = {
            "edit": discord.Color.teal(),
            "delete": discord.Color.dark_red()
        }

    async def log_message(self, action, message, new_msg=None):
        if message.author.bot:
            return
        embed = discord.Embed(title="Message " + action, description=f"", color=self.colors[action])
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.add_field(name="Channel", value=message.channel.mention)
        if message.content:
            embed.add_field(name="Content", value=message.content, inline=False)
        if message.attachments and new_msg is None:
            embed.set_image(url=message.attachments[0].proxy_url)
            if len(message.attachments) > 1:
                embed.add_field(name="Attachments", value="\n".join(a.url for a in message.attachments[1:]))
        if action == "edit":
            embed.add_field(name="Edited Content", value=new_msg.content, inline=False)
        await self.log_chan.send(embed=embed)

    async def on_message_delete(self, message):
        if message.guild == self.log_chan.guild:
            await self.log_message("delete", message)

    async def on_message_edit(self, old, new):
        if old.content != new.content:
            if old.guild == self.log_chan.guild:
                await self.log_message("edit", old, new)


def setup(bot):
    bot.add_cog(Logger(bot))
