from tkinter import *
import random


def click(event):
    global canvas
    ids = canvas.find_withtag(CURRENT)[0]
    if ids not in clicked:
        try:
            x1, y1, x2, y2 = canvas.coords(ids)
        except ValueError:
            pass
        else:
            print('Номер элемента: ' + str(ids))
            canvas.itemconfig(CURRENT, fill='green')
            canvas.create_text(x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2, text='1', font='Arial {}'.format(int(SQUARE_SIZE / 2)), fill='yellow')
            clicked.add(ids)
    else:
        pass


def nice_print(matrix):
    for i in range(len(matrix)):
        print(*matrix[i])


root = Tk()
clicked = set()
root.title('Сапёр')
SQUARES = 256
SQUARE_SIZE = 20
SQUARE_LIST = []
MINES = 40
MINES_NUM = set(random.sample(range(1, 16**2+1), 40))
size = int(SQUARES ** 0.5) * 21
GRID = list([0] * int(SQUARES ** 0.5) for i in range(int(SQUARES ** 0.5)))
nice_print(GRID)
root.geometry(str(size) + 'x' + str(size))
canvas = Canvas(width=size, height=size)
canvas.pack()
a, b, c, d = 0, 0, 20, 20
a1, b1, c1, d1 = a, b, c, d
for i in range(int(SQUARES ** 0.5)):
    for j in range(int(SQUARES ** 0.5)):
        canvas.create_rectangle(a, b, c, d, outline="black", fill="AntiqueWhite4", width=1)
        canvas.bind('<Button-1>', click)
        a, c = a + 21, c + 21
    b, d = b + 21, d + 21
    a, c = a1, c1
root.mainloop()
print(clicked)
