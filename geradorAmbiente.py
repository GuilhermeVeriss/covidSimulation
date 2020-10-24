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


# FERRAMENTAS DE SELEÇÃO
# Container
selectionTools = Frame(options)
selectionTools.grid(row=2, column=1)

# Selecionar
select = Button(selectionTools, width=10, text="Selecionar")
select.pack(side=RIGHT)
# Apagar
erase = Button(selectionTools, width=10, text="Apagar")
erase.pack(side=LEFT)

# -----------------------------------------------------------------------


# GERA O DESENHO
for r in range(len(testMatrix)):
    for c in range(len(testMatrix[r])):

        if testMatrix[r][c] == 0:
            lbNumber = Label(drawSpace, width=0, height=1, bd=0, font="Arial, 5", text=str(testMatrix[r][c]))
            lbNumber.grid(row=r, column=c)
            lbNumber["bg"] = "black"
        else:
            btNumber = Button(drawSpace, width=0, height=1, bd=0, font="Arial, 5", text=str(testMatrix[r][c]))
            btNumber.grid(row=r, column=c)


root.mainloop()
