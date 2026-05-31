import discord


def embed_answers(fields, founded={}, answers=[]):
    embed = discord.Embed(title="Réponses trouvées", color=discord.Color.green())

    if fields["title"]:
        embed.add_field(
            name="Titre",
            value=f"{answers["title"]} : trouvé par {founded["title"]}" if founded.get("title") else "????",
            inline=False
        )

    if fields["artist"]:
        embed.add_field(
            name="Artiste",
            value=f"{answers["artist"]} : trouvé par {founded["artist"]}" if founded.get("artist") else "????",
            inline=False
        )

    if fields["game"]:
        embed.add_field(
            name="Jeu",
            value=f"{answers["game"]} : trouvé par {founded["game"]}" if founded.get("game") else "????",
            inline=False
        )

    return embed