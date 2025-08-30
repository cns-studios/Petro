import sys
import json
import random
from assets.pets import all_pet_stats, common_pets, rare_pets, legendary_pets, pet_levels

class Game:
    def __init__(self):
        self.money = 50000
        self.stage = 1
        self.inventory = ["Worm"]
        self.shop_refresh_price = 5
        self.upgrade_pack = 0
        self.legendary_upgrade_pack = 0
        self.charakter_pack = 0
        self.buff_pack = 0
        self.pending_buff_choices = []
        self.reroll_shop()

    def roll_packs(self, anzahl, chance):
        return sum(1 for _ in range(anzahl) if random.randint(0, chance) == 1)

    def reroll_shop(self):
        self.upgrade_pack = self.roll_packs(10, 2)
        self.legendary_upgrade_pack = self.roll_packs(5, 20)
        self.charakter_pack = self.roll_packs(3, 9)
        self.buff_pack = self.roll_packs(10, 2)

    def get_state(self, message=""):
        inventory_details = []
        for pet_name in self.inventory:
            if pet_name in all_pet_stats:
                stats = all_pet_stats[pet_name]
                inventory_details.append({
                    "name": pet_name,
                    "level": pet_levels.get(pet_name, 1),
                    "attack": stats.get("attack"),
                    "hp": stats.get("hp"),
                    "rarity": stats.get("rarity"),
                    "dodge_chance": stats.get("dodge_chance")
                })

        return {
            "money": self.money,
            "stage": self.stage,
            "inventory": inventory_details,
            "shop": {
                "upgrade_pack": self.upgrade_pack,
                "buff_pack": self.buff_pack,
                "charakter_pack": self.charakter_pack,
                "legendary_upgrade_pack": self.legendary_upgrade_pack,
                "shop_refresh_price": self.shop_refresh_price,
            },
            "pending_buff_choices": self.pending_buff_choices,
            "message": message
        }

    def apply_buff(self, buff_id):
        message = f"Applied buff: "
        if buff_id == 1:
            message += "+1 Attack for all Pets"
            for pet in self.inventory: all_pet_stats[pet]["attack"] += 1
        elif buff_id == 2:
            message += "+1 HP for all Pets"
            for pet in self.inventory: all_pet_stats[pet]["hp"] += 1
        elif buff_id == 3:
            message += "+2% Dodge Chance for all Pets"
            for pet in self.inventory: all_pet_stats[pet]["dodge_chance"] += 2
        elif buff_id == 13:
            message += "+1 Level for all Pets"
            for pet in self.inventory:
                if pet in pet_levels:
                    pet_levels[pet] += 1
                    all_pet_stats[pet]["attack"] += all_pet_stats[pet]["rarity"]
                    all_pet_stats[pet]["hp"] += all_pet_stats[pet]["rarity"]
        self.pending_buff_choices = []
        return message

    def process_command(self, command):
        parts = command.strip().lower().split()
        action = parts[0] if parts else ""
        message = ""

        if action == "shop_buy":
            if len(parts) < 2:
                return self.get_state("Invalid command.")
            item = parts[1]
            if item == "up":
                if self.upgrade_pack > 0 and self.money >= 3:
                    self.money -= 3
                    self.upgrade_pack -= 1
                    if self.inventory:
                        upgrade_pet = random.choice(self.inventory)
                        pet_levels[upgrade_pet] = pet_levels.get(upgrade_pet, 1) + 1
                        all_pet_stats[upgrade_pet]["attack"] += all_pet_stats[upgrade_pet]["rarity"]
                        all_pet_stats[upgrade_pet]["hp"] += all_pet_stats[upgrade_pet]["rarity"]
                        message = f"Upgraded {upgrade_pet} to Level {pet_levels[upgrade_pet]}"
                else: message = "Cannot buy Upgrade Pack."
            elif item == "cp":
                if self.charakter_pack > 0 and self.money >= 8:
                    self.money -= 8
                    self.charakter_pack -= 1
                    c_r_l = random.randint(0,100)
                    new_pet, pet_type = (None, None)
                    if c_r_l > 90 and rare_pets: new_pet, pet_type = random.choice(rare_pets), "rare"
                    elif c_r_l < 5 and legendary_pets: new_pet, pet_type = random.choice(legendary_pets), "legendary"
                    elif common_pets: new_pet, pet_type = random.choice(common_pets), "common"
                    
                    if new_pet:
                        self.inventory.append(new_pet)
                        if pet_type == "rare": rare_pets.remove(new_pet)
                        elif pet_type == "legendary": legendary_pets.remove(new_pet)
                        elif pet_type == "common": common_pets.remove(new_pet)
                        message = f"You got a {pet_type} {new_pet}."
                    else: message = "No new pets available."
                else: message = "Cannot buy Character Pack."
            elif item == "lup":
                if self.legendary_upgrade_pack > 0 and self.money >= 10:
                    self.money -= 10
                    self.legendary_upgrade_pack -= 1
                    if self.inventory:
                        upgrade_pet = random.choice(self.inventory)
                        pet_levels[upgrade_pet] = pet_levels.get(upgrade_pet, 1) + 5
                        all_pet_stats[upgrade_pet]["attack"] += all_pet_stats[upgrade_pet]["rarity"] * 5
                        all_pet_stats[upgrade_pet]["hp"] += all_pet_stats[upgrade_pet]["rarity"] * 5
                        message = f"Mega Upgraded {upgrade_pet} to Level {pet_levels[upgrade_pet]}"
                else: message = "Cannot buy Legendary Upgrade Pack."
            elif item == "bp":
                if self.buff_pack > 0 and self.money >= 4:
                    self.money -= 4
                    self.buff_pack -= 1
                    available_buffs = [1, 2, 3, 13]
                    self.pending_buff_choices = random.sample(available_buffs, 3)
                    buff_descriptions = {
                        1: "+1 Attack for all Pets", 2: "+1 HP for all Pets",
                        3: "+2% Dodge Chance for all Pets", 13: "+1 Level for all Pets"
                    }
                    message = "Choose a buff."
                    # The state returned will contain the choices for the frontend
                else: message = "Cannot buy Buff Pack."

        elif action == "select_buff":
            if len(parts) < 2 or not self.pending_buff_choices:
                return self.get_state("Invalid buff selection.")
            try:
                choice_index = int(parts[1])
                if 0 <= choice_index < len(self.pending_buff_choices):
                    buff_id = self.pending_buff_choices[choice_index]
                    message = self.apply_buff(buff_id)
                else: message = "Invalid buff choice."
            except ValueError: message = "Invalid buff index."

        elif action == "shop_reroll":
            if self.money >= self.shop_refresh_price:
                self.money -= self.shop_refresh_price
                self.shop_refresh_price += 1
                self.reroll_shop()
                message = "Shop rerolled."
            else: message = "Not enough money to reroll."
        
        return self.get_state(message)

if __name__ == "__main__":
    game = Game()
    print(json.dumps(game.get_state("Welcome to Petro!")))
    sys.stdout.flush()

    for line in sys.stdin:
        command = line.strip()
        if command == "exit":
            break
        state = game.process_command(command)
        print(json.dumps(state))
        sys.stdout.flush()

