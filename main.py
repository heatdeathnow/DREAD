import tkinter as tk
from tkinter import ttk
import entities
import moves
import scenes
import variables
import patterns
import combat

# Configures colors and such
style = ttk.Style(variables.root)
style.configure('.', background='black', foreground='white')
style.configure('default.TFrame', background='black', foreground='white')
style.configure('default.TButton', background='white', foreground='black')
style.configure('patterns.TButton', background='white', foreground='black', font=('', 16))
style.map('TButton', background=[('active', 'red')])
style.configure('selected.TFrame', background='purple', foreground='white')

player = entities.Player("Resistência", 50, 20, 3, 1, 4, 0)
player.skills.append(moves.Melee(player))
player.skills.append(moves.Tackle(player))

enemy = entities.Entity("Velocidade", 15, 0, 2, 1, 12)
enemy.skills.append(moves.Melee(enemy))

enemy1 = entities.Entity("Ataque", 15, 20, 5, 1, 3)
enemy1.skills.append(moves.Melee(enemy1))
enemy1.skills.append(moves.Tackle(enemy1))

enemy2 = entities.Entity("Defesa", 15, 20, 2, 3, 2)
enemy2.skills.append(moves.Melee(enemy2))
enemy2.skills.append(moves.Tackle(enemy2))

variables.combat = combat.Battle([enemy, enemy1, enemy2], [player])

variables.root.mainloop()
