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


lis = []


def select(a, b):
    # lis.append(pos)
    print((a, b))


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

imgTestjpg = Image.open("imagens/desenhoTestePlanta.jpg").convert('L')
testMatrix = jpg_matrix(imgTestjpg)

startSelection = Button(options, width=40, text="Iniciar seleção")
startSelection.grid(row=1, column=1)


finishSelection = Button(options, width=40, text="Concluir seleção")
finishSelection.grid(row=3, column=1)

# FERRAMENTAS DE SELEÇÃO
# Container
selectionTools = Frame(options)
selectionTools.grid(row=2, column=1)

# Selecionar
btSelect = Button(selectionTools, width=10, text="Selecionar")
btSelect.pack(side=RIGHT)
# Apagar
btErase = Button(selectionTools, width=10, text="Apagar")
btErase.pack(side=LEFT)

# -----------------------------------------------------------------------

pixels = deepcopy(testMatrix)


# GERA O DESENHO
for r in range(len(testMatrix)):
    for c in range(len(testMatrix[r])):
        if testMatrix[r][c] == 0:
            lbNumber = Label(drawSpace, width=0, height=1, bd=0, font="Arial, 5", text=str(testMatrix[r][c]))
            lbNumber.grid(row=r+1, column=c+1)
            lbNumber["bg"] = "black"
        else:
            pixels[r][c] = Button(drawSpace, width=0, height=1, bd=0, font="Arial, 5", text=str(testMatrix[r][c]))
            pixels[r][c].grid(row=r+1, column=c+1)
            # BUG
            pixels[r][c].configure(command=lambda: select()) # BUG


root.mainloop()


