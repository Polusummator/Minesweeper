from tkinter import *
import random
import sys
import _tkinter


def click(event):
    global z
    if z:
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
                    clicked.add(ids)
                    if clicked & WITHOUT_BOMBS == WITHOUT_BOMBS:
                        z = False
                        Victory()
                elif GRID[i2][j2] == 0:
                    zero(ids)
                elif GRID[i2][j2] == -1:
                    canvas.itemconfig(CURRENT, fill='red')
                    los_num = ids
                    for i in MINES_NUM:
                        if i != ids:
                            canvas.itemconfig(i, fill='brown')
                    z = False
                    loss()
                clicked.add(ids)
        else:
            pass
    else:
        pass
    
    
def Victory():
    global root2
    root2 = Tk()
    root2.resizable(0, 0)
    root2.title('Victory')
    x = (root2.winfo_screenwidth() // 2) - (200 // 2)
    y = (root2.winfo_screenheight() // 2) - (130 // 2)
    root2.geometry('{}x{}+{}+{}'.format(200, 130, x, y))
    # root2.geometry('200x130+650+300')
    lab = Label(root2, text='You win!', font='Fixedays 18', fg='brown')
    but1 = Button(root2, width=10, text='Reset ►', bg='blue', fg='white', font='Fixedays 12')
    but2 = Button(root2, width=8, text='Exit', bg='green', fg='white', font='Fixedays 12')
    lab.pack()
    but1.pack(pady=10)
    but1.bind('<Button-1>', Reset)
    but2.pack(pady=9)
    but2.bind('<Button-1>', Exit)
    root2.mainloop()


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
            

def Exit(event):
    sys.exit(0)
    

def Reset(event):
    z = True
    root.destroy()
    try:
        root2.destroy()
    except NameError:
        pass
    except _tkinter.TclError:
        pass
    try:
        root1.destroy()
    except NameError:
        pass
    except _tkinter.TclError:
        pass
    main()

   
def loss():
    global root1
    root1 = Tk()
    root1.resizable(0, 0)
    root1.title('Loss')
    x = (root1.winfo_screenwidth() // 2) - (200 // 2)
    y = (root1.winfo_screenheight() // 2) - (130 // 2)
    root1.geometry('{}x{}+{}+{}'.format(200, 130, x, y))
    # root1.geometry('200x130+690+350')
    lab = Label(root1, text='You lose!', font='Fixedays 18', fg='brown')
    but1 = Button(root1, width=10, text='Reset ►', bg='blue', fg='white', font='Fixedays 12')
    but2 = Button(root1, width=8, text='Exit', bg='green', fg='white', font='Fixedays 12')
    lab.pack()
    but1.pack(pady=10)
    but1.bind('<Button-1>', Reset)
    but2.pack(pady=9)
    but2.bind('<Button-1>', Exit)
    root1.mainloop()
        

def nice_print(matrix):
    for i in range(len(matrix)):
        print(*matrix[i])


def ok(event):
    global varr
    varr = var.get()
    root3.destroy()


def exit_level(event):
    root3.destroy()
    sys.exit(0)
    

def level():
    global var, varr, root3
    root3 = Tk()
    x = (root3.winfo_screenwidth() // 2) - (400 // 2)
    y = (root3.winfo_screenheight() // 2) - (280 // 2)
    root3.geometry('{}x{}+{}+{}'.format(400, 280, x, y))
    # center(root3, 400, 280)
    # root3.geometry('400x280')
    root3.title('Level')
    root3.resizable(0, 0)
    lab = Label(root3, text='Select difficulty level', font='Fixedays 18', fg='brown')
    lab.pack()
    var = IntVar()
    var.set(2)
    varr = 2
    rbutton1 = Radiobutton(root3, text='BEGINNER            Field: 9х9 Mines: 10', font='Arial 12', variable=var, value=1)
    rbutton2 = Radiobutton(root3, text='MEDIUM                 Field: 12х12 Mines: 30', font='Arial 12', variable=var, value=2)
    rbutton3 = Radiobutton(root3, text='MASTER                Field: 16х16 Mines: 40', font='Arial 12', variable=var, value=3)
    rbutton4 = Radiobutton(root3, text='PROFESSIONAL  Field: 30х30 Mines: 150', font='Arial 12', variable=var, value=4)
    rbutton5 = Radiobutton(root3, text='GENIUS                  Field: 40х40 Mines: 300', font='Arial 12', variable=var, value=5)
    rbutton6 = Radiobutton(root3, text='SPECIAL                Create your level', font='Arial 12', variable=var, value=6)
    but = Button(root3, text='Ok', width=3, font='Fixedays 12', fg='white', bg='green')
    ex = Button(root3, text='Exit', width=4, font='Fixedays 12', fg='white', bg='blue')
    rbutton1.place(x=10, y=40)
    rbutton2.place(x=10, y=70)
    rbutton3.place(x=10, y=100)
    rbutton4.place(x=10, y=130)
    rbutton5.place(x=10, y=160)
    rbutton6.place(x=10, y=190)
    but.place(x=140, y=240)
    ex.place(x=200, y=240)
    ex.bind('<Button-1>', exit_level)
    but.bind('<Button-1>', ok)
    root3.mainloop()


def pr_ok(event):
    global SQUARES, MINES
    l_m = int(str(list_mines.curselection())[1:-2])
    l_f = int(str(list_field.curselection())[1:-2])
    s_m = int(l_mines[l_m])
    s_f = int(l_field[l_f].split('x')[0]) ** 2
    if s_m > s_f:
        lab.config(text='Mines more than cells!')
    else:
        SQUARES = s_f
        MINES = s_m
        root4.destroy()
        
        
def center1(win, r, height, width):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    if r:
        y = 0
    else:
        y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    
def center(win, width, height):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        

def main():
    global root, clicked, SQUARE_SIZE, SQUARES, flags, GRID, MINES_NUM, MINES, z, canvas, WITHOUT_BOMBS, zz, l_field, l_mines, list_field, list_mines, lab, root4
    zz = True
    sys.setrecursionlimit(500000)
    level()
    if varr == 1:
        SQUARES = 81
        MINES = 10
    elif varr == 2:
        SQUARES = 144
        MINES = 30
    elif varr == 3:
        SQUARES = 256
        MINES = 40
    elif varr == 4:
        SQUARES = 900
        MINES = 150
    elif varr == 5:
        SQUARES = 1600
        MINES = 300
    elif varr == 6:
        root4 = Tk()
        root4.title('Create level')
        # root4.geometry('400x300')
        x = (root4.winfo_screenwidth() // 2) - (400 // 2)
        y = (root4.winfo_screenheight() // 2) - (300 // 2)
        root4.geometry('{}x{}+{}+{}'.format(400, 300, x, y))
        # center(root4, 400, 300)
        # root4.geometry('400x300+650+300')
        root4.resizable(0, 0)
        l_mines = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110', '120', '130', '140', '150',
                   '160', '170', '180', '190', '200', '210', '220', '230', '240', '250', '260', '270', '280', '290',
                   '300']
        l_field = ['9x9', '10x10', '11x11', '12x12', '13x13', '14x14', '15x15', '16x16', '17x17', '18x18', '19x19',
                   '20x20', '21x21', '22x22', '23x23', '24x24', '25x25', '26x26', '27x27', '28x28', '29x29', '30x30',
                   '31x31', '32x32', '33x33', '34x34', '35x35', '36x36', '37x37', '38x38', '39x39', '40x40']
        lab = Label(root4, text='Create your level', font='Fixedays 18', fg='brown')
        lab_mines = Label(root4, text='Select number of mines', font='Fixedays 12', fg='brown')
        lab_field = Label(root4, text='Select the size of the field', font='Fixedays 12', fg='brown')
        lab_ps = Label(root4, text='* you can scroll through the lists', font='Fixedays 9 italic', fg='AntiqueWhite4')
        ok = Button(root4, text='Ok', font='Fixedays 10', fg='white', bg='green', width=10)
        ex = Button(root4, text='Exit', font='Fixedays 10', fg='white', bg='blue')
        list_mines = Listbox(exportselection=False)
        list_field = Listbox(exportselection=False)
        for m in l_mines:
            list_mines.insert(END, m)
        for f in l_field:
            list_field.insert(END, f)
        lab_mines.place(x=10, y=50)
        lab_field.place(x=200, y=50)
        list_mines.place(x=30, y=80)
        list_field.place(x=230, y=80)
        lab.pack()
        ok.place(x=143, y=250)
        ex.place(x=15, y=10)
        ex.bind('<Button-1>', Exit)
        ok.bind('<Button-1>', pr_ok)
        lab_ps.place(x=210, y=277)
        root4.mainloop()
    root = Tk()
    root.resizable(0, 0)
    z = True
    clicked = set()
    flags = set()
    r = []
    root.title('Minesweeper')
    SQUARE_SIZE = 20
    MINES_NUM = set(random.sample(range(1, SQUARES + 1), MINES))
    ALL_SQUARES = set(range(1, SQUARES + 1))
    WITHOUT_BOMBS = ALL_SQUARES.difference(MINES_NUM)
    size = int(SQUARES ** 0.5) * 21
    GRID = list([0] * int(SQUARES ** 0.5) for i in range(int(SQUARES ** 0.5)))
    for i in MINES_NUM:
        k = i - 1
        i1, j1 = k // len(GRID), k % len(GRID)
        GRID[i1][j1] = -1
    check_bombs()
    # root.geometry(str(size) + 'x' + str(size))
    r = int(SQUARES ** 0.5) > 37
    x = (root.winfo_screenwidth() // 2) - (size // 2)
    if r:
        y = 0
    else:
        y = (root.winfo_screenheight() // 2) - (size // 2)
    root.geometry('{}x{}+{}+{}'.format(size, size, x, y))
    # center1(root, r, size, size)
    # root.geometry(str(size) + 'x' + str(size) + aaa)
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


main()
