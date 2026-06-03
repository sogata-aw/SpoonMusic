import random


def random_select(data, nb=10, exclude=["Other"]):
    music_list = []
    for i in range(nb):
        choice = random.choice(data)

        while choice in music_list or choice["game"] in exclude or (
                "Other" in exclude and choice["game"] in ["Smash", "Kart"]):
            choice = random.choice(data)
        music_list.append(choice)

    return music_list


