import combat
import variables


def combat_clutch(enemies, agency):
    reset_clutch()
    variables.fight = combat.Battle(enemies, agency)


def reset_clutch():
    for child in variables.root.winfo_children():
        child.destroy()


def shutdown():
    variables.root.destroy()
    quit()


def scene_clutch(scene):
    reset_clutch()
    scene()
