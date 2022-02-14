import random
import tkinter as tk
from tkinter import ttk

import clutches
import variables
import scenes
import patterns
from math import floor, ceil


class Battle:

    def __init__(self, enemies, agency):

        self.n_attacks = 1
        self.n_attack = 1
        self.end_state = 0

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

        # Matches order of enemies with order
        self.enemies.clear()
        for entity in self.order:
            try:
                entity.dread
            except AttributeError:
                self.enemies.append(entity)

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

        self.n_attack, self.n_attacks = 1, 1  # Resets multiple attacks

        if self.current == len(self.order):  # Loops the fight back around
            self.current, who = 0, 0

        for one in self.frame_order:  # Toggles back everyone to inactive background
            one.configure(style='default.TFrame')

        try:  # Recreates action_bar in case if the player returns to menu
            self.action_bar.destroy()
        except AttributeError:
            pass

        self.action_bar = ttk.Frame(variables.root)

        # Checks if the battle is over
        if not self.agency:  # Checks if all playable characters are dead
            self.end_state = -1
        elif not self.enemies:
            self.end_state = 1

        if self.end_state == 0:
            try:
                self.order[who].dread
            except AttributeError:
                next_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                         command=self.enemy_decide)
                next_button.grid(row=0, padx=5)
            else:
                attack_button = ttk.Button(self.action_bar, text='Atacar', style='default.TButton',
                                           command=self.agent_choose_move)
                attack_button.grid(column=0, row=0, padx=5)

                item_button = ttk.Button(self.action_bar, text='Itens', style='default.TButton',)
                item_button.grid(column=1, row=0, padx=5)

                defend_button = ttk.Button(self.action_bar, text='Defender', style='default.TButton',
                                           command=self.enemy_decide)
                defend_button.grid(column=2, row=0, padx=5)
            self.desc_label['text'] = f'É o turno de {self.order[who].name}'
        elif self.end_state == -1:
            next_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                     command=clutches.shutdown)
            next_button.grid(row=0, padx=5)
            self.desc_label['text'] = f'Batalha perdida!'
        elif self.end_state == 1:
            next_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                     command=lambda: clutches.scene_clutch(scenes.survival))
            next_button.grid(row=0, padx=5)
            self.desc_label['text'] = f'Batalha vencida!'

        self.frame_order[who].configure(style='selected.TFrame')

        self.action_bar.grid(row=3, pady=10)

    def enemy_decide(self, attack_again_flag=False):  # Decides the move and the target

        self.action_bar.destroy()
        self.action_bar = ttk.Frame(variables.root)

        num = len(self.order[self.current].skills)
        choose = random.randint(0, num - 1)
        self.selected_move = self.order[self.current].skills[choose]

        if not attack_again_flag:
            num = len(self.agency)
            choose = random.randint(0, num - 1)
            self.target = self.agency[choose]
            self.attack()
        else:
            self.n_attack += 1

            self.desc_label['text'] = f"{self.selected_move.owner.name} é muito rápido! Ele ataca de novo!"
            speed_button = ttk.Button(self.action_bar, text="Próximo", style='default.TButton',
                                      command=self.attack)
            speed_button.grid(padx=5)
            self.action_bar.grid(row=3, pady=10)

    def attack(self):
        print("Attacker order: ", self.current)
        self.action_bar.destroy()

        damage, description = self.selected_move.damage(self.target)
        print("damage: ", damage, " done by ", self.selected_move.owner.name)

        # Checks if it's a critical hit
        if variables.skill == 1.5:
            if damage == 0:
                description = f"É um ótimo ataque!" \
                              f"\nPorém não é o suficiente para ferir {self.target.name}"
                difference = self.target.defense * 2 - self.selected_move.owner.attack
                if difference <= 0: difference = 1
                self.selected_move.owner.dread -= random.randint(1, difference)
            else:
                description += "\nÉ um ótimo ataque!"
                self.selected_move.owner.dread -= random.randint(1, ceil(damage / 2))
                if self.selected_move.owner.dread < 0: self.selected_move.owner.dread = 0

        self.desc_label['text'] = description
        self.target.hp -= damage
        if self.target.hp < 0: self.target.hp = 0

        # updates the health bar of the receiver and possibly the DL bar of attacker
        # and removes from frame_order and order in case of death
        count = 0
        for entity in self.order:
            if entity == self.target or entity == self.selected_move.owner:
                self.frame_order[count].toggle()
                if entity.hp == 0:
                    self.frame_order.pop(count)
                    self.order.pop(count)

                    count1 = 0
                    for enemy in self.enemies:
                        if enemy == entity:
                            self.enemies.pop(count1)
                        count1 += 1

                    count1 = 0
                    for agent in self.agency:
                        if agent == entity:
                            self.agency.pop(count1)
                        count1 += 1

                    # Corrects the order of turns because of the new missing enemy
                    self.current -= 1
                    if self.current < 0: self.current = len(self.order) - 1
            count += 1

        self.action_bar = ttk.Frame(variables.root)

        # Makes sure the critical hit check doesn't break (only players can change this value)
        variables.skill = 0

        # Checks if attacker's speed is higher than a multiple of any opponents', if so, allowing them to act again
        if self.n_attacks == 1:
            self.n_attacks = floor(self.selected_move.owner.speed / self.target.speed)
            if self.n_attacks < 1: self.n_attacks = 1
        try:
            self.selected_move.owner.dread
            if self.n_attack != self.n_attacks:
                ok_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                       command=lambda: self.agent_choose_move(True))
            else:
                self.current += 1
                ok_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                       command=lambda: self.turn(self.current))
        except AttributeError:
            if self.n_attack != self.n_attacks:
                ok_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                       command=lambda: self.enemy_decide(True))
            else:
                self.current += 1
                ok_button = ttk.Button(self.action_bar, text='Próximo', style='default.TButton',
                                       command=lambda: self.turn(self.current))

        ok_button.grid()
        self.action_bar.grid(row=3, pady=10)

    def agent_choose_move(self, attack_again_flag=False):
        print('DREAD: ', self.order[self.current].dread)

        self.action_bar.destroy()

        self.action_bar = ttk.Frame(variables.root)
        count = 0
        buttons = []
        for move in self.order[self.current].skills:
            if attack_again_flag:
                buttons.append(ttk.Button(self.action_bar, text=move.name, style='default.TButton',
                                          command=lambda a=move: self.agent_move_done(a, True)))
            else:
                buttons.append(ttk.Button(self.action_bar, text=move.name, style='default.TButton',
                                          command=lambda a=move: self.agent_move_done(a)))
            buttons[count].grid(row=0, column=count, padx=5, pady=5)
            count += 1

        while count < 4:
            buttons.append(ttk.Button(self.action_bar, text="Vazio", style='default.TButton'))
            buttons[count].grid(row=0, column=count, padx=5, pady=5)
            count += 1

        if not attack_again_flag:
            buttons.append(ttk.Button(self.action_bar, text="Retornar", style='default.TButton',
                                      command=lambda: self.turn(self.current)))
            buttons[count].grid(row=0, column=count, padx=5, pady=5)
        else:
            self.desc_label['text'] = f"{self.selected_move.owner.name} é muito rápido! Ele ataca de novo!"

        self.action_bar.grid(row=3, pady=10)

    def agent_move_done(self, move, attack_again_flag=False):
        self.selected_move = move

        if not attack_again_flag:
            self.agent_choose_target()
        else:
            self.n_attack += 1
            self.skill_check()

    def agent_choose_target(self):
        self.action_bar.destroy()

        self.action_bar = ttk.Frame(variables.root)
        count = 0
        targets = []
        for target in self.enemies:
            targets.append(ttk.Button(self.action_bar, text=target.name, style='default.TButton',
                                      command=lambda a=target: self.agent_target_done(a)))
            targets[count].grid(row=0, column=count, padx=5, pady=5)
            count += 1

        targets.append(ttk.Button(self.action_bar, text="Voltar", style='default.TButton',
                                  command=self.agent_choose_move))
        targets[count].grid(row=0, column=count, padx=5, pady=5)

        self.action_bar.grid(row=3, pady=10)

    def agent_target_done(self, target):
        self.target = target
        self.skill_check()

    def skill_check(self):
        self.enemies_frame.grid_forget()
        self.agency_frame.grid_forget()
        self.desc_label.grid_forget()
        try:
            self.action_bar.grid_forget()
        except AttributeError:
            pass

        rand = random.random()

        if 0 <= rand <= 0.33:
            self.skill_object = patterns.MatchBar()
        elif 0.33 < rand <= 0.66:
            self.skill_object = patterns.QuickButtons()
        else:
            self.skill_object = patterns.Sequence()

    def reload_window(self):
        self.enemies_frame.grid(row=0, sticky=tk.N)
        self.agency_frame.grid(row=2, sticky=tk.S)
        self.desc_label.grid(row=1, pady=100)
        self.attack()
