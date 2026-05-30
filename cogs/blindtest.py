import discord
from discord.ext import commands, tasks

import asyncio

from view.ExcludeView import ExcludeView
from view.StartBlindTestView import StartBlindTestView


@discord.app_commands.guild_only()
class BlindTestCog(commands.GroupCog, group_name="blindtest"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.tree.error(coro=self.bot.on_app_command_error)
        self.tasks: dict[str, asyncio.Task] = {}
        self.time = 0
        self.musics = []

    @discord.app_commands.command(name="start", description="Connecte le bot est lance la procédure de lancement")
    async def start(self, interaction: discord.Interaction):
        voice_chat = interaction.user.voice.channel

        if not voice_chat:
            await interaction.send_message(":x: Vous n'êtes pas dans un salon vocal")
        else:
            if not discord.utils.get(self.bot.voice_clients, guild=interaction.guild):
                await voice_chat.connect()

        await interaction.response.send_message(embed=discord.Embed(title="Sélection des paramètres"), view=StartBlindTestView())


async def setup(bot):
    await bot.add_cog(BlindTestCog(bot))