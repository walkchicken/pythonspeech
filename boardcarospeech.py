from tkinter import Button, Tk, Canvas, Frame,Label, BOTH
from tkinter.constants import LEFT
from typing import Text
from functools import partial


class Board(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def handleButton(self, x, y):
        if self.Buts[x, y]['text'] == "": #Kiểm tra ô có ký tự rỗng hay không
            print('x')

    def initUI(self):
        self.parent.title("CARO SPEECH :)))")
        self.pack(fill=BOTH, expand=1)

        for x in range(3):   # tạo ma trận button Ox * Oy
            for y in range(3):
                self.Buts[x, y] = Button( height=1, width=2,
                                            borderwidth=2, command=partial(self.handleButton, x=x, y=y))
                self.Buts[x, y].grid(row=x, column=y)


root = Tk()
ex = Board(root)
root.geometry("450x600+300+300")
# this removes the maximize button
root.resizable(0,0)
root.mainloop()