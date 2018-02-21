import random

import discord
from discord.ext import commands
from discord.ext.commands import command


BASE_URL = "https://api.weeb.sh/images"
RANDOM_URL = BASE_URL + "/random"


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

    async def make_embed(self, title, type_):
        resp = await self.bot.session.get(RANDOM_URL, params={'type': type_},
                                          headers={'Authorization': self.bot.img_auth})
        data = await resp.json()
        url = data['url']

        return discord.Embed(title=title) \
                      .set_image(url=url) \
                      .set_footer(text="Powered by weeb.sh")

    @command()
    async def ship(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Could these two be a good couple? What are the chances?"""

        if user1 is None:
            user1 = ctx.author
            user2 = random.choice(ctx.guild.members)  # can disallow bots but it might be funny this way
        elif user2 is None:
            user2 = user1
            user1 = ctx.author

        random.seed(user1.id + user2.id)
        chance = random.randint(0, 100)
        comment = self.ship_comments[round(chance, -1)]
        await ctx.send(f"Ship chance for `{user1.name}` and `{user2.name}`: {chance}%!\n{comment}")

    @ship.error
    async def rand_error(self, ctx, err):
        if isinstance(err, commands.BadArgument):
            return await ctx.send("I can't recognize who that is! Did you misspell their name, Darling?")

    @command()
    async def sync(self, ctx, thing1, thing2=None):
        """What is the sync % between these two??"""

        if thing2 is None:
            thing2 = thing1
            thing1 = ctx.author.name

        random.seed(len(thing1) + len(thing2))
        chance = random.randint(0, 100)
        await ctx.send(f"**{thing1}** and **{thing2}** have a sync rate of {chance}%!")

    @command()
    async def pat(self, ctx, user: discord.Member = None):
        """Pat someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} patted... Themselves? For some reason.")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} patted.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} patted {user.name}!", 'pat')
        await ctx.send(embed=embed)

    @command()
    async def kiss(self, ctx, user: discord.Member = None):
        """Kiss someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} kissed... Themselves? How does that even work??")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} kissed.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} kissed {user.name}!", 'kiss')
        await ctx.send(embed=embed)

    @command()
    async def hug(self, ctx, user: discord.Member = None):
        """Hug someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} hugged... Themselves? I guess.")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} hugged.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} gave {user.name} a hug!", 'hug')
        await ctx.send(embed=embed)

    @command()
    async def lick(self, ctx, user: discord.Member = None):
        """Lick someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} licked... Themselves? What?")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} licked.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} Licked {user.name}!", 'lick')
        await ctx.send(embed=embed)

    @command()
    async def cuddle(self, ctx, user: discord.Member = None):
        """cuddle someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} is cuddling all alone...")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} cuddled.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} cuddled {user.name}!", 'cuddle')
        await ctx.send(embed=embed)

    @command()
    async def saturday(self, ctx):
        """Saturday?"""

        await ctx.send("https://www.youtube.com/watch?v=hKqwULUwHFc")


def setup(bot):
    bot.add_cog(Fun(bot))
