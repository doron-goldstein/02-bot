import json
import random
from io import BytesIO

import discord
from discord.ext import commands
from discord.ext.commands import command, UserConverter, BadArgument

from utils.checks import restricted

BASE_URL = "https://api.weeb.sh"
IMAGES_URL = BASE_URL + "/images"
RANDOM_URL = IMAGES_URL + "/random"
GENERATE_URL = BASE_URL + "/auto-image"
SHIP_URL = GENERATE_URL + "/love-ship"


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

    async def generate_ship(self, m1, m2):
        body = json.dumps({"targetOne": m1.avatar_url, "targetTwo": m2.avatar_url})
        headers = {'Authorization': self.bot.img_auth, 'Content-Type': 'application/json'}
        resp = await self.bot.session.post(SHIP_URL, headers=headers, data=body)

        f = discord.File(BytesIO(await resp.read()), "ship.png")
        embed = discord.Embed().set_image(url="attachment://ship.png")
        return embed, f

    async def make_embed(self, title, type_):
        resp = await self.bot.session.get(RANDOM_URL, params={'type': type_},
                                          headers={'Authorization': self.bot.img_auth})
        data = await resp.json()
        url = data['url']

        return discord.Embed(title=title) \
                      .set_image(url=url) \
                      .set_footer(text="Powered by weeb.sh")

    @command()
    @restricted()
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
        embed, f = await self.generate_ship(user1, user2)
        embed.title = f"Ship chance for {user1.name} and {user2.name}"
        embed.description = f"{chance}%!\n{comment}"
        await ctx.send(embed=embed, file=f)

    @ship.error
    async def rand_error(self, ctx, err):
        if isinstance(err, commands.BadArgument):
            return await ctx.send("I can't recognize who that is! Did you misspell their name, Darling?")

    @command()
    @restricted()
    async def sync(self, ctx, thing1, thing2=None):
        """What is the sync % between these two??"""

        if thing2 is None:
            thing2 = thing1
            thing1 = ctx.author.name

        random.seed(len(thing1) + len(thing2))
        chance = random.randint(0, 100)
        await ctx.send(f"**{thing1}** and **{thing2}** have a sync rate of {chance}%!")

    @command()
    @restricted()
    async def pat(self, ctx, user: discord.Member = None):
        """Pat someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} patted... Themselves? For some reason.")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} patted.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} patted {user.name}!", 'pat')
        await ctx.send(embed=embed)

    @command()
    @restricted()
    async def kiss(self, ctx, user: discord.Member = None):
        """Kiss someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} kissed... Themselves? How does that even work??")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} kissed.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} kissed {user.name}!", 'kiss')
        await ctx.send(embed=embed)

    @command()
    @restricted()
    async def hug(self, ctx, user: discord.Member = None):
        """Hug someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} hugged... Themselves? I guess.")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} hugged.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} gave {user.name} a hug!", 'hug')
        await ctx.send(embed=embed)

    @command()
    @restricted()
    async def lick(self, ctx, user: discord.Member = None):
        """Lick someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} licked... Themselves? What?")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} licked.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} Licked {user.name}!", 'lick')
        await ctx.send(embed=embed)

    @command()
    @restricted()
    async def cuddle(self, ctx, user: discord.Member = None):
        """Cuddle someone!"""

        if user == ctx.author:
            return await ctx.send(f"{ctx.author.name} is cuddling all alone...")
        elif user is None:
            return await ctx.send(f"{ctx.author.name} cuddled.... No one!")

        embed = await self.make_embed(f"{ctx.author.name} cuddled {user.name}!", 'cuddle')
        await ctx.send(embed=embed)

    class UserCreated(UserConverter):
        async def convert(self, ctx, arg):
            try:
                u = super().convert(ctx, arg)
                return discord.utils.snowflake_time(u.id)
            except BadArgument:
                if isinstance(arg, int) or arg.isdigit():
                    return discord.utils.snowflake_time(arg)
                else:
                    raise BadArgument("Can only convert ID numbers.")

    @command(hidden=True)
    async def age(self, ctx, created: UserCreated):
        await ctx.send(created)

    @command()
    async def saturday(self, ctx):
        """Saturday?"""

        await ctx.send("https://www.youtube.com/watch?v=hKqwULUwHFc")


def setup(bot):
    bot.add_cog(Fun(bot))
