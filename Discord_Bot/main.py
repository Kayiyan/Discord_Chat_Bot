import os
import discord
from discord.ext import commands
import logging
import settings
import asyncio
import signal
import platform
logger = settings.logging.getLogger("bot")

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix=">",intents=intents)

    async def shutdown(signal, loop):
        """Cleanup tasks tied to the service's shutdown."""
        logger.info(f"Received exit signal {signal.name}...")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

        [task.cancel() for task in tasks]

        logger.info(f"Cancelling {len(tasks)} outstanding tasks")
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Flushing metrics")
        

    @bot.event
    async def on_ready():
        logger.info("--------------------------------------------------")
        logger.info(f"Logged in as {bot.user.name} - {bot.user.id}")
        logger.info(f"Discord.py API version: {discord.__version__}")
        logger.info(f'BOT MADE BY KAYIYAN')
        logger.info("Loading extensions...")
        logger.info("Loading done!")
        logger.info("--------------------------------------------------")
        await bot.change_presence(activity=discord.Game(name="Visual Studio Code"))
       
    
        # Load cogs
        for cogs_file in settings.COGS_DIR.glob("*.py"):
            if cogs_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cogs_file.name[:-3]}")

    try:
        bot.run(settings.DISCORD_API_SECRET,root_logger=True) 
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt, shutting down...")
        asyncio.run(shutdown())       

if __name__ == '__main__':
    while True:
        try:
            run()
        except Exception as e:
            logger.error(e)
            logger.info("Restarting bot...")
            continue
        
    