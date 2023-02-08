#retrieve slot number from label name
def slot_num(x):
    return int(str(x)[-2:])

#draw a card from player 1's deck to their hand
def draw_p1(x):
    global p1_draw_count
    if d1:
        selected_card.config(relief=RAISED, bg="white") if selected_card else ()
        h1[f"{str(p1_draw_count).zfill(3)}_{d1[x][:4]}"] = Label(frame_p1, bg="white", name=f"1_{str(p1_draw_count).zfill(3)}_{d1[x]}", width=12, height=4, relief=RAISED, text=decode_card(d1[x][:4]).name, justify="center")
        (a := h1[list(h1)[-1]]).grid(row=0,column=p1_draw_count)
        p1_draw_count += 1
        a.bind("<Button-1>", lambda z:select_card(z.widget) if player_turn == 1 else ())
        a.bind("<Button-3>", lambda z:info(str(z.widget)[-8:]))
        d1.pop(x)
        update_field()
        a["wraplength"] = h1[list(h1)[0]].winfo_width() - 10
        
#draw a card from player 2's deck to their hand
def draw_p2(x):
    global p2_draw_count
    if d2:
        h2[f"{str(p2_draw_count).zfill(3)}_{d2[x][:4]}"] = Label(frame_p2, bg="brown", name=f"2_{str(p2_draw_count).zfill(3)}_{d2[x]}", width=12, height=3, relief=RAISED)
        h2[list(h2)[-1]].grid(row=0,column=p2_draw_count)
        p2_draw_count += 1
        d2.pop(x)
        update_field()

#select a card to play from the hand
def select_card(x):
    global selected_card
    update_field()
    card_info.pack_forget()
    if x in h1.values():
        selected_card.config(relief=RAISED, bg="white") if selected_card else ()
        (selected_card := x).config(relief=RIDGE, bg="yellow")
        for i in [*p1_mains,*p1_auxes]:
            cards[i].config(bg="orange") if not cards_info[i] else ()
    elif slot_num(x) in [*p1_mains,*p1_auxes] and player_turn == 1:
        selected_card.config(relief=RAISED, bg="white") if selected_card else ()
        (selected_card := x).config(relief=RIDGE, bg="yellow")
        if slot_num(x) in p1_mains:
            for i in p2_mains:
                cards[i].config(bg="orange") if cards_info[i] and x.can_atk else ()

#play selected card
def play_card(x):
    global selected_card
    if x["bg"] == "orange" and selected_card in h1.values():
        cards_info[slot_num(x)] = str(selected_card)[-8:]
        h1.pop(str(selected_card)[-12:-4]).grid_forget()
        x.can_atk = 1
        update_field()
    elif selected_card in h2.values():
        cards_info[slot_num(x)] = str(selected_card)[-8:]
        h2.pop(str(selected_card)[-12:-4]).grid_forget()
        x.can_atk = 1
        update_field()
    card_info.pack_forget()

#call an attack
def attack(x):
    global selected_card
    if x["bg"] == "orange" and selected_card.can_atk:
        a = cards_info[slot_num(x)]
        b = int(cards_info[slot_num(selected_card)][5])
        cards_info[slot_num(x)] = "" if b >= int(a[-1]) else f"{a[:-1]}{str(int(a[-1])-b)}"
        selected_card.can_atk = 0
        update_field()

#end the current player's turn    
def end_turn():
    global player_turn
    player_turn = 3 - player_turn
    end_btn.pack_forget() if player_turn == 2 else end_btn.pack(expand=YES)
    for i in [*p2_mains,*p1_mains]:
        cards[i].can_atk = int(bool(player_turn-(i-2)//3)) if cards_info[i] else 0
    for i in h1.values():
        i.config(relief=RAISED, bg="white") if i["bg"] == "yellow" else ()
    selected_card = ""
    card_info.pack_forget()
    update_field()

#ALL CARD EFFECT FUNCTIONS
###0001
def fx_0001():
    return True
