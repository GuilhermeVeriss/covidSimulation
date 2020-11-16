from tkinter import *
from people import *
from pickle import load
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

per1 = create_person([90, 100])
per2 = create_person([120, 110])
per3 = create_person([130, 110])


people.append((per1, canvas.create_oval(*per1["circle"], fill="blue")))
people.append((per2, canvas.create_oval(*per2["circle"], fill="blue")))
people.append((per3, canvas.create_oval(*per3["circle"], fill="blue")))


"""Gera os elementos da Canvas"""
for r in range(matrix_h):
    for c in range(matrix_w):
        if matrix[r][c] == regions["parede"]:
            canvas.create_rectangle(c, r, c+1, r+1, fill="black")



"""Processar as pessoas"""
while True:
    print("+-"*250)

    for person in people:
        per_data, per_canvas = person
        process(per_data)

        """Atualizar canvas"""
        canvas.move(per_canvas, per_data["vel"][1], per_data["vel"][0])

    canvas.update()
    sleep(0.01)

root.mainloop()
