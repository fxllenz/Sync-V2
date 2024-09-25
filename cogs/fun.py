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
from dotenv import load_dotenv
load_dotenv()
import os
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="dice", description="Roll A Six Sided Die")
    async def dice(self, ctx):
        embed = nextcord.Embed(title="Dice Roll", description=f"> **You Rolled A  {random.randint(1, 6)}**", color=nextcord.Color.from_rgb(255,255,255))
        await ctx.send(embed=embed)

    



def setup(bot):
    bot.add_cog(Fun(bot))