import tkinter as tk
from tkinter import ttk
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
