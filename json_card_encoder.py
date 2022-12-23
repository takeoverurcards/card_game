import json
import tkinter as tk

from card_class import *

with open('card_master_list.json', 'r') as file:
    data = json.load(file)
    card_list = data["Cards"]


highest_card_id = int(list(card_list.keys())[-1])
card_name_list = []
for id_ in card_list:
    card_name_list.append(card_list[id_]['name'])

root = tk.Tk()

mfx_t = tk.BooleanVar(root)
afx_t = tk.BooleanVar(root)
efx_t = tk.BooleanVar(root)

m_color = tk.StringVar(root, value='R')
a_color = tk.StringVar(root)


def create_card():
    highest_card_id = int(list(card_list.keys())[-1])
    card_name_list = []
    for id_ in card_list:
        card_name_list.append(card_list[id_]['name'])

    name_out = name_field.get()
    cost_out = cost_field.get()
    power_out = power_field.get()
    health_out = health_field.get()
    tribe_out = tribe_field.get()
    main_color = m_color.get()
    aux_color = a_color.get()
    mfx = mfx_in.get()
    mfx_turn = mfx_t.get()
    afx = afx_in.get()
    afx_turn = afx_t.get()
    efx = efx_in.get()
    efx_turn = efx_t.get()
    try:
        cost_out = int(cost_out)
        power_out = int(power_out)
        health_out = int(health_out)
    except ValueError:
        error = tk.Toplevel(root, bg='black')
        error.geometry('400x200')
        error.resizable(False, False)
        error.title('ERROR')
        error_frame = tk.Frame(error, relief=tk.RAISED, borderwidth=5, bg='red')
        error_mssg = tk.Label(error_frame, text='Invalid cost/power/health')
        error_mssg.pack()
        error_frame.place(anchor='c', relx=0.5, rely=0.5)
        return
    if name_out not in card_name_list:
        id_out = str(highest_card_id+1)
        id_correction_zs =""
        for _ in range(4-len(id_out)):
            id_correction_zs += "0"
        id_out = id_correction_zs + id_out
        card_out = {"name":name_out, "cost": cost_out, "power":power_out, "health":health_out, 
            "tribe":tribe_out, "main":main_color, "aux":aux_color, "mfx":mfx, "mfx_turn":mfx_turn, 
                "afx":afx, "afx_turn":afx_turn, "efx":efx, "efx_turn":efx_turn}
        data["Cards"][id_out] = card_out
        with open('card_master_list.json', 'w') as file:
            file.write(json.dumps(data, indent=4))
        


root.title("Card Creator")

root.geometry("550x600")

text_frame = tk.Frame(root, relief=tk.GROOVE, borderwidth=5)

name_field = tk.Entry(text_frame, width=30)
tribe_field = tk.Entry(text_frame, width=20)
tk.Label(text_frame, text="Card Name").grid(column=0, row=0, sticky='nw')
tk.Label(text_frame, text="Card Tribe").grid(column=1, row=0, sticky='nw')
name_field.grid(column=0, row=1, sticky='nw', pady=10, padx=2)
tribe_field.grid(column=1, row=1, sticky='nw', padx=2, pady=10)


num_entry_frame = tk.Frame(root, relief=tk.GROOVE, borderwidth=5)

cost_field = tk.Entry(num_entry_frame, width=4)
power_field = tk.Entry(num_entry_frame, width=4)
health_field = tk.Entry(num_entry_frame, width=4)

cost_field.grid(column=0, row=0, padx=2, sticky='w')
power_field.grid(column=1, row=0, padx=2, sticky='w')
health_field.grid(column=2, row=0, padx=2, sticky='w')

colors_frame = tk.Frame(root)

main_color_field = tk.Frame(colors_frame, height=3, relief=tk.GROOVE, borderwidth=5)
aux_color_field = tk.Frame(colors_frame, height=3, relief=tk.GROOVE, borderwidth=5)

