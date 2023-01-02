#importing modules
from tkinter import *
from card_class import *
from json_decoder import *
from random import shuffle, randint, choice
from runpy import run_path

#setting up playing area
table = Tk() #main window
table.title("[INSERT CARD GAME NAME HERE] by Take, Zoop, and Elite")
#table.geometry("777x976+0+0")
table.resizable(0,0) #prevents manual window resizing
table.config(bg="black")
frame = Frame(table, pady=30, bg="black") #main widget for slots
frame_p2 = Frame(table, bg="black")
frame_p1 = Frame(table, bg="black")
info_frame = Frame(table, height=60)
end_frame = Frame(table, relief=SUNKEN, width=100, height=70)
info_frame.pack_propagate(False)
end_frame.pack_propagate(False)
for i in [frame_p2,frame,frame_p1,info_frame,end_frame]:
    i.pack(side=LEFT) if i == info_frame else i.pack()
end_btn = Button(end_frame, width=9, height=2, text="END TURN", font=("Segoe UI",12), command=lambda:end_turn())
p1_health = Label(frame, bg="black", fg="white", text="3", font=("Britannic Bold",48))
p2_health = Label(frame, bg="black", fg="white", text="3", font=("Britannic Bold",48))
p1_health.grid(row=3,column=0)
p2_health.grid(row=0,column=6)

#initializing variables
slots = [1,2,3,4,5,7,9,10,11,16,17,18,20,22,23,24,25,26] #numbers indicating grid locations for all card slots
g1 = [] #graveyard of player 1
g2 = [] #graveyard of player 2
h1 = {} #hand of player 1
h2 = {} #hand of player 2
player_turn = 0 #turn of indicated player
p1_draw_count = p2_draw_count = 0 #number of cards drawn for respective player
selected_card = ""
card_info = Label(info_frame, justify="left", height=100) #card information textbox
cards = [Label(frame, name="slot_"+str(i).zfill(2), width=12, height=8, wraplength=60, justify="center") for i in range(18)] #list containing all card slots
cards_info = ["" for i in range(18)] #list containing all card slot information
d1_lbl = Label(frame, bg="brown", relief=RAISED, width=12, height=8)
d2_lbl = Label(frame, bg="brown", relief=RAISED, width=12, height=8)
d1_lbl.grid(row=2,column=0)
d2_lbl.grid(row=1,column=6)

#creating card slots
for i,j in enumerate(slots):
    cards[i].grid(row=int(j/7), column=j%7)
    cards[i].bind("<Button-1>", lambda z:select_card(a) if (a := z.widget)["text"] and int(str(a)[-2:]) in [9,10,11] else [play_card(a),attack(a)])
for i in range(6,12):
    cards[i].can_atk = 0

#loading current decks
d1 = [f"{i}_{decode_card(i).power}_{decode_card(i).health}" for i in json.load(open("card_master_list.json", "r"))["Cards"]]
d2 = [f"{i}_{decode_card(i).power}_{decode_card(i).health}" for i in json.load(open("card_master_list.json", "r"))["Cards"]]

#creating gameplay functions
###draw a card from player 1's deck to their hand
def draw_p1(x):
    global p1_draw_count
    if d1:
        h1[str(p1_draw_count).zfill(3)+"_"+d1[x][:4]] = Label(frame_p1, bg="white", name="1_"+str(p1_draw_count).zfill(3)+"_"+d1[x], width=12, height=4, relief=RAISED, text=decode_card(d1[x][:4]).name, wraplength=80, justify="center")
        h1[list(h1)[-1]].grid(row=0,column=p1_draw_count)
        p1_draw_count += 1
        h1[list(h1)[-1]].bind("<Button-1>", lambda z:select_card(z.widget) if player_turn == 1 else ())
        h1[list(h1)[-1]].bind("<Button-3>", lambda z:[card_info.pack_forget(),info(str(z.widget)[-8:]),card_info.pack()] if player_turn == 1 else card_info.pack_forget())
        d1.pop(x)
        update_field()

###draw a card from player 2's deck to their hand
def draw_p2(x):
    global p2_draw_count
    if d2:
        h2[str(p2_draw_count).zfill(3)+"_"+d2[x][:4]] = Label(frame_p2, bg="brown", name="2_"+str(p2_draw_count).zfill(3)+"_"+d2[x][:4], width=12, height=3, relief=RAISED)
        h2[list(h2)[-1]].grid(row=0,column=p2_draw_count)
        p2_draw_count += 1
        d2.pop(x)
        update_field()

