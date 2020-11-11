from data import *
from numpy import array, matrix
from numpy.linalg import norm
from pickle import load
from math import pi, sin, cos


font = open("ambiente.xml", "rb")
regions, matrix_env = load(font).values()
wall = regions["parede"]


def rotate(ang):
    """Retorna matriz de rotação a partir de determinado ângulo"""
    return array([[cos(ang), sin(ang)], [-sin(ang), cos(ang)]])


def round_array(vec):
    return array([round(vec[0]), round(vec[1])])


def create_person(pos):

    person = {
        "pos": array(pos),
        "vel": array([1, -1]),
        "size": 2,
        "place": "",
        "visionRange": 8,
        "visionAngle": (2/3)*pi,
        "vision": array([0, -1])
    }

    if person["vel"].any() != 0:
        person["vision"] = (person["visionRange"]/norm(person["vel"]))*person["vel"]

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
    obstacles = vision_scan(per)  # wall, people

    # ------------------------------------------------
    # Forças

    f_forward = array([0, 0])

    # Parede
    f_wall = array([0, 0])
    if obstacles["wall"][1]:
        per_wall = obstacles["wall"][0] - per["pos"]
        f_wall = -round_array((q_wall*per_wall) / (norm(per_wall)**4))

    f_person = array([0, 0])

    f_all = f_forward + f_wall + f_person

    # -------------------------------------------------
    # Nova velocidade
    if norm(f_all) != 0:
        per["vel"] = round_array(v*(f_all/norm(f_all)) + per["vel"])

    # Nova posição
    per["pos"] = per["pos"] + per["vel"]

    # Apagar depois, é só pra construir o campo de visão

    # return x[0]

    # PROCESSAR A DOENÇA


def vision_scan(per):
    if per["vel"].any() != 0:
        per["vision"] = (per["visionRange"]/norm(per["vel"]))*per["vel"]
    start = round_array(rotate(-pi/3).dot(per["vision"]))

    # lim_points = []

    wall_p = []  # lista dos pontos de uma parede

    for i in range(round((2/3)*pi*per["visionRange"])+1):
        ang = i*(1/per["visionRange"])
        scan_array = round_array(rotate(ang).dot(start))

        un = (1 / norm(scan_array)) * scan_array

        for p in range(1, per["visionRange"]+1):
            point = round_array(per["pos"] + p * un)

            if matrix_env[point[0]][point[1]] == wall:  # Encontra as paredes
                wall_p.append(point)
                continue

            # lim_points.append(point)

    wall_array = False
    wall_act = False
    if wall_p:
        distances = list(map(lambda e: norm(e - per["pos"]), wall_p))
        wall_array = wall_p[distances.index(min(distances))]
        wall_act = True

    obstacles = {"wall": (wall_array, wall_act), "people": 0}

    # return lim_points, obstacles
    return obstacles
