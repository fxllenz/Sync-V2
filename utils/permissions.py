import nextcord
from functools import wraps

def permissions(name):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx, *args, **kwargs):
            permission_mapping = {
                "ban": "ban_members",
                "kick": "kick_members",
                "manage_channels": "manage_channels",
                "manage_roles": "manage_roles",
                "administrator": "administrator",
                "manage_guild": "manage_guild",
                "manage_messages": "manage_messages",
            }

            if name not in permission_mapping:
                await ctx.send(f"Invalid permission name: {name}", ephemeral=True)
                return

            required_perm = permission_mapping[name]
            

            user_perms = ctx.user.guild_permissions
            if not getattr(user_perms, required_perm, False):
                embed = nextcord.Embed(
                    title="Missing Permission",
                    description=f"> **You Are Missing The ``{required_perm}`` Permission**",
                    color=nextcord.Color.red()
                )
                await ctx.send(embed=embed)
                return


            bot_perms = ctx.guild.me.guild_permissions
            if not getattr(bot_perms, required_perm, False):
                embed = nextcord.Embed(
                    title="Missing Bot Permission",
                    description=f"> **I Am Missing The ``{required_perm}`` Permission**",
                    color=nextcord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            return await func(self, ctx, *args, **kwargs)

        return wrapper
    return decorator
