from random import randint

def flip_coin(amount=1):
    heads = 0
    for _ in range(amount):
        heads += randint(0,1)
    return((heads, amount-heads))

def roll_dice(amount=1, faces=6):
    return_vals = {i+1:0 for i in range(faces)}
    for _ in range(amount):
        return_vals[randint(1, faces)] += 1
    return return_vals
