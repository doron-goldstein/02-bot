from discord.ext import commands


class Spook:
    def __init__(self, bot):
        self.bot = bot
        roles = {"black": 497116920173035530, "orange": 497116718037204992}
        guild = bot.get_guild(391483719803994113)
        self.black = guild.get_role(roles['black'])
        self.orange = guild.get_role(roles['orange'])

    @commands.command()
    async def orange(self, ctx):
        """Join the Orange team!"""
        if self.black in ctx.author.roles:
            return await ctx.send("You can't join both teams, Darling!")
        await ctx.author.add_roles(self.orange)

    @commands.command()
    async def black(self, ctx):
        """Join the Black team!"""
        if self.orange in ctx.author.roles:
            return await ctx.send("You can't join both teams, Darling!")
        await ctx.author.add_roles(self.black)

    @commands.command()
    async def unspook(self, ctx):
        """Leave the spooky team you're in"""
        await ctx.author.remove_roles(self.orange, self.black)


def setup(bot):
    bot.add_cog(Spook(bot))
