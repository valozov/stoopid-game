import subprocess
import os
from colored import Fore, Style
import creatures as cr
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
    difficulty = input("> ")
    while difficulty not in ["easy", "mid", "hard"]: # input validation
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print(player_info)
        print("eshe raz, sinok")
        print("Choose difficulty:")
        print(f"  {Fore.green}easy{Fore.white}, {Fore.yellow}mid{Fore.white}, {Fore.red}hard{Style.reset}")
        difficulty = input("> ")
    enemy = cr.create_enemy(player.level, difficulty)
    while player.hp > 0 and enemy.hp > 0:
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print(player_info)
        print(f"{Fore.red}Enemy: {Fore.red}{enemy.name}  {Fore.white}HP {Fore.red}{enemy.hp}{Style.reset}/{enemy.max_hp}\n")