import tkinter as tk
from tkinter import *
from PIL import ImageTk
from PIL import Image

def Mustjaak():
    root = tk.Tk()
    w = 500
    h = 500
    ikoon = Image.open("kaardid/logo.png")
    iconPhoto = ImageTk.PhotoImage(ikoon)
    root.title(string = "MustJaak")
    root.iconphoto(False, iconPhoto)
    button = Button(root, text = "Alusta mängu!", bd=5,
                    command = root.destroy)
    button.pack(side="bottom")

    root.mainloop()
Mustjaak()