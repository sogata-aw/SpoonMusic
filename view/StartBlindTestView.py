import asyncio
from typing import Any
from blindTestUtilities import random_select
from embed import embed_answers
from view.BlindTestView import BlindTestView
import discord
import json


class StartBlindTestView(discord.ui.View):
    def __init__(self, bot, settings: dict[str, Any] = None):
        super().__init__(timeout=180)
        self.bot = bot
        with open("ost-data.json", "r") as file:
            self.data = json.load(file)
        if not settings:
            self.settings = {
                "exclude": ["Other"],
                "answers": {
                    "title": True,
                    "artist": True,
                    "game": False,
                },
                "time": 50,
                "rounds": 10,
                "abbreviations": False
            }
        else:
            self.settings = settings

    @discord.ui.button(label="Exclusions", style=discord.ButtonStyle.grey)
    async def exclusion(self, interaction: discord.Interaction, button: discord.ui.Button):
        from view.ExcludeView import ExcludeView
        await interaction.response.edit_message(embed=discord.Embed(title="Exclure des jeux"),
                                                view=ExcludeView(bot=self.bot, settings=self.settings))

    @discord.ui.button(label="Réponses", style=discord.ButtonStyle.grey)
    async def answers(self, interaction: discord.Interaction, button: discord.ui.Button):
        from view.AnswerView import AnswerView
        await interaction.response.edit_message(embed=discord.Embed(title="Quoi répondre ?"),
                                                view=AnswerView(bot=self.bot, settings=self.settings))

    @discord.ui.button(label="Temps de réponse", style=discord.ButtonStyle.grey)
    async def timing(self, interaction: discord.Interaction, button: discord.ui.Button):
        from view.TimeView import TimeView
        await interaction.response.edit_message(embed=discord.Embed(title="Temps pour deviner"),
                                                view=TimeView(bot=self.bot, settings=self.settings))

    # @discord.ui.button(label="Abbréviations", style=discord.ButtonStyle.red, emoji="❌")
    # async def abbreviations(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     if button.style == discord.ButtonStyle.red:
    #         button.style = discord.ButtonStyle.green
    #         button.emoji = "✅"
    #         self.settings["abbreviations"] = True
    #     else:
    #         button.style = discord.ButtonStyle.red
    #         button.emoji = "❌"
    #         self.settings["abbreviations"] = False
    #
    #     await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        music_list = random_select(self.data)
        view = BlindTestView(bot=self.bot, settings=self.settings, vc=vc, musics=music_list)
        await interaction.response.edit_message(embed=embed_answers(self.settings["answers"], 1, self.settings["rounds"]), view=view)
        await view.launch_music(interaction)
