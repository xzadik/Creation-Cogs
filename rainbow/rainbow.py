import asyncio
import discord
from discord.ext import tasks
from redbot.core import commands

class rainbow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_loops = {}

    @commands.command()
    async def rainbowset(self, ctx, delay: int, *, role_name: str):
        """Start rainbow effect on a role."""
        guild = ctx.guild
        role = discord.utils.find(lambda r: role_name.lower() in r.name.lower(), guild.roles)

        if not role:
            await ctx.send(f"❌ Role `{role_name}` not found.")
            return

        if role.id in self.active_loops:
            await ctx.send("⚠️ Rainbow already running on this role.")
            return

        if delay < 5:
            await ctx.send("⛔ Delay too low — must be 5s or more.")
            return

        loop = RainbowLoop(self.bot, role, delay)
        loop.start()
        self.active_loops[role.id] = loop
        await ctx.send(f"🌈 Rainbow started on `{role.name}` with {delay}s delay.")

    @commands.command()
    async def rainbowstop(self, ctx, *, role_name: str):
        """Stop rainbow effect on a role."""
        role = discord.utils.find(lambda r: role_name.lower() in r.name.lower(), ctx.guild.roles)

        if not role or role.id not in self.active_loops:
            await ctx.send("❌ Rainbow not running on that role.")
            return

        self.active_loops[role.id].cancel()
        del self.active_loops[role.id]
        await ctx.send(f"🛑 Rainbow stopped on `{role.name}`.")


class RainbowLoop:
    def __init__(self, bot, role, delay):
        self.bot = bot
        self.role = role
        self.delay = delay
        self.index = 0
        self.clist = [
            0xff0000, 0xff2f00, 0xff5900, 0xff7700, 0xff9d00, 0xffbf00, 0xffdd00, 0xfff200,
            0xf2ff00, 0xc8ff00, 0xb7ff00, 0x99ff00, 0x6aff00, 0x3cff00, 0x00ff11, 0x00ff37,
            0x00ff55, 0x00ff77, 0x00ff95, 0x00ffb7, 0x00ffdd, 0x00fffb, 0x00e1ff, 0x00bfff,
            0x009dff, 0x0080ff, 0x0062ff, 0x0048ff, 0x002fff, 0x1100ff, 0x4400ff, 0x5900ff,
            0x7700ff, 0x9900ff, 0xaa00ff, 0xcc00ff, 0xee00ff, 0xff00ee, 0xff00d0, 0xff00ae,
            0xff0088, 0xff005d, 0xff0037, 0xff0019
        ]
        self._task = None
        self._running = False

    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._run())

    def cancel(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()

    async def _run(self):
        while self._running:
            try:
                color = discord.Colour(value=self.clist[self.index])
                await self.role.edit(colour=color)
                self.index = (self.index + 1) % len(self.clist)
                await asyncio.sleep(self.delay)
            except discord.HTTPException as e:
                print(f"[RAINBOW] Error: {e}")
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                break
