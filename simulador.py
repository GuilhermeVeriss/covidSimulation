from pickle import load
from tkinter import *
from PIL import Image, ImageTk


font = open("ambiente.xml", "rb")
regions, matrixImg = load(font).values()

print(regions)
for i in matrixImg:
    print(i)

# root = Tk()

# img = ImageTk.PhotoImage(Image.open("imagens/desenhoTestePlanta.jpg"))
# canvas = Canvas(root, width=img.width(), height=img.height())
# canvas.create_image(0, 0, anchor=NW, image=img)
# canvas.pack()
# root.mainloop()
