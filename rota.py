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
    return (1 / 2) * (array(points[0]) + array(points[1]))


def evaluate(node, des_p):
    if node["father"]:
        node_p = middle_p(positions[node["name"]])
        father_p = middle_p(positions[node["father"]["name"]])

        node["g"] = node["father"]["g"] + norm(node_p - father_p)
        node["h"] = norm(positions[node["name"]] - des_p)
        node["f"] = node["g"] + node["h"]


def sort(lis):
    # ordena a open_list
    sorted(lis, key=lis.get("f"))


def find_route(person, destination):
    start = person["place"]
    destination_p = middle_p(positions[destination])

    open_list = {}
    closed_list = {start: {"name": start, "father": 0, "g": 0}}

    # setup
    for node in way_con[closed_list[start]["name"]]:
        open_list[node] = {"name": node, "father": closed_list[start]}
        evaluate(open_list[node], destination_p)

    sort(open_list)

    analyze = list(open_list.values())[0]

    while analyze["name"] not in way_con[destination]:
        for node in forks[analyze["name"]]:
            open_list[node] = {"name": node, "father": analyze}
            evaluate(open_list[node], destination_p)

        del open_list[analyze["name"]]
        closed_list.update(analyze)

        sort(open_list)
        analyze = list(open_list.values())[0]

    route = []
    item = analyze
    while item["father"]:
        route.append(item["name"])
        item = item["father"]
    print(route)
