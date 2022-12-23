from tkinter import *
#from math import *

from card_class import *

table = Tk()

slots = [0,1,2,3,4,5,7,9,10,11,13,14,16,17,18,20,22,23,24,25,26,27]
cards = []

for i in slots:
    Label(table, width=15, height=10, relief=SUNKEN).grid(row=int(i/7), column=i%7)
for num in range(1,23):
    cards.append(Label(table, width=13, height=9, relief=RAISED, text=num))

[m11,m12,m13,m21,m22,m23,a11,a12,a13,a14,a15,a21,a22,a23,a24,a25,n1,n2,g1,g2,d1,d2] = cards
cards = [m11,m12,m13,m21,m22,m23,a11,a12,a13,a14,a15,a21,a22,a23,a24,a25,n1,n2,g1,g2,d1,d2]

for i in range(22):
    cards[i].grid(row=int(slots[i]/7), column=slots[i]%7)

table.mainloop()
