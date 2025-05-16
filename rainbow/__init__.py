from .rainbow import RainbowHue

async def setup(bot):
    await bot.add_cog(RainbowHue(bot))
