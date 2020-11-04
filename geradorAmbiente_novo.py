from tkinter import *
from numpy import array
from PIL import Image
from copy import deepcopy


def rgb_color(rgb):
    return '#%02x%02x%02x' % rgb


imgName = "imagens/color_identifier.png"
imgTestJpg = Image.open(imgName)

imgArray = array(imgTestJpg)

matrix_res = deepcopy(imgArray)

root = Tk()
root.title("Selecionar Regiões")

draw_space = Frame(root)
draw_space.pack(side=LEFT)

options = Frame(root)
options.pack(side=RIGHT)

color_show = Label(options, width=15, height=5)
color_show.pack(side=TOP)

select = Button(options, width=30, text="Definir nome")
select.pack(side=BOTTOM)

canvas = Canvas(draw_space, width=len(imgArray[0]), height=len(imgArray))
canvas.pack()


color_code = {}

for r in range(len(imgArray)):
    for c in range(len(imgArray[r])):
        color = rgb_color(tuple(imgArray[r][c]))
        if color not in color_code.keys():
            color_code[color] = len(color_code) + 1
        canvas.create_rectangle(r, c, r+1, c+1, fill=color, width=0)

print(color_code)

root.mainloop()
