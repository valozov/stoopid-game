import random
from colored import Fore, Style
class Creature:
    def __init__(self, name, agility, strength, weapon=None, helmet=None, chest=None, boots=None):
        self.name = name
        self.agility = agility
        self.strength = strength
        self.equipment = {
            "weapon": weapon,
            "helmet": helmet,
            "chest": chest,
            "boots": boots
        }
        self.hp = self.max_hp
        self.attack_timer = 0
    def update(self, delta_time, target):
        self.attack_timer += delta_time
        cooldown = 1 / self.real_speed

        if self.attack_timer >= cooldown:
            self.attack_timer -= cooldown
            return self.attack(target)
    def attack(self, enemy):
        r_dmg = max(self.real_dmg - enemy.real_armor, 0)
        enemy.hp -= r_dmg
        return f"{Fore.green}{self.name}{Style.reset} atakoval {Fore.red}{enemy.name}{Style.reset} i nanes {Fore.yellow}{r_dmg:.1f} damaga{Style.reset}\n"
    @property
    def bonus_hp(self):
        return sum(getattr(i, "hp", 0) for i in self.equipment.values() if i)
    @property
    def max_hp(self):
        return self.strength * 10 + self.bonus_hp
    @property
    def bonus_armor(self):
        return sum(getattr(i, "armor", 0) for i in self.equipment.values() if i)
    @property
    def real_armor(self):
        return self.agility / 6 + self.bonus_armor
    @property
    def real_dmg(self):
        weapon_dmg = self.equipment["weapon"].dmg if self.equipment["weapon"] else 0
        return (self.strength + self.agility)/2 + weapon_dmg
    @property
    def real_speed(self):
        weapon_speed = self.equipment["weapon"].speed if self.equipment["weapon"] else 0
        return self.agility/6 + weapon_speed

class Enemy(Creature):
    # no equipment for enemy, too lazy
    pass

class Hero(Creature):
    def __init__(self, name, agility, strength, weapon=None, helmet=None, chest=None, boots=None):
        super().__init__(name, agility, strength, weapon, helmet, chest, boots)
        self.kills = 0
        self.level = 1
        self.inventory = {}

    def take_damage(self, enemy):
        self.hp -= max(enemy.real_dmg - self.real_armor, 0)
        print(f"ti poluchil {enemy.real_dmg} damaga, u tya {self.hp} hp")

def show_equipment(player):
    print("================choo nadel================")
    for slot, item in player.equipment.items():
        if item:
            print(f"{slot}: {item.name}")
    choose = input("cho delaesh?\n")
    if choose == "nicho":
        return

def scale_stat(base_stat, difficulty, hero_level):
    multipliers = {"easy": 0.8, "mid": 1.0, "hard": 1.2}
    hero_multiplier = 1 + (hero_level - 1) * 0.1
    return int(base_stat * multipliers[difficulty] * hero_multiplier) 

def create_enemy(level=1, difficulty="mid"):
    name = random.choice(ENEMY_NAMES)
    base_agility = random.randint(5, 15)
    base_strength = random.randint(5, 15)

    agility = scale_stat(base_agility, difficulty, level)
    strength = scale_stat(base_strength, difficulty, level)
    return Enemy(name, agility, strength)

ENEMY_NAMES = ["Vanya", "Gomosek", "Rostik", "Jirniy", "Pisya", "Chmo", "Loser", "Suka", "Pidor", "Durak>-<", "Kozel", "Shlyapa", "Zadrot", "Blin", "Pizda"]
ELITE_ENEMY_NAMES = ["Hitler", "Nastya", "Putin", "Trump", "Zelenskiy", "Biden", "Medvedev", "Navalniy", "Stalin", "Lenin", "Gorbachev", "Brezhnev", "Khrushchev", "Yeltsin", "Kim Chen In", "Mellstroy"]
