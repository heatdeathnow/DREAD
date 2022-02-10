import tkinter as tk
from tkinter import ttk
import entities
import scenes

root = tk.Tk()
root.geometry('720x480')
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.resizable(False, False)
root.title('Dread')

skill = 1  # Used to determine skill multiplier in combat
combat = None  # stores the current combat
