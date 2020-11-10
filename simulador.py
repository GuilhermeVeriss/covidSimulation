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

per1 = create_person([100, 100])

people.append((per1, canvas.create_oval(*per1["circle"], fill="blue")))


# Gera os elementos da Canvas
for r in range(matrix_h):
    for c in range(matrix_w):
        if matrix[r][c] == regions["parede"]:
            canvas.create_rectangle(c, r, c+1, r+1, fill="black")


vision_pix = []

# Processar as pessoas.
for _ in range(1000):
    for person in people:
        per_data, per_canvas = person
        pixels_vision = process(per_data)

        if len(vision_pix):
            for pix in vision_pix:
                canvas.delete(pix)
            vision_pix = []
            for pix in pixels_vision:
                vision_pix.append(canvas.create_rectangle(pix[1], pix[0], pix[1]+3, pix[0]+3, fill="red", width=0))

        elif not len(vision_pix):
            for pix in pixels_vision:
                vision_pix.append(canvas.create_rectangle(pix[1], pix[0], pix[1]+1, pix[0]+1, fill="red", width=0))

        # Atualizar canvas
        # vel = (per_data["vel"][1], per_data["vel"][0]))
        canvas.move(per_canvas, per_data["vel"][1], per_data["vel"][0])

    canvas.update()
    sleep(.1)

root.mainloop()
