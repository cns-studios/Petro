import sys
import json
import random
import sqlite3
import os
import copy
from assets.pets import all_pet_stats as global_pet_stats, common_pets as global_common_pets, rare_pets as global_rare_pets, legendary_pets as global_legendary_pets, pet_levels as global_pet_levels, all_pets

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'users.db') if os.path.dirname(__file__) else os.path.join('db', 'users.db')

def push_state(username, game):
    if not username:
        return False
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        game_state = {
            'money': game.money,
            'stage': game.stage,
            'inventory': [],
            'shop': {
                'upgrade_pack': game.upgrade_pack,
                'buff_pack': game.buff_pack,
                'charakter_pack': game.charakter_pack,
                'legendary_upgrade_pack': game.legendary_upgrade_pack,
                'shop_refresh_price': game.shop_refresh_price,
            },
            'pending_buff_choices': game.pending_buff_choices,
            'available_pets': {
                'common': game.available_common_pets,
                'rare': game.available_rare_pets,
                'legendary': game.available_legendary_pets
            }
        }
        
        for pet_name in game.inventory:
            if pet_name in game.all_pet_stats:
                pet_data = {
                    'name': pet_name,
                    'level': game.pet_levels.get(pet_name, 1),
                    'attack': game.all_pet_stats[pet_name]['attack'],
                    'hp': game.all_pet_stats[pet_name]['hp'],
                    'dodge_chance': game.all_pet_stats[pet_name]['dodge_chance'],
                    'rarity': game.all_pet_stats[pet_name]['rarity']
                }
                game_state['inventory'].append(pet_data)
        
        modified_stats = {}
        for pet_name, stats in game.all_pet_stats.items():
            if pet_name in global_pet_stats:
                if (stats['attack'] != global_pet_stats[pet_name]['attack'] or
                    stats['hp'] != global_pet_stats[pet_name]['hp'] or
                    stats['dodge_chance'] != global_pet_stats[pet_name]['dodge_chance']):
                    modified_stats[pet_name] = {
                        'attack': stats['attack'],
                        'hp': stats['hp'],
                        'dodge_chance': stats['dodge_chance']
                    }
        game_state['modified_stats'] = modified_stats
        
        game_state['pet_levels'] = game.pet_levels
        
        game_state_json = json.dumps(game_state)
        cursor.execute("UPDATE users SET game_state = ? WHERE username = ?", (game_state_json, username))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving game state: {e}", file=sys.stderr)
        return False

def pull_state(username):
    if not username:
        return None
    if not os.path.exists(DB_PATH):
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT game_state FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return json.loads(row[0])
        return None
    except Exception as e:
        print(f"Error loading game state: {e}", file=sys.stderr)
        return None

