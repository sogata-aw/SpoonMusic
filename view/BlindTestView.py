import asyncio

import discord

from embed import embed_answers


async def waiting(time, stop_event):
    await asyncio.sleep(time)
    stop_event.set()


class BlindTestView(discord.ui.View):
    def __init__(self, settings, vc, musics):
        super().__init__()
        self.settings = settings
        self.vc = vc
        self.musics = musics
        self.i = 0

    @discord.ui.button(label="Suivant", style=discord.ButtonStyle.green, emoji="⏭️")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.vc.stop()
        self.i += 1
        await interaction.response.edit_message(embed=embed_answers(self.settings["answers"]), view=self)
        await self.launch_music(interaction)


    async def launch_music(self, interaction: discord.Interaction):
        def check(m):
            return m.channel == interaction.channel

        stop_event = asyncio.Event()
        music = self.musics[self.i]
        print(music)

        self.vc.play(discord.FFmpegPCMAudio(music["filename"]))

        asyncio.create_task(waiting(time=self.settings["time"], stop_event=stop_event))

        founded = {}
        good_answers = {
            "title" : music["title"],
            "artist" : music["artist"],
            "game" : music["game"]
        }

        while not stop_event.is_set():
            try:
                message = await interaction.client.wait_for("message", check=check, timeout=1)
                answers = message.content.split(",")
                answers = [a.lower() for a in answers]

                if self.settings["answers"]["title"] and "title" not in founded and music["title"].lower() in answers:
                    founded["title"] = message.author.name
                if self.settings["answers"]["artist"] and "artist" not in founded and music["artist"].lower() in answers:
                    founded["artist"] = message.author.name
                if self.settings["answers"]["game"] and "game" not in founded and music["game"].lower() in answers:
                    founded["game"] = message.author.name

                await interaction.edit_original_response(embed=embed_answers(self.settings["answers"], founded, good_answers), view=self)
            except asyncio.TimeoutError:
                continue

