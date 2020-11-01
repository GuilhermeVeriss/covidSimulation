from tkinter import *
from tkinter import simpledialog, messagebox, ttk
from PIL import Image
from numpy import array
from numpy.linalg import norm
from copy import deepcopy
from pickle import dump


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
rectTool = False

pointsForSelection = []

regions = {}

imgName = "imagens/planta_casa_teste.jpg"
imgTestjpg = Image.open(imgName).convert('L')
imgMatrix = jpg_matrix(imgTestjpg)


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
                btPixels[pos_pixel[0]][pos_pixel[1]].change_color("#FA5858")
        if eraseTool:
            if pos_pixel in selectedPixels:
                selectedPixels.remove(pos_pixel)
                btPixels[pos_pixel[0]][pos_pixel[1]].change_color("#F2F2F2")
        if rectTool:
            global pointsForSelection

            if len(pointsForSelection) == 1:
                ans = messagebox.askquestion("Confirmar", "Deseja selecionar essa região?")
                if ans == "yes":
                    btPixels[pos_pixel[0]][pos_pixel[1]].change_color("#58FA58")
                    pointsForSelection.append(pos_pixel)
                    select_all_pixels(pointsForSelection)
                    pointsForSelection = []
                else:
                    point = pointsForSelection[0]
                    btPixels[point[0]][point[1]].change_color("#F2F2F2")
                    pointsForSelection = []
            elif len(pointsForSelection) == 0:
                btPixels[pos_pixel[0]][pos_pixel[1]].change_color("#58FA58")
                pointsForSelection.append(pos_pixel)


def select_all_pixels(points):
    global selectTool, rectTool
    selectTool = True
    rectTool = False

    x1, y1 = points[0]
    x2, y2 = points[1]
    for line in range(x1, x2+1):
        for column in range(y1, y2+1):
            select_or_erase((line, column))

    selectTool = False
    rectTool = True


def activate_selection():
    global selectTool, eraseTool, rectTool, btSelect, btErase, btSelectRect

    if selecting:
        eraseTool = False
        btErase.configure(background="#F2F2F2")
        selectTool = True
        btSelect.configure(background="#585858")
        rectTool = False
        btSelectRect.configure(background="#F2F2F2")


def activate_erasing():
    global selectTool, eraseTool, rectTool, btSelect, btErase, btSelectRect

    if selecting:
        selectTool = False
        btSelect.configure(background="#F2F2F2")
        eraseTool = True
        btErase.configure(background="#585858")
        rectTool = False
        btSelectRect.configure(background="#F2F2F2")


def activate_rectangle():
    global selectTool, eraseTool, rectTool, btSelect, btErase, btSelectRect

    if selecting:
        rectTool = True
        btSelectRect.configure(background="#585858")
        selectTool = False
        btSelect.configure(background="#F2F2F2")
        eraseTool = False
        btErase.configure(background="#F2F2F2")


def click_event(event):
    select_or_erase((event.x, event.y))


def finish_selection():
    global selecting, selectedPixels
    global btSelect, btSelectRect, btErase, selectTool, eraseTool, rectTool

    btSelect.configure(background="#F2F2F2")
    btErase.configure(background="#F2F2F2")
    btSelectRect.configure(background="#F2F2F2")

    if selecting and len(selectedPixels) != 0:
        selectTool = False
        rectTool = False
        eraseTool = False
        selecting = False
        new_region(selectedPixels)
        selectedPixels = []


def new_region(new_pixels):
    global regions
    global btPixels
    num = len(regions) + 2
    nome = simpledialog.askstring("Nome da Região", "Insira o nome da região")
    regions[nome] = num
    for p in new_pixels:
        imgMatrix[p[0]][p[1]] = num
        btPixels[p[0]][p[1]].active = False
        btPixels[p[0]][p[1]].change_color("#2E64FE")


class Pixel:
    def __init__(self, num, pos, color):
        self.color = color
        self.num = num
        self.pix = canvas.create_rectangle(*pos, pos[0]+1, pos[1]+1, fill=self.color, width=0)
        if num == 0:
            self.active = False
        elif num == 1:
            self.active = True

        canvas.bind("<Button-1>", click_event)

    def change_color(self, new_color):
        self.color = new_color
        canvas.itemconfig(self.pix, fill=self.color)


root = Tk()
root.title("Gerador do Ambiente")
root.configure(background="white")


# DESENHO
drawSpace = Frame(root, padx=20, pady=20)
drawSpace.pack(side=LEFT)

canvas = Canvas(drawSpace, width=len(imgMatrix), height=len(imgMatrix[0]))
canvas.pack(side=LEFT)


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
# Selecionar Retângulo
btSelectRect = Button(selectionTools, width=10, text="Retângulo", command=activate_rectangle)
btSelectRect.pack(side=BOTTOM)

# -----------------------------------------------------------------------

btPixels = deepcopy(imgMatrix)

# GERA O DESENHO
for r in range(len(imgMatrix)):
    for c in range(len(imgMatrix[r])):
        if imgMatrix[r][c] == 0:
            btPixels[r][c] = Pixel(imgMatrix[r][c], (r, c), "black")
        else:
            btPixels[r][c] = Pixel(imgMatrix[r][c], (r, c), "white")
            print(r)

root.mainloop()


env = {"regions": regions, "matrix": imgMatrix}

fontText = open("ambiente.xml", "wb")
dump(env, fontText)
fontText.close()