class Game:
    def __init__(self, username):
        self.username = username
        
        self.all_pet_stats = copy.deepcopy(global_pet_stats)
        self.pet_levels = {}
        self.available_common_pets = global_common_pets.copy()
        self.available_rare_pets = global_rare_pets.copy()
        self.available_legendary_pets = global_legendary_pets.copy()
        
        state = pull_state(username)
        
        if state:
            self.money = state.get('money', 67676769696969)
            self.stage = state.get('stage', 1)
            self.inventory = []
            
            shop_state = state.get('shop', {})
            self.shop_refresh_price = shop_state.get('shop_refresh_price', 5)
            self.upgrade_pack = shop_state.get('upgrade_pack', 0)
            self.legendary_upgrade_pack = shop_state.get('legendary_upgrade_pack', 0)
            self.charakter_pack = shop_state.get('charakter_pack', 0)
            self.buff_pack = shop_state.get('buff_pack', 0)
            self.pending_buff_choices = state.get('pending_buff_choices', [])
            
            available_pets = state.get('available_pets', {})
            if available_pets:
                self.available_common_pets = available_pets.get('common', global_common_pets.copy())
                self.available_rare_pets = available_pets.get('rare', global_rare_pets.copy())
                self.available_legendary_pets = available_pets.get('legendary', global_legendary_pets.copy())
            
            self.pet_levels = state.get('pet_levels', {})
            
            modified_stats = state.get('modified_stats', {})
            for pet_name, stats in modified_stats.items():
                if pet_name in self.all_pet_stats:
                    self.all_pet_stats[pet_name]['attack'] = stats['attack']
                    self.all_pet_stats[pet_name]['hp'] = stats['hp']
                    self.all_pet_stats[pet_name]['dodge_chance'] = stats['dodge_chance']
            
            for pet_details in state.get('inventory', []):
                pet_name = pet_details.get('name')
                if pet_name and pet_name in self.all_pet_stats:
                    self.inventory.append(pet_name)
                    self.all_pet_stats[pet_name]['attack'] = pet_details.get('attack', self.all_pet_stats[pet_name]['attack'])
                    self.all_pet_stats[pet_name]['hp'] = pet_details.get('hp', self.all_pet_stats[pet_name]['hp'])
                    self.all_pet_stats[pet_name]['dodge_chance'] = pet_details.get('dodge_chance', self.all_pet_stats[pet_name]['dodge_chance'])
                    
                    if pet_name not in self.pet_levels:
                        self.pet_levels[pet_name] = pet_details.get('level', 1)
            
            if not available_pets:
                for pet in self.inventory:
                    if pet in self.available_common_pets:
                        self.available_common_pets.remove(pet)
                    elif pet in self.available_rare_pets:
                        self.available_rare_pets.remove(pet)
                    elif pet in self.available_legendary_pets:
                        self.available_legendary_pets.remove(pet)
            
            if (self.upgrade_pack == 0 and self.legendary_upgrade_pack == 0 and 
                self.charakter_pack == 0 and self.buff_pack == 0):
                self.reroll_shop()
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
            
            self.pet_levels["Worm"] = 1
            if "Worm" in self.available_common_pets:
                self.available_common_pets.remove("Worm")
            
            self.reroll_shop()
            push_state(self.username, self)

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
            if pet_name in self.all_pet_stats:
                stats = self.all_pet_stats[pet_name]
                inventory_details.append({
                    "name": pet_name,
                    "level": self.pet_levels.get(pet_name, 1),
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
            for pet in self.inventory: 
                self.all_pet_stats[pet]["attack"] += 1
        elif buff_id == 2:
            message += "+1 HP for all Pets"
            for pet in self.inventory: 
                self.all_pet_stats[pet]["hp"] += 1
        elif buff_id == 3:
            message += "+2% Dodge Chance for all Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["dodge_chance"] < 98:
                    self.all_pet_stats[pet]["dodge_chance"] += 2
                else: 
                    self.all_pet_stats[pet]["dodge_chance"] = 99
        elif buff_id == 4:
            message += "+2 Attack for all Common Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 1:
                    self.all_pet_stats[pet]["attack"] += 2
        elif buff_id == 5:
            message += "+2 HP for all Common Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 1:
                    self.all_pet_stats[pet]["hp"] += 2
        elif buff_id == 6:
            message += "+3 Attack for all Rare Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 2:
                    self.all_pet_stats[pet]["attack"] += 3
        elif buff_id == 7:
            message += "+3 HP for all Rare Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 2:
                    self.all_pet_stats[pet]["hp"] += 3
        elif buff_id == 8:
            message += "+5 Attack for all Legendary Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 3:
                    self.all_pet_stats[pet]["attack"] += 5
        elif buff_id == 9:
            message += "+5 HP for all Legendary Pets"
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 3:
                    self.all_pet_stats[pet]["hp"] += 5
        elif buff_id == 10:
            message += "+1 Money for every Pet in Inventory"
            money_1 = len(self.inventory)
            message += f". You have got {money_1} Money"
            self.money += money_1
        elif buff_id == 11:
            message += "+2 Money for every Common Pet and -1 for each Rare Pet in Inventory"
            money_2 = 0
            for pet in self.inventory:
                if self.all_pet_stats[pet]["rarity"] == 1:  
                    money_2 += 2    
                elif self.all_pet_stats[pet]["rarity"] == 2:  
                    money_2 -= 1 
            message += f". You have got {money_2} Money"
            self.money = max(0, self.money + money_2)
        elif buff_id == 12:
            message += "Double the Money you have (Max. 25)"
            money_to_add = min(self.money, 25)
            self.money += money_to_add
            message += f". You have got {money_to_add} Money"
        elif buff_id == 13:
            message += "+1 Level for all Pets"
            for pet in self.inventory:
                self.pet_levels[pet] = self.pet_levels.get(pet, 1) + 1
                self.all_pet_stats[pet]["attack"] += self.all_pet_stats[pet]["rarity"]
                self.all_pet_stats[pet]["hp"] += self.all_pet_stats[pet]["rarity"]
        
        self.pending_buff_choices = []
        return message

    def process_command(self, command):
        parts = command.strip().lower().split()
        action = parts[0] if parts else ""
        message = ""

        if action == "get_state":
            return self.get_state("Welcome back!")
        elif action == "save":
            if push_state(self.username, self):
                message = "Game saved successfully."
            else:
                message = "Failed to save game."
        elif action == "sell_all_pets":
            if self.inventory:
                total_sell_value = 0
                num_sold_pets = len(self.inventory)
                
                for pet in self.inventory:
                    # Verkaufswert für jedes Pet berechnen und zur Gesamtsumme addieren
                    sell_value = self.all_pet_stats[pet]["rarity"] * 2 + (self.pet_levels.get(pet, 1) - 1)
                    total_sell_value += sell_value
                    
                    # Pet-Level zurücksetzen (falls pet ein String ist)
                    if pet in self.pet_levels:
                        self.pet_levels[pet] = 1

                    rarity = self.all_pet_stats[pet]["rarity"]
                    if rarity == 1 and pet not in self.available_common_pets:
                        self.available_common_pets.append(pet)
                    elif rarity == 2 and pet not in self.available_rare_pets:
                        self.available_rare_pets.append(pet)
                    elif rarity == 3 and pet not in self.available_legendary_pets:
                        self.available_legendary_pets.append(pet)
                self.money += total_sell_value
                self.inventory.remove(pet)  # Entferne das Pet aus dem Inventar
                message = f"Sold {num_sold_pets} pets for {total_sell_value} money."
            else:
                message = "No pets to sell."

        elif action == "spezific_pet_sell":
            if len(parts) < 2:
                return self.get_state("Invalid command.")
            
            pet_name = " ".join(parts[1:])
            print(f"spezifisches pet: '{pet_name}'")
            
            print(f"DEBUG inventory (strings): {self.inventory}")
            
            # Suche in String-Liste (case-insensitive)
            matching_pet_name = None
            for pet_string in self.inventory:
                if pet_string.lower() == pet_name.lower():
                    matching_pet_name = pet_string
                    break
            
            if matching_pet_name:
                # Berechne Verkaufswert
                total_sell_value = 0
                sell_value = self.all_pet_stats[matching_pet_name]["rarity"] * 2 + (self.pet_levels.get(matching_pet_name, 1) - 1)
                total_sell_value += sell_value
                
                # Pet-Level zurücksetzen
                if matching_pet_name in self.pet_levels:
                    self.pet_levels[matching_pet_name] = 1
                
                # Geld hinzufügen und Pet entfernen
                self.money += total_sell_value


                self.inventory.remove(matching_pet_name)
                rarity = self.all_pet_stats[pet_name]["rarity"]
                if rarity == 1 and pet_name not in self.available_common_pets:
                    self.available_common_pets.append(pet_name)
                elif rarity == 2 and pet_name not in self.available_rare_pets:
                    self.available_rare_pets.append(pet_name)
                elif rarity == 3 and pet_name not in self.available_legendary_pets:
                    self.available_legendary_pets.append(pet_name)  # Füge das Pet wieder hinzu, um den Index zu erhalten
                message = f"Sold {matching_pet_name} for {total_sell_value} money."
                print(f"SUCCESS: Sold {matching_pet_name} for {total_sell_value}")
            else:
                message = f"Pet {pet_name} not found in inventory."
                print(f"NOT FOUND: Available pets: {self.inventory}")
        elif action == "shop_buy":
            if len(parts) < 2:
                return self.get_state("Invalid command.")
            item = parts[1]
            if item == "up":
                if self.upgrade_pack > 0 and self.money >= 3:
                    self.money -= 3
                    self.upgrade_pack -= 1
                    if self.inventory:
                        upgrade_pet = random.choice(self.inventory)
                        self.pet_levels[upgrade_pet] = self.pet_levels.get(upgrade_pet, 1) + 1
                        self.all_pet_stats[upgrade_pet]["attack"] += self.all_pet_stats[upgrade_pet]["rarity"]
                        self.all_pet_stats[upgrade_pet]["hp"] += self.all_pet_stats[upgrade_pet]["rarity"]
                        message = f"Upgraded {upgrade_pet} to Level {self.pet_levels[upgrade_pet]}"
                else: 
                    message = "Cannot buy Upgrade Pack."
            elif item == "cp":
                if self.charakter_pack > 0 and self.money >= 8:
                    self.money -= 8
                    self.charakter_pack -= 1
                    c_r_l = random.randint(0, 100)
                    new_pet, pet_type = (None, None)
                    
                    if c_r_l > 90 and self.available_rare_pets: 
                        new_pet = random.choice(self.available_rare_pets)
                        pet_type = "rare"
                    elif c_r_l < 5 and self.available_legendary_pets: 
                        new_pet = random.choice(self.available_legendary_pets)
                        pet_type = "legendary"
                    elif self.available_common_pets: 
                        new_pet = random.choice(self.available_common_pets)
                        pet_type = "common"
                    
                    if new_pet:
                        self.inventory.append(new_pet)
                        self.pet_levels[new_pet] = 1
                        if pet_type == "rare": 
                            self.available_rare_pets.remove(new_pet)
                        elif pet_type == "legendary": 
                            self.available_legendary_pets.remove(new_pet)
                        elif pet_type == "common": 
                            self.available_common_pets.remove(new_pet)
                        message = f"You got a {pet_type} {new_pet}."
                    else: 
                        message = "No new pets available."
                else: 
                    message = "Cannot buy Character Pack."
            elif item == "lup":
                if self.legendary_upgrade_pack > 0 and self.money >= 10:
                    self.money -= 10
                    self.legendary_upgrade_pack -= 1
                    if self.inventory:
                        upgrade_pet = random.choice(self.inventory)
                        self.pet_levels[upgrade_pet] = self.pet_levels.get(upgrade_pet, 1) + 5
                        self.all_pet_stats[upgrade_pet]["attack"] += self.all_pet_stats[upgrade_pet]["rarity"] * 5
                        self.all_pet_stats[upgrade_pet]["hp"] += self.all_pet_stats[upgrade_pet]["rarity"] * 5
                        message = f"Mega Upgraded {upgrade_pet} to Level {self.pet_levels[upgrade_pet]}"
                else: 
                    message = "Cannot buy Legendary Upgrade Pack."
            elif item == "bp":
                if self.buff_pack > 0 and self.money >= 4:
                    self.money -= 4
                    self.buff_pack -= 1
                    available_buffs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                    self.pending_buff_choices = random.sample(available_buffs, 3)
                    message = "Choose a buff."
                else: 
                    message = "Cannot buy Buff Pack."

        elif action == "select_buff":
            if len(parts) < 2 or not self.pending_buff_choices:
                return self.get_state("Invalid buff selection.")
            try:
                choice_index = int(parts[1])
                if 0 <= choice_index < len(self.pending_buff_choices):
                    buff_id = self.pending_buff_choices[choice_index]
                    message = self.apply_buff(buff_id)
                else: 
                    message = "Invalid buff choice."
            except ValueError: 
                message = "Invalid buff index."

        elif action == "shop_reroll":
            if self.money >= self.shop_refresh_price:
                self.money -= self.shop_refresh_price
                self.shop_refresh_price += 1
                self.reroll_shop()
                message = "Shop rerolled."
            else: 
                message = "Not enough money to reroll."
        
        if action != "save":
            push_state(self.username, self)
        
        return self.get_state(message)


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else None
    if not username:
        print(json.dumps({"message": "Error: Username not provided."}))
        sys.exit(1)
    
    if not username.replace("_", "").replace("-", "").isalnum():
        print(json.dumps({"message": "Error: Invalid username format."}))
        sys.exit(1)

    try:
        game = Game(username)
        print(json.dumps(game.get_state("Welcome to Petro!")))
        sys.stdout.flush()

        for line in sys.stdin:
            command = line.strip()
            if command == "exit":
                push_state(username, game)
                break
            try:
                state = game.process_command(command)
                print(json.dumps(state))
                sys.stdout.flush()
            except Exception as e:
                import traceback
                print(f"EXCEPTION DEBUG: {str(e)}")
                print(f"TRACEBACK: {traceback.format_exc()}")
                error_state = game.get_state(f"Error processing command: {str(e)}")
                print(json.dumps(error_state))
                sys.stdout.flush()
    except Exception as e:
        print(json.dumps({"message": f"Fatal error: {str(e)}"}))
        sys.stdout.flush()