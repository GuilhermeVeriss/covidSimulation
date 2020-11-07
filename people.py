from data import *
from numpy import array
from pickle import load


font = open("ambiente.xml", "rb")
regions, matrix = load(font).values()


def create_person(pos):

    person = {
        "pos": pos,
        "vel": [0, 0],
        "size": .3,
        "place": ""
    }
    person["circle"] = list(map(lambda i: to_pixel(i), [pos[1]-person["size"], pos[0]-person["size"],
                                                        pos[1]+person["size"], pos[0]+person["size"]]))

    return person


def update_local(per):
    r, c = per["pos"]
    current_place = list(regions.keys())[list(regions.values()).index(matrix[r][c])]

    per["place"] = current_place


def process(per):
    # PROCESSAR A MECÂNICA

    # Rotas

    # Forças

    # Nova velocidade

    # Nova posição
    per["pos"] = list(array(per["pos"]) + array(per["vel"]))

    # PROCESSAR A DOENÇA

