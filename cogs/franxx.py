import discord
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
        self.snap_role = self.greet_channel.guild.get_role(437013174533881867)

    @cooldown(1, 120, BucketType.channel)
    @commands.command(aliases=["episode", "nextepisode", "airtime"])
    async def next(self, ctx):
        """Countdown to next episode of the anime."""
        embed = discord.Embed(title="Darling in the FranXX", color=0x0066CC)
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
                await member.add_roles(member.guild.get_role(r_id))

        if member.id in self.bot.snapped_members:
            await member.add_roles(self.snap_role)

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

        if self.snap_role in member.roles:
            query = """
                INSERT INTO snap_states (member_id) VALUES ($1)
            """
            await self.bot.pool.execute(query, member.id)
            self.bot.snapped_members.append(member.id)
        else:
            query = """
                DELETE FROM snap_states WHERE member_id = $1
            """
            await self.bot.pool.execute(query, member.id)
            try:
                self.bot.snapped_members.remove(member.id)
            except ValueError:
                pass

        if self.bot.config[member.guild.id]['do_welcome']:
            await self.greet_channel.send(f"Farewell, my Darling! `{member}` has left the server!")
        await self.greet_log.send(f"\N{CROSS MARK} {member.mention} ({member} / {member.id}) has left the server.")


def setup(bot):
    bot.add_cog(FranXX(bot))
