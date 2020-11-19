from math import sin, cos
from numpy import array


def to_pixel(n):
    return round(n*scale)


def rotate(ang):
    """Retorna matriz de rotação a partir de determinado ângulo"""
    return array([[cos(ang), sin(ang)], [-sin(ang), cos(ang)]])


def round_array(vec):
    return array([round(vec[0]), round(vec[1])])


scale = 1   # pixel/metros (1 pixel vale quantos metros?)

q_wall = 200
q_per = 100

v = 1.4
