from tkinter import *
from PIL import Image
from numpy import array
from numpy.linalg import norm


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


window = Tk()
window.title("Gerador do Ambiente")

imgTestjpg = Image.open("imagens/desenhoTestePlanta.jpg").convert('L')
testMatrix = jpg_matrix(imgTestjpg)

for r in range(len(testMatrix)):
    for c in range(len(testMatrix[r])):
        lbNumber = Button(window, width=0, height=1, bd=0, font="Arial, 5", text=str(testMatrix[r][c]))
        if testMatrix[r][c] == 0:
            lbNumber["bg"] = "black"
        lbNumber.grid(row=r, column=c)
        # print(r, c)

window.mainloop()
