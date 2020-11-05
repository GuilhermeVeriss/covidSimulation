from pickle import load
from tkinter import *
from people import *


font = open("ambiente.xml", "rb")
regions, matrix = load(font).values()

matrix_w = len(matrix[0])
matrix_h = len(matrix)

root = Tk()
root.title("Ambiente da simulação")

canvas = Canvas(root, bg="white", width=matrix_w, height=matrix_h)
canvas.pack()

canvas.create_oval(*create_person((20, 20))["creationArguments"], fill="blue")

for r in range(matrix_h):
    for c in range(matrix_w):
        if matrix[r][c] == regions["parede"]:
            canvas.create_rectangle(c, r, c+1, r+1, fill="black")

root.mainloop()
