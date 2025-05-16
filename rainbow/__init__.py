from .rainbow import rainbow

async def setup(bot):
    await bot.add_cog(rainbow())
