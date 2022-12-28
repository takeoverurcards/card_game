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
g1 = []
g2 = []
d1 = []
d2 = []
h1 = {}
h2 = {}
card_slots = {}
p1_health = p2_health = 3
player_turn = 0

m1_1 = m2_1 = m3_1 = m1_2 = m2_2 = m3_2 = a1_1 = a2_1 = a3_1 = a4_1 = a5_1 = a1_2 = a2_2 = a3_2 = a4_2 = a5_2 = n1 = n2 = ""

m11_info = m12_info = m13_info = m21_info = m22_info = m23_info = a11_info = a12_info = a13_info = a14_info = a15_info = a21_info = a22_info = a23_info = a24_info = a25_info = n1_info = n2_info = ""

cards = [m1_1,m2_1,m3_1,m1_2,m2_2,m3_2,a1_1,a2_1,a3_1,a4_1,a5_1,a1_2,a2_2,a3_2,a4_2,a5_2,n1,n2]

cards_info = [m11_info,m12_info,m13_info,m21_info,m22_info,m23_info,a11_info,a12_info,a13_info,a14_info,a15_info,a21_info,a22_info,a23_info,a24_info,a25_info,n1_info,n2_info]    

for i in range(len(slots)):
    cards[i] = Label(frame, name="slot_"+str(i).zfill(2), width=15, height=10, relief=SUNKEN, wraplength=100, justify="center")
    cards[i].grid(row=floor(slots[i]/7), column=slots[i]%7)
    cards[i].bind("<Button-1>", lambda z:play_card(z.widget))

for i in json.load(open("card_master_list.json", "r"))["Cards"]:
    d1.append(i)

shuffle(d1)

draw_count = play_var = 0
selected_card = ""

def draw(x):
    global draw_count
    h1[str(draw_count).zfill(3)+"_"+d1[x]] = Label(frame2, name="1_"+str(draw_count).zfill(3)+"_"+d1[x], width=13, height=4, relief=RAISED, text=decode_card(d1[x]).name, wraplength=90, justify="center")
    h1[list(h1)[-1]].grid(row=0,column=draw_count)
    draw_count += 1
    h1[list(h1)[-1]].bind("<Button-1>", lambda z:select_card(z.widget))
    h1[list(h1)[-1]].bind("<Button-3>", lambda z:[hide_info(),info(str(z.widget)[-4:]),show_info()])
    d1.pop(x)

def select_card(x):
    global selected_card, play_var
    if selected_card:
        selected_card.config(relief=RAISED,bg="white")
    selected_card = x
    x.config(relief=RIDGE,bg="yellow")
    play_var = 1
    hide_info()
    for i in [0,1,2,4,5,6,7,8]:
        if decode_card(str(selected_card)[-4:]).tribe.lower() != "item" and not cards_info[(len(cards)>>1)+i]:
            cards[(len(cards)>>1)+i].config(bg="orange")

def play_card(x):
    global selected_card, play_var
    if play_var and decode_card(str(selected_card)[-4:]).tribe.lower() != "item" and int(str(x)[-2:]) in [9,10,11,13,14,15,16,17] and not cards_info[int(str(x)[-2:])]:
        cards_info[int(str(x)[-2:])] = str(selected_card)[-4:]
        h1[str(selected_card)[-8:]].grid_forget()
        del h1[str(selected_card)[-8:]]
        hide_info()
        update_field()
        play_var = 0
        for i in range(len(cards_info)):
            if not cards_info[i]:
                cards[i].config(bg="gray")

card_info = Label(table, justify="left")

def info(x):
    global card_info
    if x:
        card_info.config(text=decode_card(x).name+"\ncost: "+
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
    else:
        hide_info()

def show_info():
    card_info.place(x=table.winfo_pointerx() - table.winfo_rootx(),y=table.winfo_pointery() - table.winfo_rooty())

def hide_info():
    card_info.place_forget()

def update_field():
    for i in range(len(cards_info)):
        if cards_info[i]:
            cards[i].config(bg="white", relief=RAISED, text=decode_card(cards_info[i]).name)
        else:
            cards[i].config(bg="grey", relief=SUNKEN)
    table.update_idletasks()

update_field()

#info("0001")
table.bind('<Return>',lambda z:draw(0))
for i in range(len(cards)):
    cards[i].bind("<Button-3>", lambda z:[hide_info(),info(cards_info[int(str(z.widget)[-2:])]),show_info() if (z.widget["text"]) else hide_info()])
frame.bind("<Button-3>", lambda z:hide_info())

table.mainloop()
