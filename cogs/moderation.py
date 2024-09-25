import nextcord
from nextcord.ext import commands
import colorama
from colorama import Fore, Style
colorama.init()
import requests
import json
import time
from nextcord.ui import Button, View
from nextcord import Embed

from utils.permissions import permissions

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ban", description="Bans A Member From The Server")
    @permissions(name="ban")
    async def ban(self, ctx: nextcord.Interaction, member: nextcord.Member, reason: str = None):
        if member == ctx.user:
            embed = nextcord.Embed(title="Ban Error", description="> **You Cannot Ban Yourself**", color=nextcord.Color.red())
            return await ctx.send(embed=embed)
        if ctx.user.top_role  < member.top_role:
            embed = nextcord.Embed(title="Ban Error", description="> **You Don't Have Permission To Ban This Member**", color=nextcord.Color.red())
            return await ctx.send(embed=embed)
        try:
            await member.ban(reason=reason)
            embed = nextcord.Embed(title="User  Banned", description=f"> **Moderator:** {ctx.user.mention}\n> **Reason:** {reason}\n> **Member:** {member.mention}", color=nextcord.Color.from_rgb(255,255,255))
        except Exception as e:
            embed = nextcord.Embed(title="Ban Error", description="> **An Error Occurred While Banning The User**", color=nextcord.Color.red())

    @nextcord.slash_command(name="unban", description="Unbans A Member From The Server")
    @permissions(name="ban")
    async def unban(self, ctx: nextcord.Interaction, user_id, reason: str = None):
        if user_id == ctx.user.id:
            embed = nextcord.Embed(title="Unban Error", description="> **You Cannot Unban Yourself**", color=nextcord.Color.red())
            return await ctx.send(embed=embed)
        try:
            await ctx.guild.unban(reason=reason)
            embed = nextcord.Embed(title="User  Unbanned", description=f"> **Moderator:** {ctx.user.mention}\n> **Reason:** {reason}\n> **User ID:** {user_id}", color=nextcord.Color.from_rgb(255,255,255))
        except Exception as e:
            embed = nextcord.Embed(title="Ban Error", description="> **An Error Occurred While Unbanning This User**", color=nextcord.Color.red())





def setup(bot):
    bot.add_cog(Moderation(bot))