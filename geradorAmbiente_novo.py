from tkinter import *
from tkinter import simpledialog
from numpy import array
from PIL import Image
from copy import deepcopy
from pickle import dump


def rgb_color(rgb):
    return '#%02x%02x%02x' % rgb


def input_colors():
    global regions
    for hex_color in color_code:
        color_show.configure(bg=hex_color)
        while True:
            name = simpledialog.askstring("Inserir nome", "Insira o nome da região")
            if name:
                regions[name] = color_code[hex_color]
                break


imgName = "imagens/color_identifier.png"
save_data = "ambiente.xml"


imgTestJpg = Image.open(imgName)

imgArray = array(imgTestJpg)

matrix_res = list(deepcopy(imgArray))
matrix_res = list(map(lambda x: list(x), matrix_res))

color_code = {}
regions = {}


root = Tk()
root.title("Selecionar Regiões")

draw_space = Frame(root)
draw_space.pack(side=LEFT)

options = Frame(root)
options.pack(side=RIGHT)

color_show = Label(options, width=15, height=5)
color_show.pack(side=TOP)

select = Button(options, width=30, text="Definir nome", command=input_colors)
select.pack(side=BOTTOM)

canvas = Canvas(draw_space, width=len(imgArray[0]), height=len(imgArray))
canvas.pack()


for r in range(len(imgArray)):
    for c in range(len(imgArray[r])):
        color = rgb_color(tuple(imgArray[r][c]))
        if color not in color_code.keys():
            color_code[color] = len(color_code) + 1
        matrix_res[r][c] = color_code[color]
        canvas.create_rectangle(r, c, r+1, c+1, fill=color, width=0)


root.mainloop()

env = {"regions": regions, "matrix": matrix_res}

fontText = open(save_data, "wb")
dump(env, fontText)
fontText.close()
