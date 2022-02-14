import tkinter as tk
from tkinter import ttk
from random import randint
import clutches
import entities
import variables


class CombatInfo(ttk.Frame):
    def __init__(self, entity, combat_root):
        super().__init__(combat_root)

        self.entity = entity

        name_label = ttk.Label(self, text=entity.name)
        name_label.grid(row=0, column=1, padx=5, pady=5)

        hp_label = ttk.Label(self, text='PV: ')
        hp_label.grid(row=1, column=0, padx=5, pady=5)
        self.hp_bar = ttk.Progressbar(self, value=(entity.hp / entity.max_hp * 100))
        self.hp_bar.grid(row=1, column=1, padx=5, pady=5)

        try:
            entity.dread
        except AttributeError:
            pass
        else:
            deli_label = ttk.Label(self, text='DL: ')
            deli_label.grid(row=2, column=0, padx=5, pady=5)
            self.deli_bar = ttk.Progressbar(self, value=(entity.delirium / entity.max_delirium * 100))
            self.deli_bar.grid(row=2, column=1, padx=5, pady=5)

            dread_label = ttk.Label(self, text='TORPOR: ')
            dread_label.grid(row=3, column=0, padx=5, pady=5)
            self.dread_bar = ttk.Progressbar(self, value=entity.dread)
            self.dread_bar.grid(row=3, column=1, padx=5, pady=5)

    def toggle(self):
        self.hp_bar.configure(value=(self.entity.hp / self.entity.max_hp * 100))

        try:
            self.entity.dread
        except AttributeError:
            pass
        else:
            self.deli_bar.configure(value=(self.entity.delirium / self.entity.max_delirium * 100))
            self.dread_bar.configure(value=self.entity.dread)


def survival():

    variables.player.hp = variables.player.max_hp
    variables.player.delirium = variables.player.max_delirium

    iteration = int(variables.enemy.name[10:])
    variables.enemy.name = "Iteration " + str(iteration + 1)

    rand = randint(0, 4)
    if rand == 0:
        variables.enemy.max_hp += 5
    elif rand == 1:
        variables.enemy.max_delirium += 5
    elif rand == 2:
        variables.enemy.attack += 1
    elif rand == 3:
        variables.enemy.defense += 1
    elif rand == 4:
        variables.enemy.speed += 1

    variables.enemy.hp = variables.enemy.max_hp
    variables.enemy.delirium = variables.enemy.max_delirium

    print(f'{variables.enemy.name}'
          f'\nHP: {variables.enemy.max_hp}, DL: {variables.enemy.max_delirium}'
          f'\nAT: {variables.enemy.attack}, DE: {variables.enemy.defense}, SP: {variables.enemy.speed}')

    label = ttk.Label(variables.root, text="Você derrotou o inimigo, mas outro aparece!")
    label.grid(row=0, padx=5, pady=5)

    button = ttk.Button(variables.root, text="Próximo", style='default.TButton',
                        command=lambda: clutches.combat_clutch([variables.enemy], [variables.player]))
    button.grid(row=1, padx=5, pady=50)
