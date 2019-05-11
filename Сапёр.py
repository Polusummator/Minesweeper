from tkinter import *
import random
import sys


def click(event):
    global canvas
    ids = canvas.find_withtag(CURRENT)[0]
    if ids not in clicked and ids not in flags:
        try:
            x1, y1, x2, y2 = canvas.coords(ids)
        except ValueError:
            pass
        else:
            i2, j2 = (ids - 1) // len(GRID), (ids - 1) % len(GRID)
            if GRID[i2][j2] != -1 and GRID[i2][j2] != 0:
                canvas.itemconfig(CURRENT, fill='green')
                canvas.create_text(x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2, text=str(GRID[i2][j2]), font='Arial {}'.format(int(SQUARE_SIZE / 2)), fill='yellow')
            elif GRID[i2][j2] == 0:
                zero(ids)
            elif GRID[i2][j2] == -1:
                canvas.itemconfig(CURRENT, fill='red')
            clicked.add(ids)
    else:
        pass


def generate_neighbors(ids):
    i, j = (ids - 1) // int(SQUARES ** 0.5), (ids - 1) % int(SQUARES ** 0.5)
    if i == 0 and j == 0:
        l = {(0, 1), (1, 1), (1, 0)}
    elif i == 0 and j == len(GRID) - 1:
        l = {(0, len(GRID) - 2), (1, len(GRID) - 2), (1, len(GRID) - 1)}
    elif i == len(GRID) - 1 and j == 0:
        l = {(len(GRID) - 1, 1), (len(GRID) - 2, 0), (len(GRID) - 2, 1)}
    elif i == len(GRID) - 1 and j == len(GRID) - 1:
        l = {(len(GRID) - 1, len(GRID) - 2), (len(GRID) - 2, len(GRID) - 2), (len(GRID) - 2, len(GRID) - 1)}
    elif i == 0:
        l = {(0, j - 1), (0, j + 1), (1, j - 1), (1, j), (1, j + 1)}
    elif i == len(GRID) - 1:
        l = {(len(GRID) - 1, j - 1), (len(GRID) - 1, j + 1), (len(GRID) - 2, j - 1), (len(GRID) - 2, j), (len(GRID) - 2, j + 1)}
    elif j == 0:
        l = {(i - 1, 0), (i + 1, 0), (i - 1, 1), (i, 1), (i + 1, 1)}
    elif j == len(GRID) - 1:
        l = {(i - 1, len(GRID) - 1), (i - 1, len(GRID) - 2), (i, len(GRID) - 2), (i + 1, len(GRID) - 2), (i + 1, len(GRID) - 1)}
    else:
        l = {(i - 1, j - 1), (i, j - 1), (i + 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1),
             (i + 1, j + 1), (i + 1, j)}
    ll = set()
    for i3 in l:
        s = i3[0] * int(SQUARES ** 0.5) + i3[1] + 1
        ll.add(s)
    return ll


def check_bombs():
    for i in range(len(GRID)):
        for j in range(len(GRID)):
            if GRID[i][j] != -1:
                s = 0
                if i == 0 and j == 0:
                    l = [GRID[0][1], GRID[1][1], GRID[1][0]]
                elif i == 0 and j == len(GRID) - 1:
                    l = [GRID[0][-2], GRID[1][-2], GRID[1][-1]]
                elif i == len(GRID) - 1 and j == 0:
                    l = [GRID[-1][1], GRID[-2][0], GRID[-2][1]]
                elif i == len(GRID) - 1 and j == len(GRID) - 1:
                    l = [GRID[-1][-2], GRID[-2][-2], GRID[-2][-1]]
                elif i == 0:
                    l = [GRID[0][j - 1], GRID[0][j + 1], GRID[1][j - 1], GRID[1][j], GRID[1][j + 1]]
                elif i == len(GRID) - 1:
                    l = [GRID[-1][j - 1], GRID[-1][j + 1], GRID[-2][j - 1], GRID[-2][j], GRID[-2][j + 1]]
                elif j == 0:
                    l = [GRID[i - 1][0], GRID[i + 1][0], GRID[i - 1][1], GRID[i][1], GRID[i + 1][1]]
                elif j == len(GRID) - 1:
                    l = [GRID[i - 1][-1], GRID[i - 1][-2], GRID[i][-2], GRID[i + 1][-2], GRID[i + 1][-1]]
                else:
                    l = [GRID[i - 1][j - 1], GRID[i][j - 1], GRID[i + 1][j - 1], GRID[i - 1][j], GRID[i - 1][j + 1], GRID[i][j + 1], GRID[i + 1][j + 1], GRID[i + 1][j]]
                s = l.count(-1)
                GRID[i][j] = s


def flag(event):
    ids = canvas.find_withtag(CURRENT)[0]
    if ids not in clicked:
        if ids not in flags:
            canvas.itemconfig(CURRENT, fill='yellow')
            flags.add(ids)
        else:
            canvas.itemconfig(CURRENT, fill='AntiqueWhite4')
            flags.remove(ids)
    else:
        pass


def zero(id):
    canvas.itemconfig(id, fill='green')
    clicked.add(id)
    neighbors = generate_neighbors(id)
    for item in set(neighbors).difference(clicked):
        ii, jj = (item - 1) // int(SQUARES ** 0.5), (item - 1) % int(SQUARES ** 0.5)
        if GRID[ii][jj] == 0:
            zero(item)
        else:
            x1, y1, x2, y2 = canvas.coords(item)
            canvas.itemconfig(item, fill='green')
            canvas.create_text(x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2, text=str(GRID[ii][jj]),
                           font='Arial {}'.format(int(SQUARE_SIZE / 2)), fill='yellow')
            clicked.add(item)
        

def nice_print(matrix):
    for i in range(len(matrix)):
        print(*matrix[i])


sys.setrecursionlimit(500000)
root = Tk()
clicked = set()
flags = set()
r = []
root.title('Сапёр')
SQUARES = 256
SQUARE_SIZE = 20
MINES = 40
MINES_NUM = set(random.sample(range(1, 16**2+1), 40))
size = int(SQUARES ** 0.5) * 21
GRID = list([0] * int(SQUARES ** 0.5) for i in range(int(SQUARES ** 0.5)))
for i in MINES_NUM:
    k = i - 1
    i1, j1 = k // len(GRID), k % len(GRID)
    GRID[i1][j1] = -1
print(MINES_NUM)
check_bombs()
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
        canvas.bind('<Button-3>', flag)
        a, c = a + 21, c + 21
    b, d = b + 21, d + 21
    a, c = a1, c1
root.mainloop()
print(clicked)
