import random
import tkinter as tk
from tkinter import ttk
import variables
import scenes


class Battle:

    def __init__(self, enemies, agency):

        # Styles for the background of active and inactive fighters
        self.active_style = ttk.Style()
        self.active_style.configure('gray.TFrame', background='gray')
        self.inactive_style = ttk.Style()
        self.inactive_style.configure('white.TFrame', background='white')

        self.enemies = enemies
        self.agency = agency
        self.target = None
        self.selected_move = None

        self.desc_label = ttk.Label(variables.root)
        self.desc_label.grid(row=1, pady=100)

        # Orders the entities by speed - attack order
        self.order = []
        self.order += enemies[:]
        self.order += agency[:]
        self.order.sort(reverse=True, key=lambda entity: entity.speed)
        self.current = 0

        # This will be used to match the frames with the entities.
        self.frame_order = []
        for num in range(0, len(self.order)):
            self.frame_order.append(None)

        # Organizes the layout of the window.
        count = 0
        self.enemies_frame = ttk.Frame(variables.root)
        for enemy in self.enemies:

            # This synchronizes the frames and the entity-objects.
            sync_order = 0
            for order in self.order:
                if order == enemy: break
                sync_order += 1

            self.frame_order[sync_order] = scenes.CombatInfo(enemy, self.enemies_frame)
            self.frame_order[sync_order].grid(column=count, row=0, padx=5, pady=5, sticky=tk.N)

            count += 1

        # Same thing for player entities
        count = 0
        self.agency_frame = ttk.Frame(variables.root)
        for agent in self.agency:

            sync_order = 0
            for order in self.order:
                if order == agent: break
                sync_order += 1

            self.frame_order[sync_order] = scenes.CombatInfo(agent, self.agency_frame)
            self.frame_order[sync_order].grid(column=count, row=0, padx=5, pady=5, sticky=tk.N)

            count += 1

        self.enemies_frame.grid(row=0, sticky=tk.N)
        self.agency_frame.grid(row=2, sticky=tk.S)

        self.turn(self.current)

    # Checks to see if it's turn of a agent or an NPC, grays out the background of the one whose it's the turn.
    # Gives different options to proceed depending if its a agent or not.
    def turn(self, who):

        # Loops the fight back around
        if self.current == len(self.order):
            self.current, who = 0, 0

        # Toggles back everyone to inactive background
        for one in self.frame_order:
            one.configure(style='white.TFrame')

        # Recreates action_bar in case if the player returns to menu
        try:
            self.action_bar.destroy()
        except AttributeError:
            pass

        self.action_bar = ttk.Frame(variables.root)
        try:
            self.order[who].dread
        except AttributeError:
            next_button = ttk.Button(self.action_bar, text='Próximo', command=self.enemy_decide)
            next_button.grid(row=0, padx=5)
        else:
            attack_button = ttk.Button(self.action_bar, text='Atacar', command=self.agent_choose_move)
            attack_button.grid(column=0, row=0, padx=5)

            item_button = ttk.Button(self.action_bar, text='Itens')
            item_button.grid(column=1, row=0, padx=5)

            defend_button = ttk.Button(self.action_bar, text='Defender', command=self.enemy_decide)
            defend_button.grid(column=2, row=0, padx=5)
        self.desc_label['text'] = f'É o turno de {self.order[who].name}'

        self.frame_order[who].configure(style='gray.TFrame')

        self.action_bar.grid(row=3, pady=10)

    def enemy_decide(self):  # Decides the move and the target

        num = len(self.order[self.current].skills)
        choose = random.randint(0, num - 1)
        self.selected_move = self.order[self.current].skills[choose]

        num = len(self.agency)
        choose = random.randint(0, num - 1)
        self.target = self.agency[choose]

        self.attack()

    def attack(self):
        self.action_bar.destroy()
        style = ttk.Style()
        style.configure('white.TFrame', background='white')

        damage, description = self.selected_move.damage(self.target)
        print("damage: ", damage, " done by ", self.selected_move.owner.name)

        self.desc_label['text'] = description
        self.target.hp -= damage
        if self.target.hp < 0: self.target.hp = 0

        # updates the health bar of the receiver
        count = 0
        for entity in self.order:
            if entity == self.target or entity == self.selected_move.owner:
                self.frame_order[count].toggle()
            count += 1

        self.current += 1
        self.action_bar = ttk.Frame(variables.root)
        ok_button = ttk.Button(self.action_bar, text='Próximo', command=lambda: self.turn(self.current))
        ok_button.grid()
        self.action_bar.grid(row=3, pady=10)

    def agent_choose_move(self):
        self.action_bar.destroy()

        self.action_bar = ttk.Frame(variables.root)
        count = 0
        buttons = []
        for move in self.order[self.current].skills:
            buttons.append(ttk.Button(self.action_bar, text=move.name,
                                      command=lambda a=move: self.agent_move_done(a)))
            buttons[count].grid(row=0, column=count, padx=5, pady=5)
            count += 1

        while count < 4:
            buttons.append(ttk.Button(self.action_bar, text="Vazio"))
            buttons[count].grid(row=0, column=count, padx=5, pady=5)
            count += 1
        buttons.append(ttk.Button(self.action_bar, text="Retornar",
                                  command=lambda: self.turn(self.current)))
        buttons[count].grid(row=0, column=count, padx=5, pady=5)

        self.action_bar.grid(row=3, pady=10)

    def agent_move_done(self, move):
        self.selected_move = move
        self.agent_choose_target()

    def agent_choose_target(self):
        self.action_bar.destroy()

        self.action_bar = ttk.Frame(variables.root)
        count = 0
        targets = []
        for target in self.enemies:
            targets.append(ttk.Button(self.action_bar, text=target.name,
                                      command=lambda: self.agent_target_done(target)))
            targets[count].grid(row=0, column=count, padx=5, pady=5)
            count += 1

        self.action_bar.grid(row=3, pady=10)

    def agent_target_done(self, target):
        self.target = target
        self.attack()
