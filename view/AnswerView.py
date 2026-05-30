import discord

from view.StartBlindTestView import StartBlindTestView

class AnswerView(discord.ui.View):
    def __init__(self, settings, timeout=180):
        super().__init__(timeout=timeout)
        self.settings = settings

    @discord.ui.button(label="Retour", style=discord.ButtonStyle.green)
    async def retour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=discord.Embed(title="Sélection des paramètres"),
                                                view=StartBlindTestView(settings=self.settings))

    @discord.ui.select(
        placeholder="Choisissez une option",
        min_values=1,
        max_values=3,
        options=[
            discord.SelectOption(label="Titre", value="title"),
            discord.SelectOption(label="Artiste", value="artist"),
            discord.SelectOption(label="Jeu", value="game"),

        ]
    )
    async def answer_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        for key in self.settings["answers"]:
            self.settings["answers"][key] = key in select.values

        await interaction.response.edit_message(embed=discord.Embed(title="Sélection des paramètres"),
                                                view=StartBlindTestView(settings=self.settings))
