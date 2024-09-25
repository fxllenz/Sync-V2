import nextcord
from nextcord.ext import commands
import os
import json
import colorama
from colorama import Fore, Style
colorama.init()
from utils.cogs import load_cogs
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(intents=nextcord.Intents.default())

@bot.event
async def on_ready():
    print(f'{Fore.BLUE}[NEXTCORD]{Fore.MAGENTA} [EVENT]{Fore.GREEN} Bot Is Online')
    print(f'{Fore.BLUE}[NEXTCORD]{Fore.MAGENTA} [EVENT]{Fore.GREEN} Synced Slash Commands')
    await bot.sync_all_application_commands()

load_cogs(bot)
bot.run(os.getenv("TOKEN"))