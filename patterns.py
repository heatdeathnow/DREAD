import tkinter as tk
from tkinter import ttk
from random import randint
import variables


class MatchBar:
    def __init__(self):
        self.end_flag = False
        self.amount = randint(1, 3)
        self.done = 0

        self.bar_frame = ttk.Frame(variables.root)

        # Paralyzed bar to which player must match his
        self.base = randint(60, 90)
        base_bar = ttk.Progressbar(self.bar_frame, length=512, value=self.base)
        base_bar.grid(column=0, row=0, padx=5, pady=5)

        self.score = 0
        self.player_bar = ttk.Progressbar(self.bar_frame, length=512, value=self.score)
        self.player_bar.grid(column=0, row=1, padx=5, pady=5)

        self.button = ttk.Button(variables.root, text='Atacar', style='patterns.TButton',
                                 command=self.start)
        self.button.grid()

        self.invisible_label = ttk.Label(variables.root)

    def start(self):
        self.button['text'] = "Parar"
        self.button['command'] = self.finish

        self.bar_frame.grid(column=0, row=0, padx=5, pady=5, sticky=tk.N)

        self.increase()

    def increase(self):
        if not self.end_flag:
            variables.root.after(1, self.increase)

            self.score += 0.2
            self.player_bar['value'] = self.score
            print("match_bar current value:", self.score, "needed value:", self.base)

    def finish(self):
        self.end_flag = True

        if self.base + 2 > self.score > self.base - 2:
            variables.skill = 1.5
        elif self.base + 7.5 > self.score > self.base - 7.5:
            variables.skill = 1
        elif self.base + 10 > self.score > self.base - 10:
            variables.skill = 0.75
        elif self.base + 15 > self.score > self.base - 15:
            variables.skill = 0.5
        else:
            variables.skill = 0

        print("skill: ", variables.skill)

        self.player_bar.destroy()
        self.bar_frame.destroy()
        self.invisible_label.destroy()
        self.button.destroy()
        variables.fight.reload_window()


class QuickButtons:
    def __init__(self):

        self.amount = randint(5, 7)
        self.count = 1
        self.clicked = 0

        self.button = ttk.Button(variables.root, text='Atacar', style='patterns.TButton', command=self.start)
        self.button.grid()

    def start(self):
        self.button.destroy()
        self.spawn()

    def spawn(self):
        if self.count <= self.amount:
            self.quick_button = ttk.Button(variables.root, width=7, text=f'\n{self.count}\n', style='patterns.TButton',
                                           command=self.pressed)

            # for safety buttons can only spawn between (80, 80) to (620, 370)
            x_position = randint(90, 620)
            y_position = randint(90, 370)

            self.quick_button.place(x=x_position, y=y_position)

            # This is so the timer can be destroyed
            self.timer_label = ttk.Label(variables.root)
            self.timer_label.after(600, self.unpressed)
        else:
            self.finish()

    def pressed(self):
        self.clicked += 1
        self.count += 1
        try:
            self.quick_button.destroy()
            self.timer_label.destroy()
        except (AttributeError, tk.TclError):
            pass
        self.spawn()

    def unpressed(self):
        self.count += 1
        self.quick_button.destroy()
        self.timer_label.destroy()
        self.spawn()

    def finish(self):
        if self.clicked / self.amount == 1:
            variables.skill = 1.5
        elif self.clicked / self.amount >= 0.65:
            variables.skill = 1
        elif self.clicked / self.amount >= 0.5:
            variables.skill = 0.5
        else:
            variables.skill = 0

        print('clicked: ', self.clicked, ", total: ", self.amount,
              '\nskill: ', variables.skill)

        variables.fight.reload_window()


class Sequence:
    def __init__(self):

        self.amount = randint(5, 7)
        self.clicked = 0

        self.button = ttk.Button(variables.root, text='Atacar', style='patterns.TButton', command=self.start)
        self.button.grid()

        self.progress = 1
        self.buttons = []

    def start(self):
        self.button.destroy()

        # The time to finish is based on the amount of buttons created
        variables.root.after(500 * self.amount, self.finish)

        self.spawn()

    def spawn(self):

        taken_up = []
        for count in range(1, self.amount + 1):
            self.buttons.append(ttk.Button(variables.root, width=7, text=f'\n{count}\n', style='patterns.TButton',
                                           command=lambda a=count: self.check(a)))

            flag = True
            while flag:
                # for safety buttons can only spawn between (80, 80) to (620, 370)
                x_position = randint(90, 620)
                y_position = randint(90, 370)

                flag = False
                for space in taken_up:
                    if abs(x_position - space[0]) <= 100 and abs(y_position - space[1]) <= 100:
                        flag = True

                print("Position x:", x_position,
                      "\nPosition y:", y_position,
                      "\ntaken_up:", taken_up)

            # Used to prevent buttons from spawning on top of each other
            taken_up.append((x_position, y_position))

            self.buttons[count - 1].place(x=x_position, y=y_position)

    def check(self, number):
        if number == self.progress:

            count = 0
            for button in self.buttons:
                if int(button['text']) == number:
                    self.buttons[count].destroy()
                    self.buttons.pop(count)
                count += 1
            self.progress += 1
            self.clicked += 1

    def finish(self):
        for button in self.buttons:
            button.destroy()

        if self.clicked / self.amount == 1:
            variables.skill = 1.5
        elif self.clicked / self.amount >= 0.65:
            variables.skill = 1
        elif self.clicked / self.amount >= 0.5:
            variables.skill = 0.5
        else:
            variables.skill = 0

        print('clicked: ', self.clicked, ", total: ", self.amount,
              '\nskill: ', variables.skill)

        variables.fight.reload_window()
