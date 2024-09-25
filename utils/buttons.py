import nextcord
from nextcord import Interaction, Embed
from nextcord.ui import View, Button


def get_custom_emoji(emoji_name: str) -> str:
    custom_emojis = {
        "home": "<:home:1288101293763592315>", 
        "utility": "<:utility:1287985608098320407>",
        "moderation":"<:moderation:1288101755577700432>", 
        "ai": "<:ai:1287985606797824102>",
        "fun":"<:fire:1288101291993726996>"
    }
    return custom_emojis.get(emoji_name, "❓")

class HelpCategoryButton(Button):
    def __init__(self, label, description, embed, emoji):
        super().__init__(label=label, style=nextcord.ButtonStyle.blurple, emoji=emoji)
        self.embed = embed

    async def callback(self, interaction: Interaction):
        await interaction.response.edit_message(embed=self.embed)

class HelpView(View):
    def __init__(self, embeds, invoker, timeout=60):
        super().__init__(timeout=timeout)
        self.invoker = invoker

        for category, embed in embeds.items():
            emoji = get_custom_emoji(category.lower())
            self.add_item(HelpCategoryButton(label=None, description=f"View {category} commands", embed=embed, emoji=emoji))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.invoker.id:
            embed = Embed(
                title="Error",
                description="You are not allowed to interact with this command.",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

def get_help_embeds(self, ctx):
    home = Embed(title="<:home:1288101293763592315> | Sync Help - Main Page", description=f"> **Bot Latency:** ``{self.bot.latency * 1000:.2f}ms``\n> **Support Server: [Invite](https://discord.gg/sync-ai)**\n> **Shard:** ``N/A``", color=nextcord.Color.from_rgb(255,255,255))
    home.set_author(name=f"User ID: {ctx.user.id}")
    home.set_footer(text=f"Guild ID: {ctx.guild.id}")
    try:
     home.set_author(icon_url=ctx.user.avatar.url)
    except Exception as e:
     pass
    try:
     home.set_footer(icon_url=ctx.guild.icon.url)
    except Exception as e:
     pass


    ai = Embed(title="<:ai:1287985606797824102> | Sync Help - AI", description="``ask-ai`` - ``imagine``", color=nextcord.Color.from_rgb(255,255,255))
    ai.set_author(name=f"User ID: {ctx.user.id}")
    ai.set_footer(text=f"Guild ID: {ctx.guild.id}")
    try:
     ai.set_author(icon_url=ctx.user.avatar.url)
    except Exception as e:
     pass
    try:
     ai.set_footer(icon_url=ctx.guild.icon.url)
    except Exception as e:
     pass


    fun = Embed(title="<:fire:1288101291993726996> | Sync Help - Fun", description="``dice``", color=nextcord.Color.from_rgb(255,255,255))
    fun.set_author(name=f"User ID: {ctx.user.id}")
    fun.set_footer(text=f"Guild ID: {ctx.guild.id}")
    try:
     fun.set_author(icon_url=ctx.user.avatar.url)
    except Exception as e:
     pass
    try:
     fun.set_footer(icon_url=ctx.guild.icon.url)
    except Exception as e:
     pass







    moderation = Embed(title="<:moderation:1288101755577700432> | Sync Help - Moderation", description="``ban`` - ``unban``", color=nextcord.Color.from_rgb(255,255,255))
    moderation.set_author(name=f"User ID: {ctx.user.id}")
    moderation.set_footer(text=f"Guild ID: {ctx.guild.id}")
    try:
     moderation.set_author(icon_url=ctx.user.avatar.url)
    except Exception as e:
     pass
    try:
     moderation.set_footer(icon_url=ctx.guild.icon.url)
    except Exception as e:
     pass


    utility = Embed(title="<:utility:1287985608098320407> | Sync Help - Utility", description="``avatar`` - ``ping`` - ``user-info`` - ``server-info`` - ``member-count`` - ``bot-count`` - ``lock`` - ``unlock`` - ``purge`` - ``uptime`` - ``channel-count`` - ``role-count``", color=nextcord.Color.from_rgb(255,255,255))
    utility.set_author(name=f"User ID: {ctx.user.id}")
    utility.set_footer(text=f"Guild ID: {ctx.guild.id}")
    try:
     utility.set_author(icon_url=ctx.user.avatar.url)
    except Exception as e:
     pass
    try:
     utility.set_footer(icon_url=ctx.guild.icon.url)
    except Exception as e:
     pass



    category_embeds = {
        "Home": home,
        "Utility": utility,
        "Moderation": moderation,
        "AI": ai,
        "Fun": fun,
    }
    return category_embeds
