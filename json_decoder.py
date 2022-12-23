import json

from card_class import *

with open("card_master_list.json", "r") as file:
    data = json.load(file)
    cards = data["Cards"]


def decode_card(id):
    formatted_id = ""
    if type(id) == int:
        for symbol in range(4 - len(str(id))):
            formatted_id += "0"
        formatted_id += str(id)
    elif type(id) == str:
        formatted_id = id
    card = cards[formatted_id]
    return Card(card["name"], card["cost"], card["power"], card["health"], card["tribe"], card["main"], card["aux"], 
                card["mfx"], card["mfx_turn"], card["afx"], card["afx_turn"], card["efx"], card["efx_turn"])
    

# print(decode_card(1).name)
# print(decode_card("0001").name)