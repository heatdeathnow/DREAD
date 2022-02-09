import tkinter as tk
from tkinter import ttk
from random import randint


class Entity:
    def __init__(self, name, max_hp, max_delirium, attack, defense, speed):

        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_delirium = max_delirium
        self.delirium = max_delirium
        self.attack = attack
        self.defense = defense
        self.speed = speed

        self.skills = []


class Player(Entity):

    def __init__(self, name, max_hp, max_delirium, attack, defense, speed, dread):
        super().__init__(name, max_hp, max_delirium, attack, defense, speed)

        self.max_dread = 100
        self.dread = dread

