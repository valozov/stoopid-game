import random
from colored import Fore, Style

from items import Armor, Weapon


class Creature:
    def __init__(self,
                 name: str,
                 agility: int,
                 strength: int,
                 weapon: Weapon = None,
                 shield: Armor = None,
                 helmet: Armor = None,
                 chest: Armor = None,
                 boots: Armor = None) -> None:
        self.name = name
        self.agility = agility
        self.strength = strength
        self.equipment = {
            "weapon": weapon,
            "shield": shield,
            "helmet": helmet,
            "chest": chest,
            "boots": boots
        }

        self.hp = self.max_hp
        self.attack_timer = 0

    @property
    def bonus_hp(self):
        return sum(getattr(i, "hp", 0) for i in self.equipment.values() if i)

    @property
    def max_hp(self):
        return self.strength * 8 + self.bonus_hp

    @property
    def real_armor(self):
        return sum(getattr(i, "armor", 0) for i in self.equipment.values() if i)

    @property
    def equip_block(self):
        shield_block = getattr(self.equipment.get("shield"), "block_chance", 0) if self.equipment.get("shield") else 0
        armor_block = sum(getattr(i, "block_chance", 0) for i in [self.equipment.get("helmet"), self.equipment.get("chest"), self.equipment.get("boots")] if i)
        return armor_block * 0.05 + shield_block * 0.25

    @property
    def real_dmg(self):
        weapon_dmg = self.equipment["weapon"].dmg if self.equipment["weapon"] else 0
        return self.strength / 2 + weapon_dmg

    @property
    def real_speed(self):
        weapon_speed = self.equipment["weapon"].speed if self.equipment["weapon"] else 0
        return self.agility / 6 + weapon_speed

    @property
    def block_chance(self):
        return min(2.0 + self.equip_block + (self.agility / (self.agility + 200.0)) * 40, 50)

    @property
    def block_power(self):
        return 0.25 + (self.strength / (self.strength + 100.0)) * 0.45

    @property
    def evade_chance(self):
        return min(2.0 + (self.agility / (self.agility + 100.0)) * 60, 60)

    def update(self, delta_time, target) -> str | None:
        self.attack_timer += delta_time
        cooldown = 1 / self.real_speed

        if self.attack_timer >= cooldown:
            self.attack_timer -= cooldown
            return self.attack(target)

    def attack(self, enemy) -> str:
        dmg = self.real_dmg * random.uniform(0.9, 1.1)

        if random.random() < enemy.evade_chance / 100.0:
            return f"{Fore.green}{self.name}{Style.reset} atakoval {Fore.red}{enemy.name}{Style.reset}, no on uvernulsya\n"

        if random.random() < enemy.block_chance / 100.0:
            dmg = max(dmg - dmg * enemy.block_power, 0)

            enemy.hp -= dmg
            if enemy.hp < 0:
                enemy.hp = 0

            return (f"{Fore.green}{enemy.name}{Style.reset} zablokiroval {Fore.yellow}{dmg * enemy.block_power:.1f}{Style.reset} " +
                    f"damage, poluchil {Fore.yellow}{dmg:.1f}{Style.reset} damage\n")

        enemy.hp -= dmg
        if enemy.hp < 0:
            enemy.hp = 0

        return (f"{Fore.green}{self.name}{Style.reset} atakoval {Fore.red}"
                f"{enemy.name}{Style.reset} i nanes {Fore.yellow}{dmg:.1f}"
                f" damaga{Style.reset}\n")


class Enemy(Creature):
    # no equipment for enemy, too lazy
    pass


class Hero(Creature):
    def __init__(self,
                 name: str,
                 agility: int,
                 strength: int,
                 weapon: Weapon = None,
                 helmet: Armor = None,
                 chest: Armor = None,
                 boots: Armor = None) -> None:
        super().__init__(name, agility, strength, weapon, helmet, chest, boots)
        self.kills = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 10
        self.inventory = {}

    def kill(self, enemy, current_difficulty):
        self.kills += 1
        current_difficulty = {"easy": 0.5, "mid": 0.75, "hard": 1.0}[current_difficulty]
        self.exp += self.level * current_difficulty * 10 + (enemy.agility + enemy.strength) / 5
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.strength *= 1.1
        self.agility *= 1.1
        self.hp = self.max_hp
        return f"{self.name} reached level {self.level}!"


def show_equipment(player) -> None:
    print("================choo nadel================")
    for slot, item in player.equipment.items():
        if item:
            print(f"{slot}: {item.name}")
    choose = input("cho delaesh?\n")
    if choose == "nicho":
        return


def scale_stat(base_stat, difficulty, hero_level) -> float:
    multipliers = {"easy": 0.8, "mid": 1.0, "hard": 1.2}
    hero_multiplier = 1 + (hero_level - 1) * 0.1
    return float(base_stat * multipliers[difficulty] * hero_multiplier)


def create_enemy(level=1, difficulty="mid") -> Enemy:
    name = random.choice(ENEMY_NAMES)
    base_agility = random.randint(5, 15)
    base_strength = random.randint(5, 15)

    agility = scale_stat(base_agility, difficulty, level)
    strength = scale_stat(base_strength, difficulty, level)
    return Enemy(name, agility, strength)


ENEMY_NAMES = ["Vanya", "Чебурашка(Лего фильтр)", "Gomosek", "Rostik", "Jirniy", "Pisya", "Chmo",
               "Loser", "Suka", "Pidor", "Durak>-<", "Kozel", "Shlyapa",
               "Zadrot", "Blin", "Pizda"]
ELITE_ENEMY_NAMES = ["Hitler", "Nastya", "Putin", "Trump", "Zelenskiy",
                     "Biden", "Medvedev", "Navalniy", "Stalin", "Lenin",
                     "Gorbachev", "Brezhnev", "Khrushchev", "Yeltsin",
                     "Kim Chen In", "Mellstroy"]
