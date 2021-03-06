from data import *
from rota import *
from numpy import array, zeros
from numpy.linalg import norm
from pickle import load
from math import pi


font = open("ambiente2.xml", "rb")
regions, matrix_env, positions = load(font).values()
wall = regions["parede"]

matrix_people = zeros((len(matrix_env), len(matrix_env[0])), dtype=int)


def create_person(pos):

    person = {
        "pos": array(pos),
        "vel": array([1, -1]),
        "size": 2,
        "place": "",
        "visionRange": 10,
        "visionAngle": (2/3)*pi,
        "vision": array([0, -1])
    }

    update_local(person)

    person["vision"] = (person["visionRange"]/norm(person["vel"]))*person["vision"]

    if person["vel"].any() != 0:
        person["vision"] = (person["visionRange"]/norm(person["vel"]))*person["vel"]

    matrix_people[person["pos"][0]][person["pos"][1]] = 1
    person["circle"] = list(map(lambda i: to_pixel(i), [pos[1]-person["size"], pos[0]-person["size"],
                                                        pos[1]+person["size"], pos[0]+person["size"]]))

    return person


def update_local(per):
    r, c = per["pos"]
    current_place = list(regions.keys())[list(regions.values()).index(matrix_env[r][c])]
    per["place"] = current_place


def process(per):
    # PROCESSAR A MECÂNICA

    # Destino
    if per["route"]:
        d = 10  # distância do destino
        if norm(list(per["route"].values())[-1] - per["pos"]) <= d:
            per["route"].pop(list(per["route"].keys())[-1])

    # route = find_route(per, "a4")

    # Visão
    obstacles = vision_scan(per)  # wall, people

    # ------------------------------------------------
    # Forças

    # Forward
    f1 = array([0, 0])
    f2 = array([0, 0])
    if per["route"]:
        current_point = list(per["route"].values())[-1]
        per_des = current_point - per["pos"]
        f1 = per_des/norm(per_des)

    if len(per["route"]) >= 2:
        current_point2 = list(per["route"].values())[-2]
        per_des2 = current_point2 - per["pos"]
        f2 = per_des2 / norm(per_des2)
        f2 = (1/2) * f2

    f_forward = (f1 + f2)/norm(f1 + f2)

    # Parede
    f_wall = array([0, 0])
    if obstacles["wall"][1]:
        per_wall = obstacles["wall"][0] - per["pos"]
        f_wall = -(q_wall*per_wall) / (norm(per_wall)**4)

    # Pessoas

    f_person = array([0, 0])
    people = obstacles["people"]

    if len(people):
        for p in people:
            per_per = p - per["pos"]
            cos_ang = (per["vision"] * per_per) / (norm(per["vision"]) * norm(per_per))
            f_person = f_person + (-q_per*per_per*cos_ang) / (norm(per_per)**2)

    # Total
    f_all = f_forward + f_wall + f_person

    # -------------------------------------------------
    # Nova velocidade
    if norm(f_all) != 0:
        per["vel"] = round_array((1/2)*(v*(f_all/norm(f_all)) + per["vel"]))

    # Nova posição
    matrix_people[per["pos"][0]][per["pos"][1]] = 0

    per["pos"] = per["pos"] + per["vel"]
    update_local(per)

    matrix_people[per["pos"][0]][per["pos"][1]] = 1

    # return x[0]

    # PROCESSAR A DOENÇA


def vision_scan(per):
    if per["vel"].any() != 0:
        per["vision"] = (per["visionRange"]/norm(per["vel"]))*per["vel"]
    start = round_array(rotate(-pi/3).dot(per["vision"]))

    # lim_points = []

    wall_p = []  # lista dos pontos de uma parede
    people_p = []

    for i in range(round((2/3)*pi*per["visionRange"])+1):
        ang = i*(1/per["visionRange"])
        scan_array = round_array(rotate(ang).dot(start))

        un = (1 / norm(scan_array)) * scan_array

        for p in range(1, per["visionRange"]+1):
            point = round_array(per["pos"] + p * un)

            if matrix_env[point[0]][point[1]] == wall:  # Encontra as paredes
                wall_p.append(point)
                continue

            elif matrix_people[point[0]][point[1]]:
                if not any(p.all() == point.all() for p in people_p):
                    people_p.append(point)


    wall_array = False
    wall_act = False
    if wall_p:
        distances = list(map(lambda e: norm(e - per["pos"]), wall_p))
        wall_array = wall_p[distances.index(min(distances))]
        wall_act = True

    obstacles = {"wall": (wall_array, wall_act), "people": people_p}
    return obstacles
