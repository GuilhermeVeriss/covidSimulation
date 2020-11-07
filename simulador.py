from pickle import load
from tkinter import *
from people import *
from time import sleep


font = open("ambiente.xml", "rb")
regions, matrix = load(font).values()

matrix_w = len(matrix[0])
matrix_h = len(matrix)

root = Tk()
root.title("Ambiente da simulação")

canvas = Canvas(root, bg="white", width=matrix_w, height=matrix_h)
canvas.pack()


people = []

per1 = create_person([10, 10])

people.append((per1, canvas.create_oval(*per1["circle"], fill="blue")))


# Gera os elementos da Canvas
for r in range(matrix_h):
    for c in range(matrix_w):
        if matrix[r][c] == regions["parede"]:
            canvas.create_rectangle(c, r, c+1, r+1, fill="black")


# Processar as pessoas.
for _ in range(1000):
    for person in people:
        per_data, per_canvas = person
        process(per_data)

        # Atualizar canvas
        vel = (to_pixel(per_data["vel"][1]), to_pixel(per_data["vel"][0]))
        canvas.move(per_canvas, *vel)

    canvas.update()
    sleep(0.1)

root.mainloop()
