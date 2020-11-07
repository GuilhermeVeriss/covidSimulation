from data import *
from numpy import array
from numpy.linalg import norm
from pickle import load


font = open("ambiente.xml", "rb")
regions, matrix = load(font).values()


def create_person(pos):

    person = {
        "pos": array(pos),
        "vel": array([1, 0]),
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

    # ------------------------------------------------
    # Forças

    f_forward = array([0, 0])

    f_wall = array([0, 0])

    f_person = array([0, 0])

    f_all = f_forward + f_wall + f_person

    # -------------------------------------------------
    # Nova velocidade
    if norm(f_all) != 0:
        per["vel"] = (v*(f_all/norm(f_all)) + per["vel"])

    # Nova posição
    per["pos"] = per["pos"] + per["vel"]

    # PROCESSAR A DOENÇA

