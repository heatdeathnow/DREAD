import tkinter as tk
from tkinter import ttk
import entities
import scenes
import moves
import combat
from random import randint

player = entities.Player("Char", 20, 20, 5, 1, 3, 0)
player.skills.append(moves.Melee(player))
player.skills.append(moves.Tackle(player))

enemy = entities.Entity("Iteration 0", 5, 5, 2, 0, 1)
enemy.skills.append(moves.Melee(enemy))
enemy.skills.append(moves.Tackle(enemy))

root = tk.Tk()
root.geometry('720x480')
root.configure(background='black')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.resizable(False, False)
root.title('Dread')

skill = 1  # Used to determine skill multiplier in fight
fight = None  # stores the current fight
