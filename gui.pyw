import tkinter as tk

window = tk.Tk()

label = tk.Label(master=window, text="")

def greeting():
    label.config(text="Hallo Welt!")

button = tk.Button(master=window, text="KlickMich", command=greeting)

label.pack()
button.pack()

window.mainloop()