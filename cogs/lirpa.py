import discord
from discord.ext import commands


class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 429686036751187968
        self.msg_id = 429693967840444416
        self.reaction_manager = {
            'nsfwtext': 407759891927924737,
            'nsfwpics': 402315991918575636,
            'crimson': 392894112036159499,
            'coyote': 392894507424940034,
            'gipsy': 392894559853477899,
            'cherno': 392894894999601153,
            'striker': 392894974234198026,
            'cah': 406564673345814542,
            'kaijupatrol': 405107014356697099,
            'newtlieb': 412069721832292372,
            '🎤': 416893959814512641,
            'kaiju': 403740756105363457,
            'terraria': 424639819852021763,
            'warframe': 428196015938732034
        }

    @commands.has_permissions(kick_members=True, ban_members=True)
    @commands.command()
    async def pentecost(self, ctx):
        await ctx.send("""```One: don't you ever ping me again.

Two: don't you ever ping me again.

Now you have no idea who the hell I am, of which anime Discord I've come from, and I'm not about to tell you my extensive list of nicknames. All I need to be to you and every Ranger on this Discord is a ban hammer. The last mod standing. I do not need your >pat or your >sync. All I need is you to read rules and your discussion skills. And if I can't get that, then you can go back to the DarliFranXX Discord where I found you crawling on. Do I make myself clear? Good.```""")

    async def on_raw_reaction_add(self, emoji, message_id, channel_id, user_id):
        guild = self.bot.get_channel(channel_id).guild
        member = guild.get_member(user_id)
        if message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.reaction_manager[emoji.name])
        if role in member.roles:
            return

        await member.add_roles(role)

    async def on_raw_reaction_remove(self, emoji, message_id, channel_id, user_id):
        guild = self.bot.get_channel(channel_id).guild
        member = guild.get_member(user_id)
        if message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.reaction_manager[emoji.name])
        if role not in member.roles:
            return

        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
