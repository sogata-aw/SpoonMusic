from typing import Any

import discord


class StartBlindTestView(discord.ui.View):
    def __init__(self, settings: dict[str, Any] = None):
        super().__init__(timeout=180)
        if not settings:
            self.settings = {
                "exclude": ["Other"],
                "answers": {
                    "title": True,
                    "artist": True,
                    "game": False,
                },
                "time": 15,
                "abbreviations": False
            }
        else:
            self.settings = settings

    @discord.ui.button(label="Exclusions", style=discord.ButtonStyle.grey)
    async def exclusion(self, interaction: discord.Interaction, button: discord.ui.Button):
        from view.ExcludeView import ExcludeView
        await interaction.response.edit_message(embed=discord.Embed(title="Exclure des jeux"),
                                                view=ExcludeView(settings=self.settings))

    @discord.ui.button(label="Réponses", style=discord.ButtonStyle.grey)
    async def answers(self, interaction: discord.Interaction, button: discord.ui.Button):
        from view.AnswerView import AnswerView
        await interaction.response.edit_message(embed=discord.Embed(title="Quoi répondre ?"),
                                                view=AnswerView(settings=self.settings))

    @discord.ui.button(label="Temps de réponse", style=discord.ButtonStyle.grey)
    async def timing(self, interaction: discord.Interaction, button: discord.ui.Button):
        from view.TimeView import TimeView
        await interaction.response.edit_message(embed=discord.Embed(title="Temps pour deviner"),
                                                view=TimeView(settings=self.settings))

    @discord.ui.button(label="Abbréviations", style=discord.ButtonStyle.red, emoji="❌")
    async def abbreviations(self, interaction: discord.Interaction, button: discord.ui.Button):
        if button.style == discord.ButtonStyle.red:
            button.style = discord.ButtonStyle.green
            button.emoji = "✅"
            self.settings["abbreviations"] = True
        else:
            button.style = discord.ButtonStyle.red
            button.emoji = "❌"
            self.settings["abbreviations"] = False

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(title="Start"))