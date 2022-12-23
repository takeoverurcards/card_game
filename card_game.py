from tkinter import *
from math import *
from card_class import *
from json_decoder import *

table = Tk()
table.resizable(width=0,height=0)
table.configure(bg="black")
table.geometry("777x850")
frame = Frame(table, pady=113, bg="black")
frame.pack()

slots = [0,1,2,3,4,5,7,9,10,11,13,14,16,17,18,20,22,23,24,25,26,27]

for i in slots:
    Label(frame, bg="grey", width=15, height=10, relief=SUNKEN).grid(row=floor(i/7), column=i%7)

cards = []

for i in range(1,23):
    cards.append(Label(frame, width=13, height=9, relief=RAISED, text=i, wraplength=100, justify="center"))

[m11,m12,m13,m21,m22,m23,a11,a12,a13,a14,a15,a21,a22,a23,a24,a25,n1,n2,g1,g2,d1,d2] = cards

cards = [m11,m12,m13,m21,m22,m23,a11,a12,a13,a14,a15,a21,a22,a23,a24,a25,n1,n2,g1,g2,d1,d2]

for i in range(22):
    cards[i].grid(row=floor(slots[i]/7), column=slots[i]%7)

m11.config(text=decode_card("0001").name)
m12.config(text=decode_card("0002").name)
m13.config(text=decode_card("0003").name)

def info(x):
    global card_info
    card_info = Label(justify="left",text=decode_card(x).name+"\ncost: "+
          str(decode_card(x).cost)+"\npower: "+
          str(decode_card(x).power)+"\nhealth: "+
          str(decode_card(x).health)+"\ntribe: "+
          decode_card(x).tribe+"\nmain: "+
          decode_card(x).main+"\naux: "+
          decode_card(x).aux+"\nmfx: "+
          decode_card(x).mfx+"\nmfx_turn: "+
          str(decode_card(x).mfx_turn)+"\nafx: "+
          decode_card(x).afx+"\nafx_turn: "+
          str(decode_card(x).afx_turn)+"\nefx: "+
          decode_card(x).efx+"\nefx_turn: "+
          str(decode_card(x).efx_turn))

def show():
    card_info.place(x=table.winfo_pointerx() - table.winfo_rootx(),y=table.winfo_pointery() - table.winfo_rooty())
def hide():
    card_info.place_forget()

info("0001")
m11.bind("<Button-1>", lambda i:[hide(),info("0001"),show()])
m12.bind("<Button-1>", lambda i:[hide(),info("0002"),show()])
m13.bind("<Button-1>", lambda i:[hide(),info("0003"),show()])
frame.bind("<Button-1>", lambda i:hide())
table.mainloop()
