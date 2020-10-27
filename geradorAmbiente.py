from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
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
rectTool = False

pointsForSelection = []

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
        testMatrix[p[0]][p[1]] = num
        btPixels[p[0]][p[1]].active = False
        btPixels[p[0]][p[1]].change_color("#2E64FE")


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
# Selecionar Retângulo
btSelectRect = Button(selectionTools, width=10, text="Retângulo", command=activate_rectangle)
btSelectRect.pack(side=BOTTOM)

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
