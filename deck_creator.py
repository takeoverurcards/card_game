import json
from os.path import exists
from pathlib import Path

import tkinter as tk


deck_min_size = 50
deck_max_size = 60


def debug():
    card_list[card_listbox.curselection()[0]]


def count_card(input):
    if input >= 99:
        return "99"
    str_input = str(input)
    if len(str_input) == 2:
        return str_input
    return "0" + str_input
    

def update_deck_listbox(cursor=None):
    deck_listbox.delete(0, deck_listbox.size())
    counter = 0
    for card in deck_dict:    
        deck_listbox.insert(counter, f"{count_card(deck_dict[card])}  | {cards[card]['name']}")
    if cursor is not None:
        deck_listbox.selection_set(cursor)
    count_deck_size()


def add_card_to_deck():
    if not len(card_listbox.curselection()):
        return
    card_id = card_list[card_listbox.curselection()[0]]
    if card_id in deck_dict:
        deck_dict[card_id] += 1
    else:
        deck_dict[card_id] = 1
    update_deck_listbox()


def remove_card_from_deck():
    selection = deck_listbox.curselection()
    if not len(selection):
        return
    card_removed = list(deck_dict)[::-1][selection[0]]
    if deck_dict[card_removed] == 1:
        del deck_dict[card_removed]
    else:
        deck_dict[card_removed] -= 1
    update_deck_listbox(selection[0])


def count_deck_size():
    count = 0
    for card_id in deck_dict:
        count += deck_dict[card_id]
    deck_size.set(count)


def clear_deck():
    deck_dict.clear()
    deck_listbox.delete(0, deck_listbox.size())
    update_deck_listbox()


def create_deck():
    deck_name = deck_name_var.get().strip()
    deck_path = Path(".")/"decks"/f"{deck_name}.json"
    if exists(deck_path) and not overwrite_var.get():
        error_window("overwrite")
        return
    if deck_name == "":
        error_window("empty")
        return
    if deck_size.get() > deck_max_size:
        error_window("surplus")
        return
    if deck_size.get() < deck_min_size:
        error_window("deficet")
        return
    with open(deck_path, "w") as file:
        json.dump(deck_dict, file, indent=4)
    

def error_window(error_type):
    error_root = tk.Toplevel(bg="red")
    error_root.geometry("300x200")
    error_root.title("ERROR")
    error_mssg = ""
    error_main_frame = tk.Frame(error_root, bg="red")
    if error_type == "overwrite":
        confirm_frame = tk.Frame(error_main_frame, relief=tk.RAISED, borderwidth=5)
        error_mssg = "Preexisting File! Overwrite?"
        tk.Label(confirm_frame, text="Overwrite?").grid(column=0, row=0)
        tk.Checkbutton(confirm_frame, variable=overwrite_var).grid(column=1, row=0)
        confirm_frame.grid(column=0, row=1)
    elif error_type == "empty":
        error_mssg = "You Cannot Create a Deck Without a Name!"
    elif error_type == "deficet":
        error_mssg = f"Not Enough Cards in Deck! \nDeck Must Have at Least {deck_min_size} Cards!"
    elif error_type == "surplus":
        error_mssg = f"Too Many Cards in Deck! \nDeck Can Only Have up to {deck_max_size} Cards!"
    tk.Label(error_main_frame, text=error_mssg, height=3, relief=tk.GROOVE, borderwidth=5, bg="gray").grid(column=0, row=0)
    error_main_frame.pack(anchor='c')

    error_root.mainloop()


root = tk.Tk()
root.geometry("1000x1000")
root.resizable(False, False)

with open("card_master_list.json", "r") as data:
    cards = json.load(data)["Cards"]

card_ids = list(cards)
card_list = []
deck_dict = {}


main_frame = tk.Frame(root)

overwrite_var = tk.BooleanVar()
deck_size = tk.IntVar(value=0)
#deck_size_label_var = tk.StringVar(f"{deck_size.get()}/{deck_max_size}")

deck_manip_frame = tk.Frame(main_frame)
add_frame = tk.Frame(deck_manip_frame)
remove_frame = tk.Frame(deck_manip_frame)


deck_name_var = tk.StringVar()
deck_name_var.trace("w", lambda x, y, z: overwrite_var.set(False))
deck_name_frame = tk.Frame(main_frame)
tk.Label(deck_name_frame, text="Deck Name:").grid(column=0, row=0)
#deck_count_label = tk.Label(deck_name_frame, text=deck_size_label_var.get())
#TODO:make an active deck size counter display
tk.Entry(deck_name_frame, textvariable=deck_name_var, width=50).grid(column=1, row=0)



card_listbox = tk.Listbox(add_frame, width=30, height=40)
for card in cards:
    card_listbox.insert(int(card)-1, cards[card]["name"])
    card_list.append(card)


deck_listbox = tk.Listbox(remove_frame, width=30, height=40)

remove_buttons_frame = tk.Frame(remove_frame)
remove_card_button = tk.Button(remove_buttons_frame, text="Remove Card", command=remove_card_from_deck)
clear_deck_button = tk.Button(remove_buttons_frame, text="Clear Deck", command=clear_deck)

add_button_frame = tk.Frame(add_frame)
add_card_button = tk.Button(add_button_frame, text="Add Card to Deck",command=add_card_to_deck)
create_deck_button = tk.Button(add_button_frame, text="Create Deck", command=create_deck)

#TODO: implement show_ids
#show_ids_var = tk.BooleanVar()
#show_ids_checkbx = tk.Checkbutton(main_frame, variable=show_ids_var)

deck_name_frame.pack()
card_listbox.pack()
deck_listbox.pack()
add_card_button.grid(column=0, row=0)
create_deck_button.grid(column=1, row=0)
add_button_frame.pack()
add_frame.grid(column=0, row=0)
remove_card_button.grid(column=0, row=0)
clear_deck_button.grid(column=1, row=0)
remove_buttons_frame.pack()
remove_frame.grid(column=1, row=0)
deck_manip_frame.pack()
main_frame.pack()
root.mainloop()