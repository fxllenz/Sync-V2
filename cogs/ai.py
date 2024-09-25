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

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ask-ai", description="Ask the AI a question")
    async def ask_ai(self, ctx, prompt: str):
        print(f'{Fore.BLUE}[COGS]{Fore.MAGENTA} [COMMAND]{Fore.GREEN} /ask-ai | {ctx.user}')
        await ctx.response.defer()
        api_key = os.getenv('API_KEY')
        url = os.getenv('TEXT_URL')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-nemo",
            "messages": [{"role": "user", "content": prompt}]
        }
        json_data = json.dumps(data)
        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, data=json_data)
            response.raise_for_status()
            end_time = time.time()
            total_time = end_time - start_time
            ai_response = response.json()['choices'][0]['message']['content']
            total_tokens = response.json()['usage']['total_tokens']
            pages = [ai_response[i:i + 2000] for i in range(0, len(ai_response), 2000)]
            current_page = 0
            view = self.PaginatedView(pages, current_page, prompt, ctx.user.id, total_time, total_tokens, self.create_embed)
            embed = self.create_embed(pages[current_page], current_page + 1, len(pages), total_time, total_tokens)
            await ctx.send(embed=embed, view=view)
        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")

    def create_embed(self, content, current_page, total_pages, total_time, total_tokens):
        embed = Embed(
            title="Sync AI - Text Generation",
            description=content[:4096],
            color=nextcord.Color(16777215)
        )
        embed.set_footer(text=f"Page {current_page}/{total_pages} | Model: Mistral Nemo | Time Taken: {total_time:.2f}s | Tokens: {total_tokens}")
        return embed

    class PaginatedView(View):
        def __init__(self, pages, current_page, prompt, user_id, total_time, total_tokens, create_embed):
            super().__init__(timeout=None)
            self.pages = pages
            self.current_page = current_page
            self.prompt = prompt
            self.user_id = user_id
            self.total_time = total_time
            self.total_tokens = total_tokens
            self.create_embed = create_embed
            self.left_button.disabled = current_page == 0
            self.right_button.disabled = current_page == len(pages) - 1

        @nextcord.ui.button(label="⬅️", style=nextcord.ButtonStyle.primary)
        async def left_button(self, button: Button, interaction: nextcord.Interaction):
            if interaction.user.id != self.user_id:
                return await interaction.response.send_message("You cannot use this button.", ephemeral=True)

            self.current_page -= 1
            self.left_button.disabled = self.current_page == 0
            self.right_button.disabled = False

            embed = self.create_embed(self.pages[self.current_page], self.current_page + 1, len(self.pages), self.total_time, self.total_tokens)
            await interaction.response.edit_message(embed=embed, view=self)
            
        @nextcord.ui.button(label="➡️", style=nextcord.ButtonStyle.primary)
        async def right_button(self, button: Button, interaction: nextcord.Interaction):
            if interaction.user.id != self.user_id:
                return await interaction.response.send_message("You cannot use this button.", ephemeral=True)

            self.current_page += 1
            self.right_button.disabled = self.current_page == len(self.pages) - 1
            self.left_button.disabled = False

            embed = self.create_embed(self.pages[self.current_page], self.current_page + 1, len(self.pages), self.total_time, self.total_tokens)
            await interaction.response.edit_message(embed=embed, view=self)
            
        @nextcord.ui.button(label="Prompt", style=nextcord.ButtonStyle.primary)
        async def prompt_bttn(self, button: Button, interaction: nextcord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            else:
                await interaction.response.send_message(f"> **System Prompt:** ```{self.prompt}```", ephemeral=True)
                    
        @nextcord.ui.button(label=None, style=nextcord.ButtonStyle.danger, emoji="<:deleted:1288101758240821270>")
        async def delete_button(self, button: Button, interaction: nextcord.Interaction):
            if interaction.user.id != self.user_id:
                return await interaction.response.send_message("You cannot use this button.", ephemeral=True)

            await interaction.message.delete()






    @nextcord.slash_command(
        name="imagine",
        description="Create Some Images Using AI"
    )
    async def imagine(self, ctx, prompt: str = None):
        print(f'{Fore.BLUE}[COGS]{Fore.MAGENTA} [COMMAND]{Fore.GREEN} /imagine | {ctx.user}')
        if prompt is None:
            embed = nextcord.Embed(
                title="Sync AI Error", 
                description="**Please Provide A Prompt, To Generate An Image!**", 
                color=nextcord.Color.red()
            )
            return await ctx.send(embed=embed)

        await ctx.response.defer()

        api_key = os.getenv('SAPI_KEY')
        url = os.getenv('IMG_URL')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "model": "sdxl"
        }

        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            end_time = time.time()
            total_time = end_time - start_time            
            image_url = response.json()['data'][0]['url']

            embed = nextcord.Embed(
                title="Sync AI - Image Generation",
                description=f"**Prompt:** {prompt}\n**Time Taken:** {total_time:.2f}s",
                color=nextcord.Color(16777215)
            )
            embed.set_image(url=image_url)

            view = ImageDeleteView(ctx.user.id)
            await ctx.send(embed=embed, view=view)

        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred: {str(e)}")


class ImageDeleteView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @nextcord.ui.button(label=None, style=nextcord.ButtonStyle.danger, emoji="<:deleted:1288101758240821270>")
    async def delete_button(self, button: Button, interaction: nextcord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("You cannot use this button.", ephemeral=True)

        await interaction.message.delete()
        
    
def setup(bot):
    bot.add_cog(AI(bot))
    