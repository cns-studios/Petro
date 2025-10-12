import sys
import json
import random
import sqlite3
import os
import copy
from assets.pets import all_pet_stats as global_pet_stats, common_pets as global_common_pets, rare_pets as global_rare_pets, legendary_pets as global_legendary_pets, pet_levels as global_pet_levels, all_pets
from logic import push_state

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