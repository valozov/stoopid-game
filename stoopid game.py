import creatures as cr
import items as it
import render as rd

rd.render_game()

player = cr.Hero(input("chmo, day imya\n> "), 10, 10)
start_weapon = it.Weapon("sword", 10, 0.5)
player.equipment["weapon"] = start_weapon
enemy = None

while player.hp > 0:
    rd.render_game(player, enemy)
