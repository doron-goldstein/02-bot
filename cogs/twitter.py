from bs4 import BeautifulSoup
from discord.ext import commands


class Twitter:
    def __init__(self, bot):
        self.bot = bot

    async def translate(self, text, target="en", source="jp"):
        params = {"sl": source, "hl": target, "q": text}
        async with self.bot.session.get("http://translate.google.com/m", params=params) as res:
            print(res.url)
            to_parse = await res.text()
            print(to_parse)
        soup = BeautifulSoup(to_parse)
        #
        return soup.find("div", {'class': 't0'}).text

    @commands.command(hidden=True, name="translate")
    async def trans(self, ctx, txt):
        await ctx.send(await self.translate(txt))


def setup(bot):
    bot.add_cog(Twitter(bot))
