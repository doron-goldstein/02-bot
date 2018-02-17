from datetime import datetime, timedelta

import discord
import pytz
from discord.ext import commands
from googletrans import Translator


class FranXX:
    def __init__(self, bot):
        self.bot = bot
        self.trans = Translator()

    async def get_next_weekday(self, startdate, day):
        days = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }
        weekday = days[day]
        d = datetime.strptime(startdate, '%Y-%m-%d')
        t = timedelta((7 + weekday - d.weekday()) % 7)
        return (d + t).strftime('%Y-%m-%d')

    async def get_remaining_time(self):
        day = "Saturday"
        hour = "23:30"
        jp_time = datetime.now(pytz.timezone("Japan"))
        air_date = await self.get_next_weekday(jp_time.strftime('%Y-%m-%d'), day)
        time_now = jp_time.replace(tzinfo=None)
        show_airs = datetime.strptime(f'{air_date} - {hour.strip()}', '%Y-%m-%d - %H:%M')
        remaining = show_airs - time_now
        if remaining.days < 0:
            return f'{6} Days {remaining.seconds // 3600} Hours and {(remaining.seconds // 60)%60} Minutes.'
        else:
            return (f'{remaining.days} Days '
                    f'{remaining.seconds // 3600} Hours '
                    f'and {(remaining.seconds // 60)%60} Minutes.')

    @commands.command(aliases=["episode", "nextepisode", "airtime"])
    async def next(self, ctx):
        """Countdown to next episode of the anime."""
        remaining = await self.get_remaining_time()
        embed = discord.Embed(title="Darling in the FranXX", color=0x0066CC)
        embed.add_field(name="Next Episode", value=remaining)
        embed.set_footer(text='Hype Up Bois')
        embed.set_thumbnail(url="https://myanimelist.cdn-dena.com/images/anime/1614/90408.jpg")
        await ctx.send(embed=embed)

    async def translate(self, txt):
        res = await self.bot.loop.run_in_executor(None, self.trans.translate, txt, 'en', 'ja')
        return res.text

    async def on_message_edit(self, old, new):
        if new.channel.id == 392840122158022656:
            embed = new.embeds[0]
            embed.description = await self.translate(embed.description)
            await new.channel.send("Translated:", embed=embed)


def setup(bot):
    bot.add_cog(FranXX(bot))
