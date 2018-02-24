from datetime import datetime, timedelta, time

import discord
import pytz
from discord.ext import commands
from googletrans import Translator


class FranXX:
    def __init__(self, bot):
        self.bot = bot
        self.trans = Translator()

    def get_next_weekday(self, startdate, day):
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
        days = timedelta((7 + weekday - startdate.weekday()) % 7)
        return startdate + days

    def get_remaining_time(self):
        day = "Saturday"
        hour, minute = "23:30".split(":")

        time_now = datetime.now(pytz.timezone("Japan")).replace(tzinfo=None)
        air_date = self.get_next_weekday(time_now, day)
        show_airs = air_date.replace(hour=int(hour), minute=int(minute))
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
        remaining = self.get_remaining_time()
        embed = discord.Embed(title="Darling in the FranXX", color=0x0066CC)
        embed.add_field(name="Next Episode", value=remaining)
        embed.set_footer(text='Hype Up Bois')
        embed.set_thumbnail(url="https://myanimelist.cdn-dena.com/images/anime/1614/90408.jpg")
        await ctx.send(embed=embed)

    async def translate(self, txt):
        res = await self.bot.loop.run_in_executor(None, self.trans.translate, txt, 'en', 'ja')
        return res.text

    async def on_message_edit(self, old, new):
        if new.author == new.guild.me:
            return
        if new.channel.id == 392840122158022656:
            embed = new.embeds[0]
            embed.description = await self.translate(embed.description)
            await new.channel.send("Translated:", embed=embed)


def setup(bot):
    bot.add_cog(FranXX(bot))
