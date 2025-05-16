import asyncio
import discord
from discord.ext import tasks
from redbot.core import commands

class rainbow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_loops = {}  # stores active rainbow loops by role ID

    @commands.command()
    async def rainbowset(self, ctx, delay: int, *, role_name: str):
        """Start rainbow role cycling on a given role name."""
        guild = ctx.guild
        role = discord.utils.find(lambda r: role_name.lower() in r.name.lower(), guild.roles)

        if not role:
            await ctx.send(f"❌ Role `{role_name}` not found.")
            return

        if role.id in self.role_loops:
            await ctx.send("⚠️ Rainbow is already running on this role.")
            return

        if delay < 5:
            await ctx.send("⛔ Delay too low — must be 5s or higher to avoid rate limits.")
            return

        loop = self._make_loop(role, delay)
        self.role_loops[role.id] = loop
        loop.start()
        await ctx.send(f"🌈 Started rainbow effect on `{role.name}` every {delay}s.")

    @commands.command()
    async def rainbowstop(self, ctx, *, role_name: str):
        """Stop rainbow cycling on a role."""
        role = discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)

        if not role or role.id not in self.role_loops:
            await ctx.send("❌ No rainbow running on that role.")
            return

        self.role_loops[role.id].cancel()
        del self.role_loops[role.id]
        await ctx.send(f"🛑 Stopped rainbow effect on `{role.name}`.")

    def _make_loop(self, role, delay):
        clist = [
            0xff0000, 0xff2f00, 0xff5900, 0xff7700, 0xff9d00, 0xffbf00, 0xffdd00, 0xfff200,
            0xf2ff00, 0xc8ff00, 0xb7ff00, 0x99ff00, 0x6aff00, 0x3cff00, 0x00ff11, 0x00ff37,
            0x00ff55, 0x00ff77, 0x00ff95, 0x00ffb7, 0x00ffdd, 0x00fffb, 0x00e1ff, 0x00bfff,
            0x009dff, 0x0080ff, 0x0062ff, 0x0048ff, 0x002fff, 0x1100ff, 0x4400ff, 0x5900ff,
            0x7700ff, 0x9900ff, 0xaa00ff, 0xcc00ff, 0xee00ff, 0xff00ee, 0xff00d0, 0xff00ae,
            0xff0088, 0xff005d, 0xff0037, 0xff0019
        ]
        index = 0

        @tasks.loop(seconds=delay)
        async def rainbow_loop():
            nonlocal index
            try:
                color = discord.Colour(value=clist[index])
                await role.edit(colour=color)
                index = (index + 1) % len(clist)
            except discord.HTTPException as e:
                print(f"[RAINBOW] Failed to edit role color: {e}")

        return rainbow_loop