###select a card to play from the hand
def select_card(x):
    update_field()
    global selected_card
    if selected_card:
        selected_card.config(relief=RAISED, bg="white")
    if x in h1.values():
        selected_card = x
        x.config(relief=RIDGE, bg="yellow")
        card_info.pack_forget()
        for i in [9,10,11,13,14,15,16,17]:
            cards[i].config(bg="orange") if not cards_info[i] else ()
    elif x.can_atk:
        selected_card = x
        x.config(relief=RIDGE, bg="yellow")
        card_info.pack_forget()
        for i in range(6,9):
            cards[i].config(bg="orange") if cards_info[i] else ()

###play selected card
def play_card(x):
    global selected_card
    if x["bg"] == "orange" and selected_card in h1.values():
        cards_info[int(str(x)[-2:])] = str(selected_card)[-8:]
        x.can_atk = 1
        h1[str(selected_card)[-12:-4]].grid_forget()
        del h1[str(selected_card)[-12:-4]]
        card_info.pack_forget()
        update_field()

def attack(x):
    global selected_card
    if x["bg"] == "orange":
        a = cards_info[int(str(x)[-2:])]
        b = int(cards_info[int(str(selected_card)[-2:])][5])
        if b >= int(a[-1]):
            cards_info[int(str(x)[-2:])] = ""
        else:
            cards_info[int(str(x)[-2:])] = a[:-1]+str(int(a[-1])-b)
        selected_card.can_atk = 0
        update_field()
    
def end_turn():
    global player_turn, end_btn
    player_turn = 3 - player_turn
    end_btn.pack_forget() if player_turn == 2 else end_btn.pack(expand=YES)
    for i in cards:
        if i["bg"] == "orange":
            i.config(bg="grey")
    for i in h1.values():
        if i["bg"] == "yellow":
            i.config(relief=RAISED, bg="white")
    selected_card = ""
    info("")
    update_field()

###update card information textbox
def info(x):
    global card_info
    newline = "\n"
    card_info.pack_forget() if not (a := x[:4]) else card_info.config(text=(f"{(b := decode_card(a)).name}"
                    f"   [{x[5]} / {x[7]}]"
                    f"   ({b.main}"
                    f"{' / '+b.aux+')' if b.aux else ')'}"
                    f"   {b.tribe.upper()}   Cost: {str(b.cost)}"
                    f"{newline+'Main effect: '+b.mfx if b.mfx else ''}"
                    f"{newline+'Aux effect: '+b.afx if b.afx else ''}"
                    f"{newline+'Equip effect: '+b.efx if b.efx else ''}"
                    ), width=info_frame.winfo_width(), wraplength=info_frame.winfo_width(), font=("Segoe UI", 8))

###update visuals of all slots
def update_field():
    for i,j in enumerate(cards_info):
        if j:
            cards[i].config(bg="white", relief=RAISED, text=f"{decode_card(j[:4]).name}\n\n{j[5]} / {j[7]}")
        else:
            cards[i].config(bg="grey", relief=SUNKEN, text="")
    d1_lbl.config(bg="brown", relief=RAISED) if d1 else d1_lbl.config(bg="grey", relief=SUNKEN)
    d2_lbl.config(bg="brown", relief=RAISED) if d2 else d2_lbl.config(bg="grey", relief=SUNKEN)
    table.update_idletasks()

#adding card information textbox functionality
frame.bind("<Button-3>", lambda z:card_info.pack_forget())
for i in cards:
    i.bind("<Button-3>", lambda z:[card_info.pack_forget(), info(cards_info[int(str(z.widget)[-2:])]), card_info.pack() if (z.widget["text"]) and player_turn == 1 else card_info.pack_forget()])

#occupying starting hands
shuffle(d1)
for i in range(5):
    draw_p1(0)
    draw_p2(0)

#initiating first turn
player_turn = 2
end_btn.pack_forget() if player_turn == 2 else end_btn.pack(expand=YES)

#DEBUGGING ONLY
d1_lbl.bind("<Button-1>",lambda z:(draw_p1(0)))
table.bind("<Escape>",lambda z:[table.destroy(),run_path('start_menu.py')])
c = [0,1,2,3,4,6,7,8]
for i in range(5):
    a = choice(c)
    b = choice(d2)
    cards_info[a] = b
    c.remove(a)
    d2.remove(b)
update_field()
end_turn()
info_frame["width"] = int(table.winfo_width()) - int(end_frame.winfo_width())
info_frame["height"] = int(end_frame.winfo_height())

#executing game
table.mainloop()
