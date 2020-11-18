from pickle import load
from numpy import array
from numpy.linalg import norm

font1 = open("grafos.xml", "rb")
forks, way_con = load(font1).values()

font2 = open("ambiente_wayp.xml", "rb")
wayp = load(font2)["positions"]
font3 = open("ambiente2.xml", "rb")
regions = load(font3)["positions"]

wayp.update(regions)
positions = wayp


def middle_p(points):
    return (1/2)*(array(points[0]) + array(points[1]))


def evaluate(node, des_p):
    node["g"] = node["father"]["g"]+norm(middle_p(positions[node["name"]])-middle_p(positions[node["father"]]["name"]))
    node["h"] = norm(positions[node] - des_p)
    node["f"] = node["g"] + node["f"]


def find_route(person, destination):
    start_name = person["place"]
    destination_p = middle_p(positions[destination])

    start = {"name": start_name, "g": 0}

    # lista aberta e fechada

