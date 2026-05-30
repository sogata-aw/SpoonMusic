import json
import os

import discord
from discord.ext import commands

import datetime as d
import traceback

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

    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        error_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        log_entry = (
            f"[{error_time}] ERREUR Slash Command (COG)\n"
            f"Auteur: {interaction.user} (ID: {interaction.user.id})\n"
            f"Guild: {interaction.guild} | Channel: {interaction.channel}\n"
            f"Erreur: {repr(error)}\n"
            f"Traceback:\n{tb}\n"
            f"{'-' * 60}\n"
        )

        with open("errors.log", "a", encoding="utf-8") as f:
            f.write(log_entry)

        if interaction.response.is_done():
            await interaction.followup.send("❌ Une erreur est survenue (suivi).", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)

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
