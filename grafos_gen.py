from pickle import load, dump

way_points = "ambiente_wayp.xml"

font = open(way_points, "rb")
regions, matrix = load(font).values()


fork = {}
# Deve nomear as portas como "p" + int
for region in regions:
    nodes = input("{node}: ".format(node=region))

    if not nodes:
        continue

    fork[region] = list(nodes.split(", "))


save_data = ""


fontText = open(save_data, "wb")
dump(fork, fontText)

fontText.close()
