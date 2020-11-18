"""Use este arquivo para definir os grafos e passá-los para um arquivo xml"""

from pickle import dump


way_con = {
    "a1": "w6",
    "a2": ("w6", "w7"),
    "a3": "w8",
    "a4": "w10",
    "a5": ("w8", "w9", "w10", "w11"),
    "a6": ("w7", "w9", "w12"),
    "a7": "w11",
    "a8": "w12"
}

forks = {
    "w6": "w7",
    "w7": ("w6", "w9", "w12"),
    "w8": ("w9", "w10", "w11"),
    "w9": ("w7", "w8", "w10", "w11", "w12"),
    "w10": ("w8", "w9", "w11"),
    "w11": ("w10", "w8", "w9"),
    "w12": ("w9", "w7"),
}

env = {"forks": forks, "connections": way_con}

save = open("grafos.xml", "wb")
dump(env, save)
save.close()
