import asyncio

import discord

from embed import embed_answers, embed_score


class BlindTestView(discord.ui.View):
    def __init__(self, bot, settings, vc, musics):
        super().__init__()
        self.bot = bot
        self.settings = settings
        self.vc = vc
        self.musics = musics
        self.i = 0
        self.score: dict[str, int] = {}
        self.stop_event: asyncio.Event | None = None

    def is_all_find(self, founded):
        for key in self.settings["answers"]:
            if self.settings["answers"][key] and key not in founded.keys():
                return False
        return True

    async def waiting(self, time):
        await asyncio.sleep(time)
        self.stop_event.set()

    @discord.ui.button(label="Arrêter", style=discord.ButtonStyle.red, emoji="⏹️")
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop_event.set()
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        await voice_client.disconnect()
        await interaction.response.edit_message(embed=discord.Embed(title=":white_check_mark: Le bot a été déconnecté du salon vocal"), view=discord.ui.View())


    @discord.ui.button(label="Suivant", style=discord.ButtonStyle.green, emoji="⏭️")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.vc.stop()
        self.i += 1
        await interaction.response.edit_message(embed=embed_answers(self.settings["answers"], self.i + 1, self.settings["rounds"],), view=self)
        await self.launch_music(interaction)


    async def launch_music(self, interaction: discord.Interaction):
        def check(m):
            return m.channel == interaction.channel

        self.stop_event = asyncio.Event()
        music = self.musics[self.i]
        print(music)

        self.vc.play(discord.FFmpegPCMAudio(music["filename"]))

        asyncio.create_task(self.waiting(time=self.settings["time"]))

        founded = {}
        good_answers = {
            "title": music["title"],
            "artist": music["artist"],
            "game": music["game"]
        }

        while not self.stop_event.is_set():
            try:
                message = await interaction.client.wait_for("message", check=check, timeout=1)
                answers = message.content.lower().split(",")
                answers = [a.lstrip() for a in answers]

                key = message.author.nick if message.author.nick else message.author.name

                if self.settings["answers"]["title"] and "title" not in founded and music["title"].lower() in answers:
                    founded["title"] = key
                    self.score[key] = self.score.get(key, 0) + 1
                if self.settings["answers"]["artist"] and "artist" not in founded and music["artist"].lower() in answers:
                    founded["artist"] = key
                    self.score[key] = self.score.get(key, 0) + 1
                if self.settings["answers"]["game"] and "game" not in founded and music["game"].lower() in answers:
                    founded["game"] = key
                    self.score[key] = self.score.get(key, 0) + 1

                if self.is_all_find(founded):
                    self.stop_event.set()
                else:
                    await interaction.edit_original_response(embed=embed_answers(self.settings["answers"], self.i + 1, self.settings["rounds"], founded, good_answers), view=self)
            except asyncio.TimeoutError:
                continue

        self.score = dict(sorted(self.score.items(), key=lambda item: item[1], reverse=True))
        await interaction.edit_original_response(embed=embed_score(self.score, self.is_all_find(founded)), view=self)

