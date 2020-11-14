from tkinter import *
from tkinter import simpledialog
from numpy import array
from PIL import Image
from copy import deepcopy
from pickle import dump


def rgb_color(rgb):
    rgb = rgb[:3]
    return '#%02x%02x%02x' % rgb


def input_colors():
    global regions
    for hex_color in color_code:
        color_show.configure(bg=hex_color)

        for r1 in range(mat_height):
            for c1 in range(mat_width):
                if matrix_res[r1][c1] == color_code[hex_color]:
                    canvas.itemconfig(pixels[r1][c1], fill=color_highlight)

        while True:
            name = simpledialog.askstring("Inserir nome", "Insira o nome da região")
            if name:
                regions[name] = color_code[hex_color]
                print(regions)
                break

        for r1 in range(mat_height):
            for c1 in range(mat_width):
                if matrix_res[r1][c1] == color_code[hex_color]:
                    canvas.itemconfig(pixels[r1][c1], fill=hex_color)


imgName = "imagens/planta_casa_cores_wayp.png"
save_data = ""

color_highlight = "blue"


imgTestJpg = Image.open(imgName)

imgArray = array(imgTestJpg)

matrix_res = list(deepcopy(imgArray))
matrix_res = list(map(lambda x: list(x), matrix_res))

mat_width = len(matrix_res[0])
mat_height = len(matrix_res)

pixels = list(deepcopy(imgArray))
pixels = list(map(lambda x: list(x), pixels))

color_code = {}
regions = {}


root = Tk()
root.title("Selecionar Regiões")

draw_space = Frame(root)
draw_space.pack(side=LEFT)

options = Frame(root)
options.pack(side=RIGHT)

color_show = Label(options, width=15, height=5, borderwidth=2, relief="solid")
color_show.pack(side=TOP)

select = Button(options, width=30, text="Definir nome", command=input_colors)
select.pack(side=BOTTOM)

canvas = Canvas(draw_space, width=mat_width, height=mat_height)
canvas.pack()


for r in range(mat_height):
    for c in range(mat_width):
        color = rgb_color(tuple(imgArray[r][c]))
        if color not in color_code.keys():
            color_code[color] = len(color_code) + 1
        matrix_res[r][c] = color_code[color]
        pixels[r][c] = canvas.create_rectangle(c, r, c+1, r+1, fill=color, width=0)


root.mainloop()

env = {"regions": regions, "matrix": matrix_res}

fontText = open(save_data, "wb")
dump(env, fontText)
fontText.close()



