import tkinter as tk
from tkinter import ttk
import variables
import combat
from random import randint

# Configures colors and such
style = ttk.Style(variables.root)
style.configure('.', background='black', foreground='white')
style.configure('default.TFrame', background='black', foreground='white')
style.configure('default.TButton', background='white', foreground='black')
style.configure('patterns.TButton', background='white', foreground='black', font=('', 16))
style.map('TButton', background=[('active', 'red')])
style.configure('selected.TFrame', background='purple', foreground='white')

variables.fight = combat.Battle([variables.enemy], [variables.player])
variables.root.mainloop()
