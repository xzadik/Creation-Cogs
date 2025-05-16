import asyncio
import discord
from redbot.core import commands

class rainbow(commands.Cog):
    @commands.command()
    async def rainbowset(self, ctx, delay: int, role: str):
        user = ctx.author
        rrole = discord.utils.get(user.guild.roles, name=role)
        
        if not rrole:
            await ctx.send(f"Role '{role}' not found.")
            return

        await ctx.send(f"Starting rainbow on role: {rrole.name} with {delay}s delay.")

        clist = [
            0xff0000, 0xff2f00, 0xff5900, 0xff7700, 0xff9d00, 0xffbf00, 0xffdd00, 0xfff200,
            0xf2ff00, 0xc8ff00, 0xb7ff00, 0x99ff00, 0x6aff00, 0x3cff00, 0x00ff11, 0x00ff37,
            0x00ff55, 0x00ff77, 0x00ff95, 0x00ffb7, 0x00ffdd, 0x00fffb, 0x00e1ff, 0x00bfff,
            0x009dff, 0x0080ff, 0x0062ff, 0x0048ff, 0x002fff, 0x1100ff, 0x4400ff, 0x5900ff,
            0x7700ff, 0x9900ff, 0xaa00ff, 0xcc00ff, 0xee00ff, 0xff00ee, 0xff00d0, 0xff00ae,
            0xff0088, 0xff005d, 0xff0037, 0xff0019
        ]

        while True:
            for c in clist:
                try:
                    await rrole.edit(colour=discord.Colour(value=c))
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"Failed to edit role color: {e}")
                    return
