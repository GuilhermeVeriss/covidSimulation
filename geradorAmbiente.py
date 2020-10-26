from tkinter import *
from PIL import Image
from numpy import array
from numpy.linalg import norm
from copy import deepcopy


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


selectedPixels = []
selecting = False
selectTool = False
eraseTool = False

regions = {}

imgTestjpg = Image.open("imagens/desenhoTestePlanta.jpg").convert('L')
testMatrix = jpg_matrix(imgTestjpg)


def start_selecting():
    global selectedPixels
    global selecting
    selecting = True


def select_or_erase(pos_pixel):
    global btPixels
    if selecting and btPixels[pos_pixel[0]][pos_pixel[1]].active:
        if selectTool:
            if pos_pixel not in selectedPixels:
                selectedPixels.append(pos_pixel)
                btPixels[pos_pixel[0]][pos_pixel[1]].change_color("#FE2E2E")
        if eraseTool:
            if pos_pixel in selectedPixels:
                selectedPixels.remove(pos_pixel)
                btPixels[pos_pixel[0]][pos_pixel[1]].change_color("#F2F2F2")


def activate_selection():
    global selectTool
    global eraseTool
    eraseTool = False
    selectTool = True


def activate_erasing():
    global selectTool
    global eraseTool
    selectTool = False
    eraseTool = True


def finish_selection():
    global selecting
    global selectedPixels
    if selecting and len(selectedPixels) != 0:
        selecting = False
        new_region(selectedPixels)
        selectedPixels = []


def get_region_name():
    name = None

    def get_name():
        nonlocal name
        nonlocal input_name_frame
        name = name_box.get()
        input_name_frame.destroy()

    input_name_frame = Toplevel(root, padx=50, pady=30)
    input_name_frame.title("Nome")

    name_box = Entry(input_name_frame)
    name_box.pack()

    finish_bt = Button(input_name_frame, text="Ok", command=get_name)
    finish_bt.pack()
    input_name_frame.mainloop()

    return name


def new_region(new_pixels):
    global btPixels

    num = len(regions) + 2
    regions[get_region_name()] = num
    for p in new_pixels:
        testMatrix[p[0]][p[1]] = num
        btPixels[p[0]][p[1]].active = False


class Pixel:
    def __init__(self, num, pos):
        self.bt = Button(drawSpace, width=0, height=1, bd=0, font="Arial, 5", text=str(num),
                         command=lambda: select_or_erase(pos), bg="#F2F2F2")
        self.bt.grid(row=pos[0]+1, column=pos[1]+1)
        self.active = True

    def change_color(self, color):
        self.bt["bg"] = color


root = Tk()
root.title("Gerador do Ambiente")
root.configure(background="white")


# DESENHO
drawSpace = Frame(root, padx=20, pady=20)
drawSpace.pack(side=LEFT)

# =========================================================================
# OPÇÕES
options = Frame(root, padx=20, pady=20)
options.pack(side=RIGHT)

startSelection = Button(options, width=40, text="Iniciar seleção", command=start_selecting)
startSelection.grid(row=1, column=1)


finishSelection = Button(options, width=40, text="Concluir seleção", command=finish_selection)
finishSelection.grid(row=3, column=1)

# FERRAMENTAS DE SELEÇÃO
# Container
selectionTools = Frame(options)
selectionTools.grid(row=2, column=1)

# Selecionar
btSelect = Button(selectionTools, width=10, text="Selecionar", command=activate_selection)
btSelect.pack(side=RIGHT)
# Apagar
btErase = Button(selectionTools, width=10, text="Apagar", command=activate_erasing)
btErase.pack(side=LEFT)

# -----------------------------------------------------------------------

btPixels = deepcopy(testMatrix)

# GERA O DESENHO
for r in range(len(testMatrix)):
    for c in range(len(testMatrix[r])):
        if testMatrix[r][c] == 0:
            lbNumber = Label(drawSpace, width=0, height=1, bd=0, font="Arial, 5", text=str(0))
            lbNumber.grid(row=r+1, column=c+1)
            lbNumber["bg"] = "black"
        else:
            btPixels[r][c] = Pixel(testMatrix[r][c], (r, c))

root.mainloop()

print(regions)