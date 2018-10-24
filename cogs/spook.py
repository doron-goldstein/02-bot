import random

from discord.ext import commands


class Spook:
    def __init__(self, bot):
        self.bot = bot
        roles = {"black": 497116920173035530, "orange": 497116718037204992}
        guild = bot.get_guild(391483719803994113)
        self.black = guild.get_role(roles['black'])
        self.orange = guild.get_role(roles['orange'])

    @commands.command(name="orange")
    async def orange_(self, ctx):
        """Join the Orange team!"""
        if self.black in ctx.author.roles:
            return await ctx.send("You can't join both teams, Darling!")
        await ctx.author.add_roles(self.orange)
        await ctx.send("You've joined the Orange team!")

    @commands.command(name="black")
    async def black_(self, ctx):
        """Join the Black team!"""
        if self.orange in ctx.author.roles:
            return await ctx.send("You can't join both teams, Darling!")
        await ctx.author.add_roles(self.black)
        await ctx.send("You've joined the Black team!")

    @commands.command()
    async def unspook(self, ctx):
        """Leave the spooky team you're in"""
        await ctx.author.remove_roles(self.orange, self.black)
        await ctx.send("You've left the spooky team!")

    @commands.command()
    async def happy(self, ctx, color):
        color = color.lower()
        if color not in ["orange", "black"]:
            return await ctx.send("Darling, that's not a valid color!")
        m = random.choice(getattr(self, color).members)
        await ctx.send(f"Happy Halloween, {m.mention}!")


def setup(bot):
    bot.add_cog(Spook(bot))
