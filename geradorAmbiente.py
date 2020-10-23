from tkinter import *
from PIL import Image
from numpy import array
from numpy.linalg import norm

imgTestjpg = Image.open("imagens/plantaTeste.jpg").convert('L')


def jpg_matrix(img):
    def to_binary(color):
        white = array([255, 255, 255])
        limit = array([230, 230, 230])
        k = norm(white - limit)
        color = array(color)

        if norm(color - white) < k:
            return 1
        return 0

    img = list(array(img))
    return list(map(lambda line: list(map(to_binary, line)), img))

