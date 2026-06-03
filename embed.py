import discord


def embed_settings(settings={}):
    embed = discord.Embed(title="Sélection des paramètres", description="Résumé des paramètres :")
    if settings == {}:
        embed.add_field(name="Jeux Exclus", value="Autre")
        embed.add_field(name="Réponses à trouver", value="Titre, Artiste")
        embed.add_field(name="Temps de réponse", value="30 secondes")
    else:
        value = ""
        for i in range(len(settings["exclude"])):
            if i == len(settings["exclude"]) - 1:
                value = value + settings["exclude"][i]
            else:
                value = value + settings["exclude"][i] + ","
        embed.add_field(name="Jeux Exclus", value=value)

        value = ""
        if settings["answers"]["title"]:
            value = value + "Titre."
        if settings["answers"]["artist"]:
            value = value + "Artiste."
        if settings["answers"]["game"]:
            value = value + "Jeux."

        value = value.lstrip().replace(".", ", ")
        embed.add_field(name="Réponses à trouver", value=value)

        if settings["time"] == 60:
            value = "1 minute"
        else:
            value = f"{settings['time']} secondes"

        embed.add_field(name="Temps de réponse", value=value)

    return embed


def embed_answers(fields, nb, nb_manches, founded={}, answers=[]):
    embed = discord.Embed(title=f"Manche {nb}/{nb_manches}", color=discord.Color.green())

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


def embed_score(score, all_founded):
    embed = discord.Embed(
        title="Tout a été trouvé ! Voici les scores :" if all_founded else "Pas tout a été trouvé... Voici les scores :",
        color=discord.Color.green()
    )

    for player in score:
        embed.add_field(name=f"{player} : {score[player]}", value="")

    return embed
