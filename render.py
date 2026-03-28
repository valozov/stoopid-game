import os
import subprocess
import time
from colored import Fore, Style

import creatures as cr


def battle(player_info, player):
    difficulty = choose_difficulty(player_info)
    enemy = cr.create_enemy(player.level, difficulty)
    time_from_start = 0
    last_time = time.time()
    log = [f"{Fore.cyan}A bizzare {enemy.name} appears!{Style.reset}\n"]

    while player.hp > 0 and enemy.hp > 0:  # combat loop
        while len(log) > 5:  # log limit
            log.pop(0)

        now = time.time()
        delta = now - last_time
        last_time = now
        time_from_start += delta

        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

        if (result := player.update(delta, enemy)):
            log.append(result)
            if (enemy.hp <= 0):
                temp = player.kill(enemy, difficulty)
                victory(update_info(player, enemy, time_from_start), log, temp)
                return

        if (result := enemy.update(delta, player)):
            log.append(result)
            if (player.hp <= 0):
                defeat(update_info(player, enemy, time_from_start), log)
                return

        print(update_info(player, enemy, time_from_start) + "".join(log))

        time.sleep(0.1)


def update_info(player, enemy, time_from_start):
    return (  # fancy player info
        f"{Fore.cyan}Stoopid Game{Style.reset}\n"
        "========================================================\n"
        f"{Fore.green}Player: {Fore.magenta}{player.name}  "
        f"{Fore.white}HP {Fore.green}{player.hp:.1f}{Fore.white}/"
        f"{Fore.green}{player.max_hp:<5.1f}  {Fore.white}Kills: "
        f"{Fore.yellow}{player.kills}  {Fore.white}Level: "
        f"{Fore.blue}{player.level}{Style.reset}\n"
        "========================================================\n"
        f"{Fore.white}Enemy: {Fore.red}{enemy.name}  "
        f"{Fore.white}HP {Fore.red}{enemy.hp:.1f}{Style.reset}/{enemy.max_hp:<5.1f}\n"
        "--------------------------------------------------------\n"
        f"{Fore.magenta}Time: {time_from_start:.1f}s{Style.reset}\n"
        "--------------------------------------------------------\n"
    )


def victory(info, log, level_up: str = None):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    print(info + "".join(log) +
          f"{Fore.green}You win!{Style.reset}")
    if level_up:
        print(level_up)
    input("Press Enter to continue...")


def defeat(info, log):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    print(info + "".join(log) +
          f"{Fore.red}You lose!{Style.reset}")
    input("Press Enter to continue...")


def choose_difficulty(player_info):
    print("Choose difficulty:")
    print(f"  {Fore.green}easy{Fore.white}, "
          f"{Fore.yellow}mid{Fore.white}, "
          f"{Fore.red}hard{Style.reset}")
    difficulty = input("> ")   # input difficulty

    while difficulty not in ["easy", "mid", "hard"]:  # input validation
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print(player_info)
        print("eshe raz, sinok")
        print("Choose difficulty:")

        print(f"  {Fore.green}easy{Fore.white}, "
              f"{Fore.yellow}mid{Fore.white}, "
              f"{Fore.red}hard{Style.reset}")

        difficulty = input("> ")
    return difficulty


def render_game(player=None, enemy=None):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    if not player:  # input player name
        print(Fore.cyan + "Stoopid Game" + Style.reset)
        print("========================================================")
        print(f"{Fore.green}Player: {Fore.magenta}NaN  {Fore.white}HP {Fore.green}NaN{Fore.white}/"
              f"{Fore.green}NaN  {Fore.white}Kills: {Fore.yellow}NaN  {Fore.white}Level: {Fore.blue}NaN{Style.reset}")
        print("========================================================")
        return

    player_info = (  # fancy player info
        f"{Fore.cyan}Stoopid Game{Style.reset}\n"
        "========================================================\n"
        f"{Fore.green}Player: {Fore.magenta}{player.name}  "
        f"{Fore.white}HP {Fore.green}{player.hp:.1f}{Fore.white}/"
        f"{Fore.green}{player.max_hp:<5.1f}  {Fore.white}Kills: "
        f"{Fore.yellow}{player.kills}  {Fore.white}Level: "
        f"{Fore.blue}{player.level}{Style.reset}\n"
        "========================================================"
    )
    print(player_info)

    battle(player_info, player)
    
