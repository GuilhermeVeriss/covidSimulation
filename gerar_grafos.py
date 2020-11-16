"""Use este arquivo para definir os grafos e passá-los para um arquivo xml"""

from pickle import dump


forks = {
    "a1": ["a2"],
    "a2": ["a1", "a6"],
    "a3": ["a5"],
    "a4": ["a5"],
    "a5": ["a4", "a3", "a7", "a6"],
    "a6": ["a2", "a5", "a8"],
    "a7": ["a5"],
    "a8": ["a6"]
}

wayp_connections = {
    "w6": ("a1", "a2"),
    "w7": ("a2", "a6"),
    "w8": ("a3", "a5"),
    "w9": ("a5", "a6"),
    "w10": ("a4", "a5"),
    "w11": ("a5", "a7"),
    "w12": ("a6", "a8"),
}







