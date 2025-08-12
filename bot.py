import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv(".env")

token = os.getenv("token")


class SpoonMusic(commands.Bot):
    def __init__(self, intents, token_bot):
        super().__init__(command_prefix="!", intents=intents)
        self.token: str = token_bot

    async def on_ready(self):

        await self.change_presence(status=discord.Status.online, activity=discord.Game(name='/youtube play'))

        await bot.tree.sync()

    # Synchronisation avec les cogs
    async def setup_hook(self):
        for extension in os.listdir("./cogs"):
            if extension.endswith(".py") and not extension.startswith("__"):
                await self.load_extension(f'cogs.{extension[:-3]}')

    def run(self, **kwargs):
        super().run(self.token)


if __name__ == "__main__":
    bot = SpoonMusic(discord.Intents.all(), token)

    bot.run()
