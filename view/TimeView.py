import discord

from embed import embed_settings
from view.StartBlindTestView import StartBlindTestView


class TimeView(discord.ui.View):
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
        min_values=1,
        max_values=3,
        options=[
            discord.SelectOption(label="10 secondes", value="10"),
            discord.SelectOption(label="15 secondes", value="15"),
            discord.SelectOption(label="30 secondes", value="30"),
            discord.SelectOption(label="1 minute", value="60")
        ]
    )
    async def answer_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.settings["time"] = int(select.values[0])

        await interaction.response.edit_message(embed=embed_settings(self.settings),
                                                view=StartBlindTestView(bot=self.bot, settings=self.settings))
