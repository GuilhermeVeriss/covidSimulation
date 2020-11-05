from data import *
from numpy import array


def create_person(pos):

    person = {
        "pos": array([pos]),
        "vel": [],
        "size": 3,
        "job": [],       # Armazena as informações da pessoa, como rotina, movimentação, etc
        "visionfield": [],
        "route": []
    }
    person["creationArguments"] = [pos[0]-person["size"], pos[1]-person["size"],
                                   pos[0]+person["size"], pos[1]+person["size"]]

    return person

