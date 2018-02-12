from datetime import datetime, timedelta

import discord
import pytz
from discord.ext import commands


class FranXX:
    def __init__(self, bot):
        self.bot = bot

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
        print(jp_time)
        air_date = await self.get_next_weekday(jp_time.strftime('%Y-%m-%d'), day)
        print(air_date)
        time_now = jp_time.replace(tzinfo=None)
        show_airs = datetime.strptime(f'{air_date} - {hour.strip()}', '%Y-%m-%d - %H:%M')
        print(show_airs)
        remaining = show_airs - time_now
        if remaining.days < 0:
            return f'{6} Days {remaining.seconds // 3600} Hours and {(remaining.seconds // 60)%60} Minutes.'
        else:
            return (f'{remaining.days} Days '
                    f'{remaining.seconds // 3600} Hours '
                    f'and {(remaining.seconds // 60)%60} Minutes.')

    @commands.command(aliases=["episode", "nextepisode", "airtime"], hidden=True)
    async def next(self, ctx):
        """Countdown to next episode of an airing anime."""
        remaining = await self.get_remaining_time()
        embed = discord.Embed(title="Darling in the FranXX", color=0x0066CC)
        embed.add_field(name="Next Episode", value=remaining)
        embed.set_footer(text='Hype Up Bois')
        embed.set_thumbnail(url="https://myanimelist.cdn-dena.com/images/anime/1614/90408.jpg")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FranXX(bot))
