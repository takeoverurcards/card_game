#importing modules
from tkinter import *
from math import *
from card_class import *
from json_decoder import *
from random import *

#create game layout
def game():
    global p1_draw_count, p2_draw_count, card_info, selected_card, play_var
    #setting up playing area
    table = Tk() #main window
    table.title("[INSERT CARD GAME NAME HERE] by Take, Zoop, and Elite")
    table.geometry("777x976+0+0")
    table.resizable(0,0) #prevents manual window resizing
    table.config(bg="black")
    frame = Frame(table, pady=60, bg="black") #main widget for slots
    frame_p2 = Frame(table, bg="black", height=66)
    frame_p1 = Frame(table, bg="black", height=66)
    frame_p2.pack()
    frame.pack()
    frame_p1.pack()
    info_frame = Frame(table, width=777, height=100)
    info_frame.pack()
    p1_health = Label(frame, bg="black", fg="white", text="3", font=("Britannic Bold",48))
    p2_health = Label(frame, bg="black", fg="white",text="3", font=("Britannic Bold",48))
    p1_health.grid(row=3,column=0)
    p2_health.grid(row=0,column=6)

    #initializing variables
    slots = [1,2,3,4,5,7,9,10,11,16,17,18,20,22,23,24,25,26] #numbers indicating grid locations for all card slots
    g1 = [] #graveyard of player 1
    g2 = [] #graveyard of player 2
    d1 = [] #deck of player 1
    d2 = [] #deck of player 2
    h1 = {} #hand of player 1
    h2 = {} #hand of player 2
    player_turn = 0 #turn of indicated player
    p1_draw_count = p2_draw_count = 0 #number of cards drawn for respective player
    play_var = False #indicator for play_card()
    selected_card = ""
    card_info = Label(info_frame, justify="left", height=100) #card information textbox
    m11 = m21 = m31 = m12 = m22 = m32 = a11 = a21 = a31 = a41 = a51 = a12 = a22 = a32 = a42 = a52 = n1 = n2 = "" #all card labels on the field
    m11_info = m21_info = m31_info = m12_info = m22_info = m32_info = a11_info = a21_info = a31_info = a41_info = a51_info = a12_info = a22_info = a32_info = a42_info = a52_info = n1_info = n2_info = "" #all current cards on the field
    cards = [a12,a22,a32,a42,a52,n2,m12,m22,m32,m11,m21,m31,n1,a11,a21,a31,a41,a51] #list containing all card slots
    cards_info = [a12_info,a22_info,a32_info,a42_info,a52_info,n2_info,m12_info,m22_info,m32_info,m11_info,m21_info,m31_info,n1_info,a11_info,a21_info,a31_info,a41_info,a51_info] #list containing all card slot information
    d1_lbl = Label(frame, bg="brown", relief=RAISED, width=15, height=10)
    d2_lbl = Label(frame, bg="brown", relief=RAISED, width=15, height=10)
    d1_lbl.grid(row=2,column=0)
    d2_lbl.grid(row=1,column=6)
    d1_lbl.bind("<Button-1>", lambda z:draw_p1(0))
    
    #creating card slots
    for i in range(len(slots)):
        cards[i] = Label(frame, name="slot_"+str(i).zfill(2), width=15, height=10, bg="grey", relief=SUNKEN, wraplength=100, justify="center")
        cards[i].grid(row=floor(slots[i]/7), column=slots[i]%7)
        cards[i].bind("<Button-1>", lambda z:play_card(z.widget))

    #loading current decks
    for i in json.load(open("card_master_list.json", "r"))["Cards"]:
        d1.append(i)
    for i in json.load(open("card_master_list.json", "r"))["Cards"]:
        d2.append(i)

    #creating gameplay functions
    ###draw a card from player 1's deck to their hand
    def draw_p1(x):
        global p1_draw_count
        if d1:
            h1[str(p1_draw_count).zfill(3)+"_"+d1[x]] = Label(frame_p1, name="1_"+str(p1_draw_count).zfill(3)+"_"+d1[x], width=13, height=4, relief=RAISED, text=decode_card(d1[x]).name, wraplength=90, justify="center")
            h1[list(h1)[-1]].grid(row=0,column=p1_draw_count)
            p1_draw_count += 1
            h1[list(h1)[-1]].bind("<Button-1>", lambda z:select_card(z.widget))
            h1[list(h1)[-1]].bind("<Button-3>", lambda z:[hide_info(),info(str(z.widget)[-4:]),show_info()])
            d1.pop(x)
            update_field()

    ###draw a card from player 2's deck to their hand
    def draw_p2(x):
        global p2_draw_count
        if d2:
            h2[str(p2_draw_count).zfill(3)+"_"+d2[x]] = Label(frame_p2, bg="brown", name="2_"+str(p2_draw_count).zfill(3)+"_"+d2[x], width=13, height=4, relief=RAISED)
            h2[list(h2)[-1]].grid(row=0,column=p2_draw_count)
            p2_draw_count += 1
            d2.pop(x)
            update_field()

    ###select a card to play from the hand
    def select_card(x):
        global selected_card, play_var
        if selected_card:
            selected_card.config(relief=RAISED,bg="white")
        selected_card = x
        x.config(relief=RIDGE,bg="yellow")
        play_var = True
        hide_info()
        for i in [9,10,11,13,14,15,16,17]:
            if decode_card(str(selected_card)[-4:]).tribe.lower() != "item" and not cards_info[i]:
                cards[i].config(bg="orange")

    ###play selected card
    def play_card(x):
        global selected_card, play_var
        if play_var and decode_card(str(selected_card)[-4:]).tribe.lower() != "item" and int(str(x)[-2:]) in [9,10,11,13,14,15,16,17] and not cards_info[int(str(x)[-2:])]:
            cards_info[int(str(x)[-2:])] = str(selected_card)[-4:]
            h1[str(selected_card)[-8:]].grid_forget()
            del h1[str(selected_card)[-8:]]
            hide_info()
            update_field()
            play_var = False
            for i in range(len(cards_info)):
                if not cards_info[i]:
                    cards[i].config(bg="gray")

    ###update card information textbox
    def info(x):
        global card_info
        newline = "\n"
        if x:
            card_info.config(text=(f"{decode_card(x).name}"
                            f"   [{str(decode_card(x).power)} / {str(decode_card(x).health)}]"
                            f"   ({decode_card(x).main}"
                            f"{' / '+decode_card(x).aux+')' if decode_card(x).aux else ')'}"
                            f"   {decode_card(x).tribe.upper()}   Cost: {str(decode_card(x).cost)}"
                            f"{newline+'Main effect: '+decode_card(x).mfx if decode_card(x).mfx else ''}"
                            f"{newline+'Aux effect: '+decode_card(x).afx if decode_card(x).afx else ''}"
                            f"{newline+'Equip effect: '+decode_card(x).efx if decode_card(x).efx else ''}"
                            ), width=info_frame.winfo_width(), wraplength=info_frame.winfo_width())
        else:
            hide_info()

    ###display card information
    def show_info():
        #card_info.place(x=table.winfo_pointerx() - table.winfo_rootx(),y=table.winfo_pointery() - table.winfo_rooty())
        card_info.pack(anchor=W)

    ###hide card information
    def hide_info():
        card_info.pack_forget()

    ###update visuals of all slots
    def update_field():
        for i in range(len(cards_info)):
            if cards_info[i]:
                cards[i].config(bg="white", relief=RAISED, text=decode_card(cards_info[i]).name)
            else:
                cards[i].config(bg="grey", relief=SUNKEN)
        if d1:
            d1_lbl.config(bg="brown", relief=RAISED)
        else:
            d1_lbl.config(bg="grey", relief=SUNKEN)
        if d2:
            d2_lbl.config(bg="brown", relief=RAISED)
        else:
            d2_lbl.config(bg="grey", relief=SUNKEN)
        table.update_idletasks()

    #adding card information textbox functionality
    frame.bind("<Button-3>", lambda z:hide_info())
    for i in range(len(cards)):
        cards[i].bind("<Button-3>", lambda z:[hide_info(),info(cards_info[int(str(z.widget)[-2:])]),show_info() if (z.widget["text"]) else hide_info()])

    #DEBUGGING ONLY
    #table.bind("<Return>",lambda z:draw(0))
    table.bind("<Escape>",lambda z:[table.destroy(),start()])

    #occupying beginning hands
    shuffle(d1)
    for i in range(5):
        draw_p1(0)
        draw_p2(0)

    #executing game
    table.mainloop()

#create options menu
def options():
    print("options test")

#create start menu
def start():
    start_menu = Tk()
    start_menu.title("START MENU")
    start_menu.geometry("500x500+100+100")
    start_menu.resizable(0,0)
    start_menu.config(bg="black")
    start_frame = Frame(start_menu, bg="black")
    start_lbl = Label(start_frame, bg="grey", width=50, height=15, text="[INSERT TEXT HERE]")
    start_btn = Button(start_frame, text="NEW GAME", width=20, command=lambda:[start_menu.destroy(),game()])
    options_btn = Button(start_frame, text="OPTIONS", width=20, command=options)
    quit_btn = Button(start_frame, text="QUIT TO DESKTOP", width=20, command=start_menu.destroy)
    start_frame.pack()
    start_lbl.grid()
    start_btn.grid(pady=6)
    options_btn.grid(pady=0)
    quit_btn.grid(pady=6)
    start_menu.mainloop()

#begin program
start()