main_red = tk.Radiobutton(main_color_field, variable=m_color, value='R')
main_blue = tk.Radiobutton(main_color_field, variable=m_color, value='B')
main_yellow = tk.Radiobutton(main_color_field, variable=m_color, value='Y')


tk.Label(main_color_field, text='Red').grid(column=0, row=1)
tk.Label(main_color_field, text='Blue').grid(column=0, row=2)
tk.Label(main_color_field, text='Yellow').grid(column=0, row=3)
tk.Label(main_color_field, text="Main Color").grid(column=0, row=0)
tk.Label(main_color_field, text='', height=2).grid(column=0, row=4)
main_red.grid(column=1, row=1)
main_blue.grid(column=1, row=2)
main_yellow.grid(column=1, row=3)

aux_none = tk.Radiobutton(aux_color_field, variable=a_color, value='')
aux_red = tk.Radiobutton(aux_color_field, variable=a_color, value='R')
aux_blue = tk.Radiobutton(aux_color_field, variable=a_color, value='B')
aux_yellow = tk.Radiobutton(aux_color_field, variable=a_color, value='Y')

tk.Label(aux_color_field, text='Red').grid(column=0, row=1)
tk.Label(aux_color_field, text='Blue').grid(column=0, row=2)
tk.Label(aux_color_field, text='Yellow').grid(column=0, row=3)
tk.Label(aux_color_field, text='None', height=2).grid(column=0, row=4)
tk.Label(aux_color_field, text="Auxiliary Color").grid(column=0, row=0)
aux_red.grid(column=1, row=1)
aux_blue.grid(column=1, row=2)
aux_yellow.grid(column=1, row=3)
aux_none.grid(column=1, row=4)

main_color_field.grid(column=0, row=0)
aux_color_field.grid(column=1, row=0)

effects = tk.Frame(root, relief=tk.GROOVE, borderwidth=5)
tk.Label(effects, text="Effect Description                    Effect Turn").grid(column=0, row=0)

mfx_frame = tk.Frame(effects, relief=tk.SUNKEN, borderwidth=3)
mfx_in = tk.Entry(mfx_frame, width=30)
mfx_turn_in = tk.Checkbutton(mfx_frame, variable=mfx_t)
tk.Label(mfx_frame, text="Main").grid(column=0, row=0, sticky='nw')
mfx_in.grid(column=0, row=1)
mfx_turn_in.grid(column=1, row=1)
mfx_frame.grid(column=0, row=1)

afx_frame = tk.Frame(effects, relief=tk.SUNKEN, borderwidth=3)
afx_in = tk.Entry(afx_frame, width=30)
afx_turn_in = tk.Checkbutton(afx_frame, variable=afx_t)
tk.Label(afx_frame, text="Auxiliary").grid(column=0, row=0, sticky='nw')
afx_in.grid(column=0, row=1)
afx_turn_in.grid(column=1, row=1)
afx_frame.grid(column=0, row=2)

efx_frame = tk.Frame(effects, relief=tk.SUNKEN, borderwidth=3)
efx_in = tk.Entry(efx_frame, width=30)
efx_turn_in = tk.Checkbutton(efx_frame, variable=efx_t)
tk.Label(efx_frame, text="Equipment").grid(column=0, row=0, sticky='nw')
efx_in.grid(column=0, row=1)
efx_turn_in.grid(column=1, row=1)
efx_frame.grid(column=0, row=3)

# Finally griding all the stuff to the root window

generate_button = tk.Button(root, text="Generate", command=create_card)


text_frame.grid(column=0, row=0, sticky='nw')
num_entry_frame.grid(column=0, row=1, sticky='nw')
colors_frame.grid(column=0, row=2, sticky='nw')
effects.grid(column=0, row=3, sticky='nw')
generate_button.grid(column=0, row=4, pady=10)




root.mainloop()

