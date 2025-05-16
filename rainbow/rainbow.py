from discord.ext import tasks
from redbot.core import commands
import discord
import asyncio
import colorsys

def is_owner_or_guild_owner():
    async def predicate(ctx):
        if ctx.guild is not None:
            if ctx.author.id == ctx.guild.owner_id:
                return True
        return await ctx.bot.is_owner(ctx.author)
    return commands.check(predicate)
    
class RainbowHue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_loops = {}

    @commands.command(name="rainbowset")
    @is_owner_or_guild_owner()
    async def rainbowset(self, ctx, *, role_name: str):
        """Start a hue-based rainbow gradient on a role."""
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if not role:
            await ctx.send(f"Role '{role_name}' not found.")
            return

        if guild.id in self.guild_loops:
            await ctx.send("Rainbow is already running in this server.")
            return

        loop = self._make_loop(guild, role)
        self.guild_loops[guild.id] = loop
        loop.start()
        await ctx.send(f"🌈 Started rainbow hue shift on `{role.name}`.")

    @commands.command(name="rainbowstop")
    @is_owner_or_guild_owner()
    async def rainbowset(self, ctx, *, role_name: str):
        """Stop the rainbow hue effect."""
        guild_id = ctx.guild.id
        if guild_id in self.guild_loops:
            self.guild_loops[guild_id].cancel()
            del self.guild_loops[guild_id]
            await ctx.send("🛑 Rainbow effect stopped.")
        else:
            await ctx.send("No rainbow effect running in this server.")

    def _make_loop(self, guild, role, delay=12):
        step_count = 100
        index = 0

        @tasks.loop(seconds=delay)
        async def rainbow_loop():
            nonlocal index
            try:
                hue = (index / step_count) % 1.0
                r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
                color = discord.Colour.from_rgb(int(r*255), int(g*255), int(b*255))
                await role.edit(colour=color, reason="Rainbow hue shift")
                index = (index + 1) % step_count
            except discord.HTTPException as e:
                if e.status == 429:
                    print(f"[RAINBOW] Rate limited on {guild.name}, sleeping 60s.")
                    await asyncio.sleep(60)
                else:
                    print(f"[RAINBOW] Error on {guild.name}: {e}")
                    await asyncio.sleep(15)

        return rainbow_loop
