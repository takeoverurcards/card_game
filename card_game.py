from tkinter import *
from math import *

class card():
    def __init__(self,name,power,health,tribe,main,aux,mfx,afx):
        self.name = name
        self.power = power
        self.health = health
        self.tribe = tribe
        self.main = main
        self.aux = aux
        self.mfx = mfx
        self.afx = afx

    def setcard():
        pass

table = Tk()
for i in range(20):
    Label(table, width=15, height=10, relief=RAISED).grid(row=i%4+1, column=floor(i/4))
        
table.mainloop()
