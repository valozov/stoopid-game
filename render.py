import subprocess
import os
from colored import Fore, Style
import creatures as cr
import time
def update_info(player, enemy, time_from_start):
    player = ( # fancy player info
        f"{Fore.cyan}Stoopid Game{Style.reset}\n"
        "========================================================\n"
        f"{Fore.green}Player: {Fore.magenta}{player.name}  "
        f"{Fore.white}HP {Fore.green}{player.hp}{Fore.white}/"
        f"{Fore.green}{player.max_hp}  {Fore.white}Kills: "
        f"{Fore.yellow}{player.kills}  {Fore.white}Level: "
        f"{Fore.blue}{player.level}{Style.reset}\n"
        "========================================================"
    )
    enemy = f"{Fore.white}Enemy: {Fore.red}{enemy.name}  {Fore.white}HP {Fore.red}{enemy.hp}{Style.reset}/{enemy.max_hp}\n--------------------------------------------------------\n{Fore.magenta}Time: {time_from_start:.1f}s{Style.reset}\n--------------------------------------------------------"
def victory(player_info, enemy_info, log):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    print(player_info)
    print(enemy_info)
    print("".join(log))
    print(f"{Fore.green}You win!{Style.reset}")
    input("Press Enter to continue...")

def defeat(player_info, enemy_info, log):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    print(player_info)
    print(enemy_info)
    print("".join(log))
    print(f"{Fore.red}You lose!{Style.reset}")
    input("Press Enter to continue...")

def render_game(player = None, enemy = None):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    
    if not player and not enemy: # input player name
        print(Fore.cyan + "Stoopid Game" + Style.reset)
        print("========================================================")
        print(f"{Fore.green}Player: {Fore.magenta}NaN  {Fore.white}HP {Fore.green}NaN{Fore.white}/"
              f"{Fore.green}NaN  {Fore.white}Kills: {Fore.yellow}NaN  {Fore.white}Level: {Fore.blue}NaN{Style.reset}")
        print("========================================================")
        return
    player_info = ( # fancy player info
        f"{Fore.cyan}Stoopid Game{Style.reset}\n"
        "========================================================\n"
        f"{Fore.green}Player: {Fore.magenta}{player.name}  "
        f"{Fore.white}HP {Fore.green}{player.hp}{Fore.white}/"
        f"{Fore.green}{player.max_hp}  {Fore.white}Kills: "
        f"{Fore.yellow}{player.kills}  {Fore.white}Level: "
        f"{Fore.blue}{player.level}{Style.reset}\n"
        "========================================================"
    )
    print(player_info)
    print("Choose difficulty:")
    print(f"  {Fore.green}easy{Fore.white}, {Fore.yellow}mid{Fore.white}, {Fore.red}hard{Style.reset}")
    difficulty = input("> ") # input difficulty
    while difficulty not in ["easy", "mid", "hard"]: # input validation
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print(player_info)
        print("eshe raz, sinok")
        print("Choose difficulty:")
        print(f"  {Fore.green}easy{Fore.white}, {Fore.yellow}mid{Fore.white}, {Fore.red}hard{Style.reset}")
        difficulty = input("> ")
    enemy = cr.create_enemy(player.level, difficulty)
    time_from_start = 0
    last_time = time.time()
    enemy_info = f"{Fore.white}Enemy: {Fore.red}{enemy.name}  {Fore.white}HP {Fore.red}{enemy.hp}{Style.reset}/{enemy.max_hp}\n--------------------------------------------------------\n{Fore.magenta}Time: {time_from_start:.1f}s{Style.reset}\n--------------------------------------------------------"
    log = [f"{Fore.cyan}A bizzare {enemy.name} appears!{Style.reset}\n"]
    while player.hp > 0 and enemy.hp > 0: # combat loop
        if len(log) > 10: # log limit
            log.pop(0)
        now = time.time()

        delta = now - last_time
        last_time = now
        if(result := player.update(delta, enemy)):
            log.append(result)
        if(enemy.hp <= 0):
            victory(player_info, enemy_info, log)
            break
        if(result := enemy.update(delta, player)):
            log.append(result)
        if(player.hp <= 0):
            defeat(player_info, enemy_info, log)
            break
        update_info(player, enemy, time_from_start)
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print(player_info, enemy_info, "".join(log))
        time.sleep(0.1)


        