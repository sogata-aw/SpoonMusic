import discord

from embed import embed_settings
from view.AnswerView import AnswerView
from view.StartBlindTestView import StartBlindTestView


class ExcludeView(discord.ui.View):
    def __init__(self, bot, settings, timeout=180):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.settings = settings

    @discord.ui.button(label="Retour", style=discord.ButtonStyle.green)
    async def retour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=embed_settings(self.settings),
                                                view=StartBlindTestView(bot=self.bot, settings=self.settings))

    @discord.ui.select(
        placeholder="Choisissez une option",
        min_values=0,
        max_values=4,
        options=[
            discord.SelectOption(label="Splatoon", value="Splatoon"),
            discord.SelectOption(label="Splatoon 2", value="Splatoon 2"),
            discord.SelectOption(label="Octo Expansion", value="Octo Expansion"),
            discord.SelectOption(label="Splatoon 3", value="Splatoon 3"),
            discord.SelectOption(label="Side Order", value="Side Order"),
            discord.SelectOption(label="Autres", value="Other")
        ]
    )
    async def exclude_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.settings["exclude"] = select.values
        await interaction.response.edit_message(embed=embed_settings(self.settings), view=StartBlindTestView(bot=self.bot, settings=self.settings))
