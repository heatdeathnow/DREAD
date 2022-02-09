import tkinter as tk
from tkinter import ttk
from random import randint
import entities


class Move:
    def __init__(self, single, owner, name, dl_cost):

        self.single = single
        self.owner = owner
        self.name = name
        self.dl_cost = dl_cost


# Ataque básico que todas as entidades vão ter e que não é possível remover.
# Dano baseado na força do dono e na defesa do oponente.
class Melee(Move):
    def __init__(self, owner):
        super().__init__(True, owner, 'Socão', 0)

    def damage(self, opponent):
        random_part = round(randint(0, round(self.owner.attack / 4)))  # dano extra aleatório de 0 até 1/4 do ataque
        damage = self.owner.attack - opponent.defense + random_part

        damage = apply_multiplier(self, opponent, damage)

        if damage < 0: damage = 0

        # Increases dread if it's a player being attacked based on how much stronger the enemy is
        try:
            difference = self.owner.attack - opponent.attack
            if difference <= 0: difference = 1

            opponent.dread += randint(1, difference)
        except AttributeError:
            pass

        if damage == 0:
            try:
                battle_description = f'{self.owner.name} é muito fraco para dar algum dano!\n' \
                                     f'Que fracasso!'
                self.owner.dread += randint(1, 10)
            except AttributeError:
                battle_description = f'{self.owner.name} acerta {opponent.name}, mas não o fere'
        else:
            battle_description = f'{self.owner.name} soca {opponent.name}!'

        return damage, battle_description


class Tackle(Move):
    def __init__(self, owner):
        super().__init__(True, owner, 'Encontrão', 10)

    def damage(self, opponent):

        if self.owner.delirium < self.dl_cost:
            battle_description = f'{self.owner.name} tenta jogar o seu corpo contra o oponente,\n' \
                                 f'mas sente-se sem motivação!'
            return 0, battle_description
        else:
            self.owner.delirium -= self.dl_cost
            random_part = round(randint(0, round((self.owner.attack + self.owner.speed) / 4)))
            damage = self.owner.attack + self.owner.speed - opponent.defense + random_part

            damage = apply_multiplier(self, opponent, damage)

            # Increases dread if it's a player being attacked based on how much stronger or faster the enemy is.
            try:
                difference = self.owner.attack - opponent.attack
                if (self.owner.speed - opponent.speed) > difference:
                    difference = self.owner.speed - opponent.speed
                elif difference <= 0: difference = 1

                opponent.dread += randint(1, difference)
            except AttributeError:
                pass

            if damage == 0:
                try:
                    battle_description = f'{self.owner.name} é muito fraco para dar algum dano!\n' \
                                         f'Que fracasso!'
                    self.owner.dread += randint(1, 10)
                except AttributeError:
                    battle_description = f'{self.owner.name} joga seu corpo contra {opponent.name},\n' \
                                         f'mas não o fere'
            else:
                battle_description = f'{self.owner.name} joga o seu corpo contra {opponent.name}!'

            return damage, battle_description


def apply_multiplier(self, opponent, damage):
    try:  # if it's an enemy attacking
        multiplier = (opponent.dread + 100) / 100
    except AttributeError:  # if it's the player attacking
        multiplier = (100 - self.owner.dread) / 100

    return round(damage * multiplier)
