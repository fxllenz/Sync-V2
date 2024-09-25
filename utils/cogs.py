import os
import importlib
import traceback
import colorama
from colorama import Fore, Style
colorama.init()
from nextcord.ext.commands import Bot

def load_cogs(bot: Bot) -> None:
    for root, _, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                cog_path = os.path.relpath(os.path.join(root, file)).replace(os.path.sep, '.')[:-3]
                try:
                    module = importlib.import_module(cog_path)
                    if getattr(module, "COG", True):
                        bot.load_extension(cog_path)
                        print(f"{Fore.BLUE}[COGS]{Fore.MAGENTA}     [EVENT]{Fore.GREEN} {cog_path} Cog Loaded")
                except Exception:
                    traceback.print_exc()
