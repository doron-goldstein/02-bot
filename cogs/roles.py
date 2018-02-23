import asyncio

import discord
from discord.ext import commands
from utils.checks import restricted


class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.text_role = 407759891927924737
        self.pics_role = 402315991918575636
        self.nsfw_msg = """
            Hi! Before you accept the NSFW role(s) that grant you access to the hidden NSFW-content channels, you must agree to the following terms:
\* That you, the user, claim to be 18 years of age or older,
\* You understand that the role(s) being requested grant access to previously hidden NSFW-content channel(s),
\* The moderators reserve the right to withdraw the role(s) without prior notice nor explanation at any point in time,
\* You have read and agreed to Discord Terms of Service (<https://discordapp.com/terms>) and will abide by them as a member of the /r/DarliFranXX community.

Please copy and paste the following message to consent:
`I, $user, have read the Terms & Conditions of the /r/DarliFranXX server and agree to them.`
Where $user is your name.
        """  # noqa

    @commands.guild_only()
    @commands.command()
    @restricted()
    async def lewdme(self, ctx, role_type):
        """Join NSFW channel roles"""
        if role_type not in ("pics", "images", "text"):
            return await ctx.send("Role must be either `pics` or `text`.")
        if role_type == "images":
            role_type == "pics"
        role = discord.utils.get(ctx.guild.roles, id=getattr(self, role_type + "_role"))
        if role in ctx.author.roles:
            return await ctx.send("You have this role already.")
        try:
            await ctx.author.send(self.nsfw_msg)
        except:  # noqa
            return await ctx.send(ctx.author.mention + " I couldn't send you a DM, do you have them disabled perhaps?")

        def check(m):
            return isinstance(m.channel, discord.DMChannel) and m.channel.recipient == ctx.author and not m.author.bot

        while True:
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.author.send("Command timed out.")
            if msg.content.strip('`') == "I, $user, have read the Terms & Conditions of the /r/DarliFranXX server and agree to them.":  # noqa
                await ctx.author.send("Please substitute your name (example: Zero Two) instead of `$user`.\n"
                                      "Try again.")
                continue
            elif msg.content.strip('`') == "I, {}, have read the Terms & Conditions of the /r/DarliFranXX server and agree to them.".format(ctx.author.name):  # noqa
                await ctx.author.add_roles(role)
                await ctx.author.send(f"The role `{role.name}` has been added!")
                break
            else:
                await ctx.author.send("Please try again with the proper format.")
                continue
        await ctx.message.delete()

    @commands.command(aliases=["unlewd"])
    @restricted()
    async def purify(self, ctx):
        """Leave all NSFW roles"""
        roles = [discord.utils.get(ctx.guild.roles, id=r_id) for r_id in (self.text_role, self.pics_role)]
        if any(r in ctx.author.roles for r in roles):
            await ctx.author.remove_roles(*roles)
            return await ctx.message.add_reaction("\N{OK HAND SIGN}")
        await ctx.send(f"You don't have any lewd roles! Use `{ctx.prefix}lewdme <role_type>` if you want to join them.")


def setup(bot):
    bot.add_cog(Roles(bot))
