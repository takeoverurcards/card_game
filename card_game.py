#importing modules
from tkinter import *
from card_class import *
from json_decoder import *
from random import shuffle, choice
from card_functions import *

#initialize card functions file
exec(open("./card_functions.py").read())

#setting up playing area
table = Tk() #main window
table.title("[INSERT CARD GAME NAME HERE] by Take, Zoop, and Elite")
table.resizable(0,0) #prevents manual window resizing
table.config(bg="black")
frame = Frame(table, pady=30, bg="black") #main widget for slots
frame_p1 = Frame(table, bg="black") #frame for player 1's hand
frame_p2 = Frame(table, bg="black") #frame for player 2's hand
info_frame = Frame(table, height=100) #frame for card_info
end_frame = Frame(table, relief=SUNKEN, width=100, height=70) #frame for end_btn
info_frame.pack_propagate(False) #prevent frame resizing due to child widgets
end_frame.pack_propagate(False)
for i in [frame_p2,frame,frame_p1,info_frame,end_frame]:
    i.pack(side=LEFT) if i == info_frame else i.pack()
end_btn = Button(end_frame, width=9, height=2, text="END TURN", font=("Segoe UI",12), command=lambda:end_turn())
p1_health = Label(frame, bg="black", fg="white", text="3", font=("Britannic Bold",48)) #player 1's hit points
p2_health = Label(frame, bg="black", fg="white", text="3", font=("Britannic Bold",48)) #player 2's hit points
p1_health.grid(row=3,column=0)
p2_health.grid(row=0,column=6)
d1_lbl = Label(frame, bg="brown", relief=RAISED, width=12, height=8) #label representing player 1's deck
d2_lbl = Label(frame, bg="brown", relief=RAISED, width=12, height=8) #label representing player 2's deck
d1_lbl.grid(row=2,column=0)
d2_lbl.grid(row=1,column=6)

#initializing variables
p2_auxes,p2_mains,p1_mains,p1_auxes = [*range(5)],[*range(5,8)],[*range(8,11)],[*range(11,16)] #variables for card slots
slots = [*[x+1 for x in p2_auxes],
         *[x+4 for x in p2_mains],
         *[x+8 for x in p1_mains],
         *[x+11 for x in p1_auxes]] #list of all slot positions
g1,g2,h1,h2 = [],[],{},{} #graveyards and hands of players 1 and 2, respectively
player_turn = 0 #turn of indicated player
p1_draw_count = p2_draw_count = 0 #number of cards drawn for respective player
card_info = Label(info_frame, justify="left", height=100) #card information textbox
cards = [Label(frame, name="slot_"+str(i).zfill(2), width=12, height=8, justify="center") for i in range(16)] #list containing all card slots
cards_info = [(selected_card := "") for i in range(16)] #list containing all card slot information

#creating card slots
for i,j in enumerate(slots):
    cards[i].grid(row=j//7, column=j%7)
    cards[i].bind("<Button-1>", lambda z:
                  play_card(a) if not (a := z.widget)["text"] else
                  attack(a) if slot_num(a) in p2_mains else
                  select_card(a) if slot_num(a) not in p2_auxes else ())
for i in [*p2_mains,*p1_mains]:
    cards[i].can_atk = 0 #new attribute for main cards indicating ability to call an attack

#loading current decks
d1 = [f"{i}_{decode_card(i).power}_{decode_card(i).health}" for i in json.load(open("card_master_list.json", "r"))["Cards"]]
d2 = [f"{i}_{decode_card(i).power}_{decode_card(i).health}" for i in json.load(open("card_master_list.json", "r"))["Cards"]]

###update card information textbox
def info(x):
    global card_info
    newline = "\n"
    card_info.pack_forget() if not x else [card_info.config(text=(f"{(a := decode_card(x[:4])).name}"
                    f"   [{x[5]} / {x[7]}]"
                    f"   ({a.main}"
                    f"{' / '+a.aux+')' if a.aux else ')'}"
                    f"   {a.tribe.upper()}   Cost: {str(a.cost)}"
                    f"{newline+'Main effect: '+a.mfx if a.mfx else ''}"
                    f"{newline+'Aux effect: '+a.afx if a.afx else ''}"
                    f"{newline+'Equip effect: '+a.efx if a.efx else ''}"
                    ), width=info_frame.winfo_width(), wraplength=info_frame.winfo_width(), font=("Segoe UI", 8)),card_info.pack()]
    card_info["wraplength"] = info_frame.winfo_width() - 10

###update visuals of all slots
def update_field():
    for i,j in enumerate(cards_info):
        cards[i].config(bg="white", relief=RAISED, text=f"{decode_card(j[:4]).name}\n\n{j[5]} / {j[7]}") if j else cards[i].config(bg="grey", relief=SUNKEN, text="")
    d1_lbl.config(bg="brown", relief=RAISED) if d1 else d1_lbl.config(bg="grey", relief=SUNKEN)
    d2_lbl.config(bg="brown", relief=RAISED) if d2 else d2_lbl.config(bg="grey", relief=SUNKEN)
    table.update_idletasks()

#adding card information textbox functionality
frame.bind("<Button-3>", lambda z:card_info.pack_forget())
for i in cards:
    i.bind("<Button-3>", lambda z:info(cards_info[slot_num(z.widget)]))

#occupying starting hands
shuffle(d1)
shuffle(d2)
for i in range(5):
    draw_p1(0)
    draw_p2(0)

#fixing label and frame attributes
info_frame["width"] = int(table.winfo_width()) - int(end_frame.winfo_width())
info_frame["height"] = int(end_frame.winfo_height())
for i in cards:
    i["wraplength"] = i.winfo_width() - 10
#for i in h1.values():
#    i["wraplength"] = i.winfo_width() - 10

#initiating first turn
player_turn = 2
end_btn.pack_forget() if player_turn == 2 else end_btn.pack(expand=YES)

#DEBUGGING ONLY
d1_lbl.bind("<Button-1>",lambda z:draw_p1(0) if player_turn == 1 else ())
table.bind("<Escape>",lambda z:[table.destroy(),run_path('start_menu.py')])
shuffle(c := list(range(8)))
while h2:
    selected_card = h2[choice(list(h2.keys()))]
    play_card(cards[c.pop(0)])
update_field()
end_turn()

#executing game
table.mainloop()
