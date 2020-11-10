from data import *
from numpy import array, matrix
from numpy.linalg import norm
from pickle import load
from math import pi, sin, cos


font = open("ambiente.xml", "rb")
regions, matrix_env = load(font).values()


def rotate(ang):
    """Retorna matriz de rotação a partir de determinado ângulo"""
    return array([[cos(ang), sin(ang)], [-sin(ang), cos(ang)]])


def round_array(vec):
    return array([round(vec[0]), round(vec[1])])


def create_person(pos):

    person = {
        "pos": array(pos),
        "vel": array([1, 0]),
        "size": 2,
        "place": "",
        "visionRange": 25,
        "visionAngle": (2/3)*pi
    }
    person["circle"] = list(map(lambda i: to_pixel(i), [pos[1]-person["size"], pos[0]-person["size"],
                                                        pos[1]+person["size"], pos[0]+person["size"]]))

    return person


def update_local(per):
    r, c = per["pos"]
    current_place = list(regions.keys())[list(regions.values()).index(matrix_env[r][c])]
    per["place"] = current_place


def process(per):
    # PROCESSAR A MECÂNICA

    # Rotas

    # Visão

    # ------------------------------------------------
    # Forças

    f_forward = array([0, 0])

    f_wall = array([0.2, 0.1])

    f_person = array([0, 0])

    f_all = f_forward + f_wall + f_person

    # -------------------------------------------------
    # Nova velocidade
    if norm(f_all) != 0:
        per["vel"] = (v*(f_all/norm(f_all)) + per["vel"])

    # Nova posição
    per["pos"] = round_array(per["pos"] + per["vel"])

    # Apagar depois, é só pra construir o campo de visão
    x = vision_scan(per)
    return x

    # PROCESSAR A DOENÇA


def vision_scan(per):
    vision_array = (per["visionRange"]/norm(per["vel"]))*per["vel"]
    start = round_array(rotate(-pi/3).dot(vision_array))

    lim_points = []
    for i in range(round((2/3)*pi*per["visionRange"])+1):
        ang = i*(1/per["visionRange"])
        scan_array = round_array(rotate(ang).dot(start))
        point = per["pos"] + scan_array
        lim_points.append(point)

        un = (1 / norm(scan_array)) * scan_array
        for p in range(1, per["visionRange"]+1):
            point1 = per["pos"] + round_array(p * un)
            lim_points.append(point1)

    return lim_points



