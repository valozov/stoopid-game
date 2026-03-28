class Item:
    def __init__(self, name, count) -> None:
        self.name = name
        self.count = count


class Weapon(Item):
    def __init__(self, name, dmg, speed, count=1) -> None:
        super().__init__(name, count)
        self.dmg = dmg
        self.speed = speed


class Armor(Item):
    def __init__(self, name, armor, hp, bonus_agility, bonus_strength, count=1) -> None:
        super().__init__(name, count)
        self.armor = armor
        self.hp = hp
        self.bonus_agility = bonus_agility
        self.bonus_strength = bonus_strength


class Consumable(Item):
    def __init__(self, name, heal, count=1) -> None:
        super().__init__(name, count)
        self.heal = heal
