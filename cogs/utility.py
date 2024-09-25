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
from utils.buttons import HelpView, get_help_embeds
COG: True


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @nextcord.slash_command(name="ping")
    async def ping(self, ctx):
        embed = nextcord.Embed(
            title="Sync Latency",
            description=f"> **{self.bot.latency * 1000:.2f}ms**",
            color=nextcord.Color.from_rgb(0, 0, 0))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="avatar", description="Gets a user's avatar from the server")
    async def avatar(self, ctx: nextcord.Interaction, user: nextcord.Member = None):
        if user is None:
            user = ctx.user
        
        if user.avatar is None:
            e1 = nextcord.Embed(
                title="Avatar",
                description=f"{user.mention} has no avatar uploaded!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=e1)
        else:
            e2 = nextcord.Embed(
                title=f"{user.name}'s Avatar",
                color=nextcord.Color.from_rgb(255, 255, 255)
            )
            e2.set_image(url=user.avatar.url)
            await ctx.send(embed=e2)

    @nextcord.slash_command(name="member-count", description="Shows The Servers Member Count")
    async def member_count(self, ctx: nextcord.Interaction):
        embed = nextcord.Embed(title="Member Count", description=f"> **{ctx.guild.member_count}**", color=nextcord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="bot-count", description="Shows The Servers Bot Count")
    async def bot_count(self, ctx: nextcord.Interaction):
        embed = nextcord.Embed(title="Bot Count", description=f"> **{len([m for  m in ctx.guild.members if m.bot])}**", color=nextcord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="role-count",  description="Shows The Servers Role Count")
    async def role_count(self, ctx: nextcord.Interaction):
        embed = nextcord.Embed(title="Role Count", description=f"> **{len(ctx.guild.roles)}**",  color=nextcord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="channel-count",  description="Shows The Servers Channel Count")
    async def channel_count(self, ctx: nextcord.Interaction):
        embed = nextcord.Embed(title="Channel Count", description=f"> **{len(ctx.guild.channels)}**", color=nextcord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="uptime", description="Shows How Long The Bot Has Been Running")
    async def uptime(self, ctx: nextcord.Interaction):
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        embed = nextcord.Embed(title="Sync Uptime", description=f"> **Uptime: {hours}h {minutes}m {seconds}s**",  color=nextcord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="lock",  description="Locks A Channel")
    @permissions(name="manage_channels")
    async def lock(self, ctx: nextcord.Interaction, channel: nextcord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed  = nextcord.Embed(title="Channel Locked", description=f"> **{channel.mention} Has Been Locked!**",  color=nextcord.Color.from_rgb(255, 255, 255))
            await ctx.send(embed=embed)
        else:
         await channel.set_permissions(ctx.guild.default_role, send_messages=False)
         embed  = nextcord.Embed(title="Channel Locked", description=f"> **{channel.mention} Has Been Locked!**",  color=nextcord.Color.from_rgb(255, 255, 255))
         await ctx.send(embed=embed)

    @nextcord.slash_command(name="unlock",  description="Unlocks A Channel")
    @permissions(name="manage_channels")
    async def unlock(self, ctx: nextcord.Interaction, channel: nextcord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed  = nextcord.Embed(title="Channel Unlocked", description=f"> **{channel.mention} Has Been Unlocked!**",  color=nextcord.Color.from_rgb(255, 255, 255))
            await ctx.send(embed=embed)
        else:
         await channel.set_permissions(ctx.guild.default_role, send_messages=True)
         embed  = nextcord.Embed(title="Channel Unlocked", description=f"> **{channel.mention} Has Been Unlocked!**",  color=nextcord.Color.from_rgb(255, 255, 255))
         await ctx.send(embed=embed)

    @nextcord.slash_command(name="purge", description="Purges A Specified Amount Of Messages")
    @permissions(name="manage_messages")
    async def purge(self, ctx: nextcord.Interaction, amount: int = None):
        if amount is None:
            embed = nextcord.Embed(title="Purge Error", description="> **Please Specify An Amount Of Messages To Purge**",  color=nextcord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=embed)
        if  amount > 100:
            embed = nextcord.Embed(title="Purge Error", description="> **You Can Only Purge 100 Messages At A Time**",   color=nextcord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=embed)
        if amount  < 1:
            embed = nextcord.Embed(title="Purge Error", description="> **You Must Enter A Number Bigger Than 0**",   color=nextcord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=embed)
        else:
            await ctx.channel.purge(limit=amount)
            embed = nextcord.Embed(title="Purge Success", description=f"> **``{amount}`` Messages Deleted**",   color=nextcord.Color.from_rgb(255, 255, 255))
            await ctx.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name="user-info",  description="Gets Information About A User")
    async def user_info(self, ctx: nextcord.Interaction, user: nextcord.Member = None):
        if user is None:
            user = ctx.user
            embed = nextcord.Embed(title="User Info", description=f"> **Username:** {user.name}  \n> **ID:** {user.id} \n> **Created At:**  {user.created_at} \n> **Joined At:** {user.joined_at} \n> **Roles: {len(ctx.user.roles)}** ", color=nextcord.Color.from_rgb(255, 255, 255))
            embed.set_thumbnail(url=user.display_avatar)
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(title="User Info", description=f"> **Username:** {user.name}   \n> **ID:** {user.id} \n> **Created At:**   {user.created_at} \n> **Joined At:** {user.joined_at}  \n> **Roles: {len(user.roles)}** ", color=nextcord.Color.from_rgb(255, 255, 255))
            embed.set_thumbnail(url=user.display_avatar)
            await ctx.send(embed=embed)

    @nextcord.slash_command(name="server-info", description="Gets Information About The Server")
    async def server_info(self, ctx: nextcord.Interaction):
        embed = nextcord.Embed(title="Server Info", description=f"> **Server Name:** {ctx.guild.name}  \n> **Server ID:** {ctx.guild.id} \n> **Server Created At:**  {ctx.guild.created_at} \n> **Server Owner:** <@{ctx.guild.owner_id}> \n > **Server Roles:** {len(ctx.guild.roles)} \n> **Server Channels:** {len (ctx.guild.channels)} \n> **Server Members:** {ctx.guild.member_count} ", color= nextcord.Color.from_rgb(255, 255, 255))
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)


    @nextcord.slash_command(name="help", description="Shows help information")
    async def help(self, ctx: nextcord.Interaction):
        category_embeds = get_help_embeds(self, ctx)
        await ctx.response.send_message(
            embed=category_embeds["Home"],
            view=HelpView(category_embeds, invoker=ctx.user)
        )


def setup(bot):
    bot.add_cog(Utility(bot))
   