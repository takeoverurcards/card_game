from random import randint

def flip_coin(amount):
    heads = tails = 0
    for _ in range(amount):
        if randint(0,1):
            heads+=1
        else:
            tails+=1
    return((heads, tails))

def roll_dice(amount, faces=6):
    return_vals = {}
    for i in range(1, faces+1):
        return_vals[i] = 0
    
    for _ in range(amount):
        return_vals[randint(1, faces)] += 1
    return return_vals
