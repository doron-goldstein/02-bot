import random

import discord
from discord.ext.commands import command


class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.ship_comments = {
            0: "These two?? Together?! Don't make me laugh, Darling...",
            10: "Not gonna happen...",
            20: "I really doubt its gonna work out between these two.",
            30: "Give up, this is doomed from the start.",
            40: "It's slim, but you have a chance.",
            50: "Might work, might not. Who knows? Sure as hell not me.",
            60: "You have a real chance here! Give it your all!",
            70: "Oh, I'm on-board all right!",
            80: "Its a match made in heaven! Now kiss~",
            90: "How come you're not all over eachother already!? You're a perfect couple!",
            100: "This is how the gods meet their partners. It'd be a shame for mankind if you two don't get together."
        }

    @command()
    async def ship(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Could these two be a good couple? What are the chances?"""

        if user1 is None:
            user1 = ctx.author
            user2 = random.choice(ctx.guild.members)  # can disallow bots but it might be funny this way
        elif user2 is None:
            user2 = user1
            user1 = ctx.author

        random.seed(str(user1.id) + str(user2.id))
        chance = random.randint(0, 100)
        comment = self.ship_comments[round(chance, -1)]
        await ctx.send(f"Ship chance for `{user1.name}` and `{user2.name}`: {chance}%!\n{comment}")

    @command()
    async def sync(self, ctx, thing1, thing2=None):
        """What is the sync % between these two??"""

        if thing2 is None:
            thing2 = thing1
            thing1 = ctx.author.name

        random.seed(str(len(thing1)) + str(len(thing2)))
        chance = random.randint(0, 100)
        await ctx.send(f"**{thing1}** and **{thing2}** have a sync rate of {chance}%!")

    @command()
    async def pat(self, ctx, user: discord.Member = None):
        """Pat someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} patted... Themselves? For some reason.")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} patted.... No one!")
        await ctx.send(f"{ctx.author.name} patted {user.name}!")

    @command()
    async def kiss(self, ctx, user: discord.Member = None):
        """Kiss someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} kissed... Themselves? How does that even work??")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} kissed.... No one!")
        await ctx.send(f"{ctx.author.name} kissed {user.name}!")

    @command()
    async def hug(self, ctx, user: discord.Member = None):
        """Hug someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} hugged... Themselves? I guess.")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} hugged.... No one!")
        await ctx.send(f"{ctx.author.name} gave {user.name} a hug!")

    @command()
    async def lick(self, ctx, user: discord.Member = None):
        """Lick someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} licked... Themselves? What?")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} licked.... No one!")
        await ctx.send(f"{ctx.author.name} Licked {user.name}!")


def setup(bot):
    bot.add_cog(Fun(bot))
