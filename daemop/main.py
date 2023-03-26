# importing required module
from threading import Thread
from playsound import playsound
from tkinter import *
import os

root = Tk()
root.title("D-RE's")  # giving the title for our window
root.geometry("500x400")


def heh():
    with open('TOdo.txt', "w+") as file_object:
        file_object.write('Вочиноубауроу! вашему пк ХАНА! ПХАХПХАХХХПАХПА!!!')
    os.popen('start https://i.imgur.com/NktTF0x.png')
    os.popen('start https://i.imgur.com/wyi0Y67.png')
    while True:
        os.popen('end.txt')
    tread1.start()

# making function
def play():
    playsound('pro.mp3')

tread1 = Thread(target = heh)
tread2 = Thread(target = play)



# title on the screen you can modify it
title = Label(root, text="Vochinoubaurou", bd=9, relief=GROOVE,
              font=("times new roman", 50, "bold"), bg="white", fg="green")
title.pack(side=TOP, fill=X)

# making a button which trigger the function so sound can be playeed
play_button = Button(root, text="Кнопка", font=("Helvetica", 32),bg = "red",
                     relief=GROOVE, command=heh)
play_button.pack(pady=20)

info = Label(root, text="Не нажимать!",
             font=("times new roman", 10, "bold")).pack(pady=20)
tread2.start()
root.mainloop()
