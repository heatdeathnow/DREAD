import tkinter as tk
from tkinter import ttk
import entities
import scenes

player = entities.Player('Char', 40, 20, 5, 5, 5, 0)

root = tk.Tk()
root.geometry('720x480')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.resizable(False, False)
root.title('Dread')
