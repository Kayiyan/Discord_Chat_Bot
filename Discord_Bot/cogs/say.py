from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["s"],
        help="This is chat command",
        description="Commands for chat and say something cool",        
        enabled=True,
        hidden=False
    )
    async def say(self, ctx, *what): 
        await ctx.send(" ".join(what))

async def setup(bot):
    await bot.add_cog(Say(bot))