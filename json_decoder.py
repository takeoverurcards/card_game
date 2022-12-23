import json

from card_class import *

with open("card_master_list.json", "r") as file:
    cards = json.load(file)["Cards"]


def decode_card(card_id):
    formatted_id = ""
    if type(card_id) == int:
        for _ in range(4 - len(str(card_id))):
            formatted_id += "0"
        formatted_id += str(card_id)
    elif type(card_id) == str:
        formatted_id = card_id
    else:
        raise TypeError("INVALID ID FORMAT")
    card = cards[formatted_id]
    return Card(card["name"], card["cost"], card["power"], card["health"], card["tribe"], card["main"], card["aux"], 
                card["mfx"], card["mfx_turn"], card["afx"], card["afx_turn"], card["efx"], card["efx_turn"])

# print(decode_card(1).name)
# print(decode_card("0001").name)