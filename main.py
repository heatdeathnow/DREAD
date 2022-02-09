import entities
import moves
import scenes
import variables
import combat

player = entities.Player('Char', 50, 50, 5, 5, 3, 0)
player.skills.append(moves.Melee(player))
player.skills.append(moves.Tackle(player))

spectre1 = entities.Entity('Spectre', 20, 50, 5, 5, 2)
spectre1.skills.append(moves.Melee(spectre1))
spectre1.skills.append(moves.Tackle(spectre1))

spectre2 = entities.Entity('Spectre', 20, 50, 5, 5, 2)
spectre2.skills.append(moves.Melee(spectre2))
spectre2.skills.append(moves.Tackle(spectre2))

spectre3 = entities.Entity('Spectre', 20, 50, 5, 5, 2)
spectre3.skills.append(moves.Melee(spectre3))
spectre3.skills.append(moves.Tackle(spectre3))

combat.Battle([spectre1, spectre2, spectre3], [player])

variables.root.mainloop()
