import discord


class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.msg_id = 417823406617001987
        self.role_dict = {
            'SeXX': 407759891927924737,
            '02bounce': 402315991918575636,
            'strelizia': 392894112036159499,
            'argentea': 392894507424940034,
            'delphinium': 392894559853477899,
            'genista': 392894894999601153,
            'chlorophytum': 392894974234198026,
            'cah': 406564673345814542,
            'ThotPatrol': 405107014356697099,
            'BlueOni': 412069721832292372,
            '🎤': 416893959814512641,
            'klaxo': 403740756105363457,
            'terraria': 424639819852021763
        }

    async def on_raw_reaction_add(self, emoji, message_id, channel_id, user_id):
        guild = self.bot.get_channel(channel_id).guild
        member = guild.get_member(user_id)
        if message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.role_dict[emoji.name])
        if role in member.roles:
            return

        await member.add_roles(role)

    async def on_raw_reaction_remove(self, emoji, message_id, channel_id, user_id):
        guild = self.bot.get_channel(channel_id).guild
        member = guild.get_member(user_id)
        if message_id != self.msg_id:
            return

        role = discord.utils.get(guild.roles, id=self.role_dict[emoji.name])
        if role not in member.roles:
            return

        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
