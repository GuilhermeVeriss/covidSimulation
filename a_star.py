from pickle import load


fork_font = "ambiente_grafos.xml"

font = open(fork_font, "rb")
fork = load(font)

print(fork)
