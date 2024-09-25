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

    # Credits To .puzzy. For This Command
    @nextcord.slash_command(
        name="rainbow-text", description="Make Text Rainbow In Discord!"
    )
    async def rainbowText(self, interaction: nextcord.Interaction, text: str):
        rainbowStr = ""

        def randomColor():
            list = ["30", "31", "32", "33", "34", "35", "36", "37"]
            randomC = random.choice(list)
            return randomC

        for char in text:
            char = f"[0;{randomColor()}m{char}[0;0m"
            rainbowStr += char
        if len(rainbowStr) > 4000:
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    color=nextcord.Color.from_rgb(255, 255, 255),
                    title=f"Rainbow Text Error",
                    description="> **Text Must Not Exceed 4000 Characters**",
                )
            )
        else:
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    color=nextcord.Color.from_rgb(255, 255, 255),
                    title=f"Rainbow Text",
                    description=f"```ansi\n{rainbowStr}```",
                )
            )    



def setup(bot):
    bot.add_cog(Fun(bot))