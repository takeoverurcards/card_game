import random
from tkinter import *
from json_decoder import *


class EntireGame:
    def __init__(self, d1, d2):
        self.table = Tk() #main window
        self.table.title("[INSERT CARD GAME NAME HERE] by Take, Zoop, and Elite")
        self.table.geometry("777x976+0+0")
        self.table.resizable(0,0) #prevents manual window resizing
        self.table.config(bg="black")
        self.frame = Frame(self.table, pady=60, bg="black") #main widget for slots
        self.frame_p2 = Frame(self.table, bg="black", height=66)
        self.frame_p1 = Frame(self.table, bg="black", height=66)
        self.frame_p2.pack()
        self.frame.pack()
        self.frame_p1.pack()
        self.info_frame = Frame(self.table, width=777, height=100)
        self.info_frame.pack()
        self.p1_health = Label(self.frame, bg="black", fg="white", text="3", font=("Britannic Bold",40))
        self.p2_health = Label(self.frame, bg="black", fg="white", text="3", font=("Britannic Bold",40))
        self.p1_health.grid(row=0,column=6)
        self.p2_health.grid(row=3,column=0)
        self.slots = [1,2,3,4,5,7,9,10,11,16,17,18,20,22,23,24,25,26] #numbers indicating grid locations for all card slots
        self.g1 = [] #graveyard of player 1
        self.g2 = [] #graveyard of player 2
        self.d1 = d1 #deck of player 1
        self.d2 = d2 #deck of player 2
        self.h1 = {} #hand of player 1
        self.h2 = {} #hand of player 2
        self.player_turn = 0 #turn of indicated player
        self.p1_draw_count = self.p2_draw_count = 0 #number of cards drawn for respective player
        self.play_var = False #indicator for play_card()
        self.selected_card = ""
        self.card_info = Label(self.info_frame, justify="left") #card information textbox
        self.m11 = self.m21 = self.m31 = self.m12 = self.m22 = self.m32 = self.a11 = self.a21 = self.a31 = self.a41 = self.a51 = self.a12 = self.a22 = self.a32 = self.a42 = self.a52 = self.n1 = self.n2 = "" #all card labels on the field
        self.m11_info = self.m21_info = self.m31_info = self.m12_info = self.m22_info = self.m32_info = self.a11_info = self.a21_info = self.a31_info = self.a41_info = self.a51_info = self.a12_info = self.a22_info = self.a32_info = self.a42_info = self.a52_info = self.n1_info = self.n2_info = "" #all current cards on the field
        self.cards = [self.a12,self.a22,self.a32,self.a42,self.a52,self.n2,self.m12,self.m22,self.m32,self.m11,self.m21,self.m31,self.n1,self.a11,self.a21,self.a31,self.a41,self.a51] #list containing all card slots
        self.cards_info = [self.a12_info,self.a22_info,self.a32_info,self.a42_info,self.a52_info,self.n2_info,self.m12_info,self.m22_info,self.m32_info,self.m11_info,self.m21_info,self.m31_info,self.n1_info,self.a11_info,self.a21_info,self.a31_info,self.a41_info,self.a51_info] #list containing all card slot information
        for i in range(len(self.slots)):
            self.cards[i] = Label(self.frame, name="slot_"+str(i).zfill(2), width=15, height=10, bg="grey", relief=SUNKEN, wraplength=100, justify="center")
            self.cards[i].grid(row=int(self.slots[i]/7), column=self.slots[i]%7)
            self.cards[i].bind("<Button-1>", lambda z:self.play_card(z.widget))
        for i in json.load(open("card_master_list.json", "r"))["Cards"]:
               d1.append(i)
        random.shuffle(self.d1)
        self.table.bind('<Return>',lambda z:(self.draw(0)))
        self.frame.bind("<Button-3>", lambda z, k=self:k.shide_info())
        for i in range(len(self.cards)):
            self.cards[i].bind("<Button-3>", lambda z, k=self:[k.hide_info(),k.info(k.cards_info[int(str(z.widget)[-2:])]),k.show_info() if (z.widget["text"]) else k.hide_info()])


    def draw(self, x):
        self.h1[str(self.p1_draw_count).zfill(3)+"_"+self.d1[x]] = Label(self.frame_p1, name="1_"+str(self.p1_draw_count).zfill(3)+"_"+self.d1[x], width=13, height=4, relief=RAISED, text=decode_card(self.d1[x]).name, wraplength=90, justify="center")
        self.h1[list(self.h1)[-1]].grid(row=0,column=self.p1_draw_count)
        self.p1_draw_count += 1
        self.h1[list(self.h1)[-1]].bind("<Button-1>", lambda z, k=self:k.select_card(z.widget))
        self.h1[list(self.h1)[-1]].bind("<Button-3>", lambda z, k=self:[k.hide_info(),k.info(str(z.widget)[-4:]),k.show_info()])
        self.d1.pop(x)


    def play_card(self, x):
        if self.play_var and decode_card(str(self.selected_card)[-4:]).tribe.lower() != "item" and int(str(x)[-2:]) in [9,10,11,13,14,15,16,17] and not self.cards_info[int(str(x)[-2:])]:
            self.cards_info[int(str(x)[-2:])] = str(self.selected_card)[-4:]
            self.h1[str(self.selected_card)[-8:]].grid_forget()
            del self.h1[str(self.selected_card)[-8:]]
            self.hide_info()
            self.update_field()
            self.play_var = False
            for i in range(len(self.cards_info)):
                if not self.cards_info[i]:
                    self.cards[i].config(bg="gray")

    def hide_info(self):
        self.card_info.place_forget()

    def update_field(self):
        for i in range(len(self.cards_info)):
            if self.cards_info[i]:
                self.cards[i].config(bg="white", relief=RAISED, text=decode_card(self.cards_info[i]).name)
            else:
                self.cards[i].config(bg="grey", relief=SUNKEN)
        self.table.update_idletasks()

    def info(self, x):
        newline = "\n"
        if x:
            self.card_info.config(text=(f"{decode_card(x).name}"
                            f"   [{str(decode_card(x).power)} / {str(decode_card(x).health)}]"
                            f"   ({decode_card(x).main}"
                            f"{' / '+decode_card(x).aux+')' if decode_card(x).aux else ')'}"
                            f"   {decode_card(x).tribe.upper()}   Cost: {str(decode_card(x).cost)}"
                            f"{newline+'Main effect: '+decode_card(x).mfx if decode_card(x).mfx else ''}"
                            f"{newline+'Aux effect: '+decode_card(x).afx if decode_card(x).afx else ''}"
                            f"{newline+'Equip effect: '+decode_card(x).efx if decode_card(x).efx else ''}"
                            ), width=self.info_frame.winfo_width(), wraplength=self.info_frame.winfo_width())
        else:
            self.hide_info()

    def show_info(self):
        self.card_info.place(x=self.table.winfo_pointerx() - self.table.winfo_rootx(),y=self.table.winfo_pointery() - self.table.winfo_rooty())
        self.card_info.pack(anchor=W)

    def select_card(self, x):
        if self.selected_card:
            self.selected_card.config(relief=RAISED,bg="white")
        self.selected_card = x
        x.config(relief=RIDGE,bg="yellow")
        self.play_var = True
        self.hide_info()
        for i in [9,10,11,13,14,15,16,17]:
            if decode_card(str(self.selected_card)[-4:]).tribe.lower() != "item" and not self.cards_info[i]:
                self.cards[i].config(bg="orange")




test = EntireGame([], [])

test.table.mainloop()