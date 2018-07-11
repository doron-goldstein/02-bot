from datetime import datetime, timedelta

import discord
import pytz
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
from googletrans import Translator


class FranXX:
    def __init__(self, bot):
        self.bot = bot
        self.trans = Translator()
        self.greet_channel = bot.get_channel(391483720244264961)
        self.greet_log = bot.get_channel(392444419535667200)
        self.welcome_emoji = discord.utils.get(bot.emojis, name="welcome")

    def get_next_weekday(self, startdate: datetime, day: str) -> datetime:
        """Get the next date per day of the week"""

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

    def get_remaining(self, day: str, *, hour: int, minute: int) -> timedelta:
        """Returns the time between now and and the next `day` at `hour`:`minute`"""

        time_now = datetime.now(pytz.timezone("Japan")).replace(tzinfo=None)
        air_date = self.get_next_weekday(time_now, day)
        show_airs = air_date.replace(hour=hour, minute=minute)

        remaining = show_airs - time_now
        return remaining

    def get_formatted_time(self, day: str, *, hour: int, minute: int, delta=0) -> str:
        """Format time until `day` at `hour`:`minute`"""

        remaining = self.get_remaining(day, hour=hour, minute=minute) + timedelta(hours=delta)

        days = remaining.days
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        fmt = f' Days, {hours} Hours, and {minutes} Minutes.'
        if days < 0:
            time = '6' + fmt
        elif days >= 7:
            time = '0' + fmt
        else:
            time = str(days) + fmt
        return time

    @cooldown(1, 120, BucketType.channel)
    @commands.command(aliases=["episode", "nextepisode", "airtime"])
    async def next(self, ctx):
        """Countdown to next episode of the anime."""

        air_time = self.get_formatted_time("Saturday", hour=23, minute=30)
        crunchy = self.get_formatted_time("Saturday", hour=23, minute=30, delta=1.5)

        embed = discord.Embed(title="Darling in the FranXX", color=0x0066CC)
        embed.set_footer(text='Hype Up Bois')

        if not int(air_time[0]) > 1:
            embed.add_field(name="Air Time", value=air_time, inline=False)
        if not int(crunchy[0]) > 1:
            embed.add_field(name="Crunchyroll Release", value=crunchy)
        if len(embed.fields) == 0:
            embed.description = "The show is over!"
            embed.set_footer(text=':(')
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

    async def on_member_join(self, member):
        if member.guild != self.greet_channel.guild:
            return

        state = self.bot.muted_members.get(member.id)
        if state:
            if state.get('muted'):
                r_id = self.bot.muted_roles.get(member.guild.id)
                await member.add_roles(discord.utils.get(member.guild.roles, id=r_id))

        if self.bot.config[member.guild.id]['do_welcome']:
            m = await self.greet_channel.send(f"Welcome {member.mention}, my Darling! "
                                              "Only those who read <#434836251766423564> can ride Strelizia with me.\n"
                                              "Proceed there to collect your roles as well!")
            try:
                await m.add_reaction(self.welcome_emoji)
            except:  # noqa
                pass
        await self.greet_log.send(f"\N{WHITE HEAVY CHECK MARK} {member.mention} has joined the server.")

    async def on_member_remove(self, member):
        if member.guild != self.greet_channel.guild:
            return

        if self.bot.config[member.guild.id]['do_welcome']:
            await self.greet_channel.send(f"Farewell, my Darling! `{member}` has left the server!")
        await self.greet_log.send(f"\N{CROSS MARK} {member.mention} ({member} / {member.id}) has left the server.")


def setup(bot):
    bot.add_cog(FranXX(bot))
