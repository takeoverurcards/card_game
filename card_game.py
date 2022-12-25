from tkinter import *
from math import *
from card_class import *
from json_decoder import *
from random import *

table = Tk()
table.resizable(width=0,height=0)
table.configure(bg="black")
frame = Frame(table, pady=60, bg="black")
frame2 = Frame(table, bg="black")
frame.pack()
frame2.pack()

slots = [1,2,3,4,5,7,9,10,11,16,17,18,20,22,23,24,25,26]
g1 = g2 = d1 = d2 = []
h1 = h2 = {}

for i in slots:
    Label(frame, bg="grey", width=15, height=10, relief=SUNKEN).grid(row=floor(i/7), column=i%7)

m11 = m12 = m13 = m21 = m22 = m23 = a11 = a12 = a13 = a14 = a15 = a21 = a22 = a23 = a24 = a25 = n1 = n2 = Label(frame, width=13, height=9, relief=RAISED, text="", wraplength=100, justify="center")

m11_info = m12_info = m13_info = m21_info = m22_info = m23_info = a11_info = a12_info = a13_info = a14_info_info = a15_info = a21_info = a22_info = a23_info = a24_info = a25_info = n1_info = n2_info = ""

cards = [m11,m12,m13,m21,m22,m23,a11,a12,a13,a14,a15,a21,a22,a23,a24,a25,n1,n2]

cards_info = [m11_info, m12_info, m13_info, m21_info, m22_info, m23_info, a11_info, a12_info, a13_info, a14_info_info, a15_info, a21_info, a22_info, a23_info, a24_info, a25_info, n1_info, n2_info]    

for i in json.load(open("card_master_list.json", "r"))["Cards"]:
    d1.append(i)
    print(i)

shuffle(d1)

draw_count = 0

def draw(x):
    h1[d1[x]] = Label(frame2, name=d1[x], width=13, height=4, relief=RAISED, text=decode_card(d1[x]).name, wraplength=100, justify="center")
    global draw_count
    h1[list(h1)[-1]].grid(row=0,column=draw_count)
    draw_count += 1
    h1[list(h1)[-1]].bind("<Button-3>", lambda z:[hide_info(),info(str(z.widget)[-4:]),show_info()])
    d1.pop(x)

def info(x):
    global card_info
    card_info = Label(table, justify="left",text=decode_card(x).name+"\ncost: "+
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

def show_info():
    card_info.place(x=table.winfo_pointerx() - table.winfo_rootx(),y=table.winfo_pointery() - table.winfo_rooty())

def hide_info():
    card_info.place_forget()

def update_field():
    for i in range(len(cards_info)):
        if cards_info[i]:
            cards[i].grid(row=floor(slots[i]/7), column=slots[i]%7)
        else:
            cards[i].grid_forget()
    table.update_idletasks()

update_field()

info("0001")
table.bind('<Return>',lambda z:draw(0))
#for i in range(len(cards)):
#    cards[i].bind("<Button-3>", lambda z:[hide_info(),info(cards_info[i]),show_info()])
for i in range(len(h1)):
    h1[list(h1)[i]].grid(row=0,column=i)
frame.bind("<Button-3>", lambda z:hide_info())

table.mainloop()
