from tkinter import *

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
    start_btn = Button(start_frame, text="NEW GAME", width=20, command=lambda:[start_menu.destroy(),exec(open("card_game.py").read())])
    options_btn = Button(start_frame, text="OPTIONS", width=20, command=options)
    quit_btn = Button(start_frame, text="QUIT TO DESKTOP", width=20, command=start_menu.destroy)
    start_frame.pack()
    for i,j in zip([start_lbl,start_btn,options_btn,quit_btn],[0,6,0,6]):
        i.grid(pady=j)
    start_menu.mainloop()

#begin program
start()
