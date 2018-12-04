from discord.ext import commands


class Santa:
    def __init__(self, bot):
        self.bot = bot
        roles = {"red": 519411441711710208, "green": 519411575971512330}
        guild = bot.get_guild(391483719803994113)
        self.red = guild.get_role(roles['red'])
        self.green = guild.get_role(roles['green'])

    @commands.command(name="peepo")
    async def peepo_(self, ctx):
        """Join the Peepo Green team!"""
        if self.red in ctx.author.roles:
            return await ctx.send("You can't join both teams, Darling!")
        await ctx.author.add_roles(self.green)
        await ctx.send("You've joined the Peepo Green team!")

    @commands.command(name="commie")
    async def commie_(self, ctx):
        """Join the Commie Red team!"""
        if self.green in ctx.author.roles:
            return await ctx.send("You can't join both teams, Darling!")
        await ctx.author.add_roles(self.red)
        await ctx.send("You've joined the Commie Red team!")

    @commands.command()
    async def unjolly(self, ctx):
        """Leave the jolly team you're in"""
        await ctx.author.remove_roles(self.green, self.red)
        await ctx.send("You've left the jolly team!")


def setup(bot):
    bot.add_cog(Santa(bot))
