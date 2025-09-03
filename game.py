import sys
import json
import random
from assets.pets import all_pet_stats, common_pets, rare_pets, legendary_pets, pet_levels, all_pets

class Game:
    def __init__(self, state_json=None):
        if state_json:
            state = json.loads(state_json)
            self.money = state.get('money', 50000)
            self.stage = state.get('stage', 1)
            self.inventory = [pet['name'] for pet in state.get('inventory', [])]
            shop_state = state.get('shop', {})
            self.shop_refresh_price = shop_state.get('shop_refresh_price', 5)
            self.upgrade_pack = shop_state.get('upgrade_pack', 0)
            self.legendary_upgrade_pack = shop_state.get('legendary_upgrade_pack', 0)
            self.charakter_pack = shop_state.get('charakter_pack', 0)
            self.buff_pack = shop_state.get('buff_pack', 0)
            self.pending_buff_choices = state.get('pending_buff_choices', [])

            for pet_details in state.get('inventory', []):
                pet_name = pet_details.get('name')
                if pet_name:
                    pet_levels[pet_name] = pet_details.get('level', 1)
                    if pet_name in all_pet_stats:
                        all_pet_stats[pet_name]['attack'] = pet_details.get('attack', all_pet_stats[pet_name].get('attack'))
                        all_pet_stats[pet_name]['hp'] = pet_details.get('hp', all_pet_stats[pet_name].get('hp'))
                        all_pet_stats[pet_name]['dodge_chance'] = pet_details.get('dodge_chance', all_pet_stats[pet_name].get('dodge_chance'))
        else:
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

    # pull_state("all_pets_stats")
    def pull_state(self, things):
        if things == "all":
            return self.get_state()
        elif things == "all_pets_stats":
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
            return inventory_details
        elif things == "all_pets_level":
            return {p: pet_levels.get(p, 1) for p in self.inventory}
        elif things == "common_pets":
            return [p for p in self.inventory if p in all_pet_stats and all_pet_stats[p].get("rarity") == 1]
        elif things == "rare_pets":
            return [p for p in self.inventory if p in all_pet_stats and all_pet_stats[p].get("rarity") == 2]
        elif things == "legendary_pets":
            return [p for p in self.inventory if p in all_pet_stats and all_pet_stats[p].get("rarity") > 2]
        return None

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
            message = "+1 HP for all Pets"
            for pet in self.inventory: all_pet_stats[pet]["hp"] += 1
        elif buff_id == 3:
            message = "+2% Dodge Chance for all Pets"
            for pet in self.inventory:
                if all_pet_stats[pet]["dodge_chance"] < 98:
                    all_pet_stats[pet]["dodge_chance"] += 2
                else: all_pet_stats[pet]["dodge_chance"] = 99
        elif buff_id == 4:
            message = "+2 Attack for all Common Pets"
            for pet in self.inventory:
                if pet in common_pets:
                    all_pet_stats[pet]["attack"] += 2
        elif buff_id == 5:
            message = " +2 HP for all Common Pets"
            for pet in self.inventory:
                if pet in common_pets:
                    all_pet_stats[pet]["hp"] += 2
        elif buff_id == 6:
            message = " +3 Attack for all Rare Pets"
            for pet in self.inventory:
                if pet in rare_pets:
                    all_pet_stats[pet]["attack"] += 3
        elif buff_id == 7:
            message = " +3 HP for all Rare Pets"
            for pet in self.inventory:
                if pet in rare_pets:
                    all_pet_stats[pet]["hp"] += 3
        elif buff_id == 8:
            message = " +5 Attack for all Legendary Pets"
            for pet in self.inventory:
                if pet in legendary_pets:
                    all_pet_stats[pet]["attack"] += 5
        elif buff_id == 9:
            message = " +5 HP for all Legendary Pets"
            for pet in self.inventory:
                if pet in legendary_pets:
                    all_pet_stats[pet]["hp"] += 5
        elif buff_id == 10:
            message = " +1 Money for every Pet in Inventory"
            money_1 = len(self.inventory)
            message = f"You have got {money_1} Money"
            money += money_1
        elif buff_id == 11:
            message = " +2 Money for every Common Pet and -1 for each Rare Pet in Inventory"
            for pet in self.inventory:
                if all_pet_stats[pet]["rarity"] ==  1:  
                    money_2 += 2    
                elif all_pet_stats[pet]["rarity"] == 2:  
                    money_2 -= 1 
                else:
                    money_2 += 0
            message = f"You have got {money_2} Money"
            money += money_2
        elif buff_id == 12:
            message = " Dubble the Money you have (Max. 25)"
            if money * 2 <= 25:
                money *= 2
                money += f"You have got {money/2} Money"
            else:
                money += "You have got 25 Money"
                money += 25
        elif buff_id == 13:
            message = "+1 Level for all Pets"
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
                    available_buffs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                    self.pending_buff_choices = random.sample(available_buffs, 3)
                    buff_descriptions = {
                        1: "+1 Attack for all Pets", 2: "+1 HP for all Pets",
                        3: "+2% Dodge Chance for all Pets",4: "+2 Attack for all Common Pets", 
                        5: "+2 HP for all Common Pets", 6: "+3 Attack for all Rare Pets",
                        7: "+3 HP for all Rare Pets", 8: "+5 Attack for all Legendary Pets",
                        9: "+5 HP for all Legendary Pets", 10: "+1 Money for every Pet in Inventory",
                        11: "+2 Money for every Common Pet and -1 for each Rare Pet in Inventory", 12: "Dubble the Money you have (Max. 25)",
                        13: "+1 Level for all Pets"
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
    
def modify_two_pets_clean(pets: dict):
    # Zwei zufällige Pets auswählen
    pet_1, pet_2 = random.sample(list(pets.keys()), 2)
    
    # Kopien der Pets erstellen
    mod_pets = {
        pet_1: pets[pet_1].copy(),
        pet_2: pets[pet_2].copy()
    }

    def apply_rules(attacker, defender):
        classes = mod_pets[attacker]["class"]
        other_classes = mod_pets[defender]["class"]

        def change_attack(pet, percent):
            mod_pets[pet]["attack"] = round(mod_pets[pet]["attack"] * (1 + percent / 100))

        def change_dodge(pet, percent):
            mod_pets[pet]["dodge_chance"] = max(0, min(100, round(mod_pets[pet].get("dodge_chance", 0) * (1 + percent / 100))))

        # Alle Regeln hier...
        if 2 in classes and 1 in other_classes:
            change_attack(attacker, -30)
        if 4 in classes and 1 in other_classes:
            change_attack(attacker, 20)
        if 6 in classes and 3 in other_classes:
            change_dodge(attacker, -10)
        if 5 in classes and 7 in other_classes:
            change_attack(attacker, 15)
        if 7 in classes and 1 in other_classes:
            change_attack(attacker, 10)
        if 3 in classes and 1 in other_classes:
            change_attack(attacker, -10)
        if (5 in classes or 6 in classes) and 2 in other_classes:
            change_dodge(attacker, -20)

    # Regeln für beide Richtungen anwenden
    apply_rules(pet_1, pet_2)
    apply_rules(pet_2, pet_1)
    pet_1_original = pets[pet_1].copy()
    pet_2_original = pets[pet_2].copy()
    pet_1_modified = mod_pets[pet_1].copy()
    pet_2_modified = mod_pets[pet_2].copy()

    return pet_1_original, pet_1_modified, pet_2_original, pet_2_modified, mod_pets, pet_1, pet_2
    


if __name__ == "__main__":
    line = sys.stdin.readline().strip()
    game = None
    cmd = None
    try:
        json.loads(line)
        game = Game(state_json=line)
        print(json.dumps(game.get_state("Game loaded.")))
        sys.stdout.flush()
    except (json.JSONDecodeError, TypeError):
        game = Game()
        print(json.dumps(game.get_state("Welcome to Petro!")))
        sys.stdout.flush()
        if line:
            cmd = line
    if cmd:
        state = game.process_command(cmd)
        print(json.dumps(state))
        sys.stdout.flush()
    for line in sys.stdin:
        command = line.strip()
        if command == "exit":
            break
        state = game.process_command(command)
        print(json.dumps(state))
        sys.stdout.flush()