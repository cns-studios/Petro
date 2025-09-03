import time
import random 
import sys
import os
import math
from Charaters_Card_Game import *


shop_refresh_price = 5
tss = 1.5                               # wartezeit zwischen nachricht und hauptmenu
money = 50000
stage = 1
Inventory = ["Worm"]

def roll_packs(anzahl, chance):
    return sum(1 for _ in range(anzahl) if random.randint(0, chance) == 1)

upgrade_pack = roll_packs(10, 2)                 # durschnittlich 2.5 packs pro shop
legendary_upgrade_pack = roll_packs(5, 20)       # 0.25 also alle 4 shops
charakter_pack = roll_packs(3, 9)               # 0.3 alle 3 shops
buff_pack = roll_packs(10, 2)                      # 2.5 packs pro shop
    

def Fight():
    dubble_check = input("You are fighting on stage "+ str(stage)+". Are you sure you want to fight? N/Y")
    if dubble_check == "wo bist du":
        print("yea")
    else:
        main_menu()

def Inventory_function():
    print("Your Inventory:")
    print(", ".join([f"{pet} (Lv.{pet_levels.get(pet, 1)})" for pet in Inventory]))
    print("do You want to sell any Pet? Type: Sell Petname ")
    user_Request = input()
    if user_Request in Inventory:
        print(all_pet_stats[user_Request])
        Inventory_function()
    elif user_Request.startswith("sell "):
        pet_to_sell = user_Request[5:].strip()
        if pet_to_sell in Inventory:
            sell_price = all_pet_stats[pet_to_sell]["rarity"] * 2
            confirm = input(f"Are you sure you want to sell {pet_to_sell} for {sell_price}$? (Y/N): ").lower()
            if confirm == 'y':
                Inventory.remove(pet_to_sell)
                all_pet_stats[pet_to_sell][rarity]
                money += sell_price
                if pet_to_sell in pet_levels:
                    pet_levels[pet_to_sell] = 1
                print(f"You have sold {pet_to_sell} for {sell_price}$.")
        main_menu()
    
def shop():
    global money, upgrade_pack, buff_pack, charakter_pack, legendary_upgrade_pack, shop_refresh_price, r_p
    liness = [
    "-------------Shop-------------",
    "Money:"+str(money)+"$",
    "",
    "  "+str(upgrade_pack)+" Upgrade Pack (UP) available                   3$",
    "  "+str(buff_pack)+" Buff Pack (BP) available                      4$",
    "  "+str(charakter_pack)+" Charakter Pack (CP) available                 8$",
    "  "+str(legendary_upgrade_pack)+" Legendary Upgrade Pack (LUP) available        10$",
    " ♾️  Reroll Shop(RS)                               "+str(shop_refresh_price)+"$                         ",
    ]
    for line in liness:
        print(line)
        time.sleep(0.03)
    user_request = input("1, 2,3, 4, r or Main Menu?: ").lower()
    if user_request == "m":
        main_menu()
    elif user_request == "up":
        if upgrade_pack > 0:
            if money > 2:
                money -= 3
                upgrade_pack -= 1
                upgrade = random.choice(Inventory)
                if upgrade in pet_levels:
                    pet_levels[upgrade] += 1
                    if upgrade in all_pet_stats:
                        all_pet_stats[upgrade]["attack"] += all_pet_stats[upgrade]["rarity"] 
                        all_pet_stats[upgrade]["hp"] += all_pet_stats[upgrade]["rarity"] 
                    print(f"you have upgraded {upgrade} to Level {pet_levels[upgrade]}")
                wait = input()
                shop()
            else:
                print("not enough Money")
                time.sleep(tss)
                shop()
        else:
            print("not on Stock")
            time.sleep(tss)
            
        shop()

    
    elif user_request == "cp":  
        if charakter_pack > 0:
            if money > 7:
                money -= 8
                charakter_pack -= 1
                c_r_l = random.randint(0,100)
                if c_r_l > 90:
                    r_p = random.choice(rare_pets)
                    Inventory.append(r_p)
                    rare_pets.remove(r_p)
                    print(f"You have got a rare {r_p}.")
                    wait = input("")
                elif c_r_l < 5:
                    r_p = random.choice(legendary_pets)
                    Inventory.append(r_p)
                    legendary_pets.remove(r_p)
                    print(f"You have got a legendary {r_p}.")
                    wait = input("")
                else:
                    if len(common_pets) > 0:
                        r_p = random.choice(common_pets)
                        Inventory.append(r_p)
                        common_pets.remove(r_p)
                        print(f"You have got a common {r_p}.")
                    else:
                        print(f"You already own all 20 common Pets")
                    wait = input("")
                shop()
            else:
                print("not enough Money")
                time.sleep(tss)
                shop()
        else:
            print("not on Stock")
            time.sleep(tss)
        shop()
        
    elif user_request == "lup":
        if legendary_upgrade_pack > 0:
            if money > 9:
                money -= 10
                legendary_upgrade_pack -= 1
                upgrade = random.choice(Inventory)
                if upgrade in pet_levels:
                    pet_levels[upgrade] += 5
                    if upgrade in all_pet_stats:
                        all_pet_stats[upgrade]["attack"] += all_pet_stats[upgrade]["rarity"] * 5 
                        all_pet_stats[upgrade]["hp"] += all_pet_stats[upgrade]["rarity"] * 5

                    
                    print(f"you have upgraded {upgrade} to Level {pet_levels[upgrade]}")
                wait = input()
                shop()
            else:
                print("not enough Money")
                time.sleep(tss)
                shop()
        else:
            print("not on Stock")
            time.sleep(tss)

    elif user_request == "bp":
        if buff_pack > 0:
            if money > 3:
                money -= 4
                buff_pack -= 1
                available_buffs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                selected_buffs = random.sample(available_buffs, 3)
                buff_descriptions = {
                1: "+1 Attack for all Pets in Inventory",
                2: "+1 HP for all Pets in Inventory", 
                3: "+2% Dodge Chance for all Pets in Inventory",
                4: "+2 Attack for all Common Pets in Inventory",
                5: "+2 HP for all Common Pets in Inventory",
                6: "+3 Attack for all rare Pets in Inventory",
                7: "+3 hp for all rare Pets in Inventory",
                8: "+5 Attack for all Legandary Pets in Inventory",
                9: "+5 hp for all Legandary Pets in Inventory",
                10: "1 money for every Pet in Inventory",
                11: "+2 Money for every common and -1 for each rare in Inventory",
                12: "dubble the money you have",
                13: "+1 Level for all Pets in Inventory",


            }
            
            print("-------------------------------")
            print("Choose one of these buffs:")
            print(f"1) {buff_descriptions[selected_buffs[0]]}")
            print(f"2) {buff_descriptions[selected_buffs[1]]}")
            print(f"3) {buff_descriptions[selected_buffs[2]]}")
            
            
            while True:
                choice = input("Enter 1, 2, or 3: ")
                if choice in ["1", "2", "3"]:
                    chosen_buff = selected_buffs[int(choice) - 1]
                    break
                else:
                    print("Invalid choice! Enter 1, 2, or 3.")
            money_1 = 0
            money_2 = 0 
            if chosen_buff == 1:
                print("You have chosen: +1 Attack for all Pets")
                for pet in Inventory:
                    all_pet_stats[pet]["attack"] += 1
            elif chosen_buff == 2:
                print("You have chosen: +1 HP for all Pets")
                for pet in Inventory:
                    all_pet_stats[pet]["hp"] += 1
            elif chosen_buff == 3:
                print("You have chosen: +2% Dodge Chance for all Pets")
                for pet in Inventory:
                    all_pet_stats[pet]["dodge_chance"] += 2
            elif chosen_buff == 4:
                print("You have chosen: +2 Attack for all Common Pets")
                for pet in Inventory:
                    if pet in common_pets:
                        all_pet_stats[pet]["attack"] += 2
            elif chosen_buff == 5:
                print("You have chosen: +2 HP for all Common Pets")
                for pet in Inventory:
                    if pet in common_pets:
                        all_pet_stats[pet]["hp"] += 2
            elif chosen_buff == 6:
                print("You have chosen: +3 Attack for all Rare Pets")
                for pet in Inventory:
                    if pet in rare_pets:
                        all_pet_stats[pet]["attack"] += 3
            elif chosen_buff == 7:
                print("You have chosen: +3 HP for all Rare Pets")
                for pet in Inventory:
                    if pet in rare_pets:
                        all_pet_stats[pet]["hp"] += 3
            elif chosen_buff == 8:
                print("You have chosen: +5 Attack for all Legendary Pets")
                for pet in Inventory:
                    if pet in legendary_pets:
                        all_pet_stats[pet]["attack"] += 5
            elif chosen_buff == 9:
                print("You have chosen: +5 HP for all Legendary Pets")
                for pet in Inventory:
                    if pet in legendary_pets:
                        all_pet_stats[pet]["hp"] += 5
            elif chosen_buff == 10:
                print("You have chosen: +1 Money for every Pet in Inventory")
                money_1 = len(Inventory)
                print(f"You have got {money_1} Money")
                money += money_1
            elif chosen_buff == 11:
                print("You have chosen: +2 Money for every Common Pet and -1 for each Rare Pet in Inventory")
                for pet in Inventory:
                    if all_pet_stats[pet]["rarity"] ==  1:  
                        money_2 += 2    
                    elif all_pet_stats[pet]["rarity"] == 2:  
                        money_2 -= 1 
                    else:
                        money_2 += 0
                print(f"You have got {money_2} Money")  
                money += money_2
            elif chosen_buff == 12:
                print("You have chosen: Dubble the Money you have (Max. 25)")
                if money * 2 <= 25:
                    money *= 2
                    print(f"You have got {money/2} Money")
                else:
                    print("You have got 25 Money")
                    money += 25
            elif chosen_buff == 13:
                print("You have chosen: +1 Level for all Pets in Inventory")
                for pet in Inventory:
                    if pet in pet_levels:
                        pet_levels[pet] += 1
                        all_pet_stats[pet]["attack"] += all_pet_stats[pet]["rarity"]
                        all_pet_stats[pet]["hp"] += all_pet_stats[pet]["rarity"]
            

            
                
                time.sleep(1)
                shop()
      

            
            else:
                    print("not enough Money")
                    time.sleep(tss)
                    shop()
        else:
            print("not on Stock")
            time.sleep(tss)









            
        shop()
    elif user_request == "r":
        if money > shop_refresh_price - 1:
            money -= shop_refresh_price
            shop_refresh_price += 1
            

            upgrade_pack = roll_packs(5, 2)                 # durschnittlich 2.5 packs pro shop
            legendary_upgrade_pack = roll_packs(5, 20)       # 0.25 also alle 4 shops
            charakter_pack = roll_packs(1, 3)               # 0.3 alle 3 shops
            buff_pack = roll_packs(5, 2)                      # 2.5 packs pro shop
            
            shop()
    
        else:
            print("not enough money")
            time.sleep(tss)
            shop()
    elif user_request == "e":
        exit()
    else:
        shop()


def main_menu():
    
    global money

    
    

   
    lines = [
        "------------------------------",
        "Your Inventory:",
        ",".join(Inventory),
        "------------------------------",
        "Money:"+str(money)+"$",
        "------------------------------",
        "Main Menu:",
        "I Inventory",
        "F Fight",
        "S Shop"
    ]
    
    for line in lines:
        print(line)
        time.sleep(0.02)  
    
    user_Request = input("").lower()
    
    print("------------------------------")
    
    if user_Request == "i":
       Inventory_function()
    elif user_Request == "f":
        Fight()
    elif user_Request == "s":
        shop()
    elif user_Request == "esc" or "e":
        exit()
    else:
        print("")
        time.sleep(tss)
        main_menu()

#main_menu()






# Pläne:
# Viele Stufen, die immer schwerer werden
# 3 Leben: Wenn man eine Stufe nicht schafft, kriegt man trotzdem das Geld und -1 Herz
# Wenn alle 3 Leben weg sind, dann Reset. Es soll low key Balatro sein, dass du mit deinen Pets und den Upgradern 0 Pack haushalten sollst
# Re-Roll-Button für Shop
# Super selten: Neuer Charakter direkt im Shop
# GUI bzw. schöneres/übersichtlicheres Design
# Tutorial
# Pets mergen. Heißt: Mehrere Common-Pets mergen zu einem Rare-Pet. Bissl wie bei Roblox, dass die Wahrscheinlichkeit höher wird, wenn mehr Pets gemerged werden.
# Upgrade-System: Legendäres Upgrade-Pack soll 5 Mal ein Pet upgraden. Upgrade-Pack soll nur ein Level leveln. Buff-Pack soll Buffkarten geben. Charakter-Pack soll ein random Common-Pet geben und mit 1/10 Chance Rare und mit 1/100 Chance Legendary.
# Buff-Pack/Fighting-System: Soll ein bisschen wie bei Pokémon sein heißt: Du machst Attacke, KI macht Attacke (Random)
#     !--> Wenn der Player Attacke macht, kann er wählen, welches Pet er für diese Attacke nutzt. Dann kann er zwischen Attacken auswählen. Starter (Wurm) 1 Attacke, Uncommon (Ant) 2 Attacken, Rare (Cat) 3 Attacken, Legendary (Tiger) 4 Attacken,
#           !--> (Attacken können z. B. auch Block sein.) Dann KI greift an (Random). Ab dann: Spieler kann zuerst Buffkarte auswählen (wenn er möchte), dann ob er das Pet wechseln möchte (wenn ja: KI ist direkt dran mit Angreifen). Wenn nicht = Attacke auswählen. Repeat
# Wenn Pet tot, dann für 3 Runden tot. Ab dann wieder einsetzbar.
# Pets übers Inventar verkaufen können.
# Money-Pack: Möglichkeit, Geld zu machen: z. B.: Verdoppelt Geld, gibt doppeltes Geld wie Anzahl der Pets, 2 Dollar für jedes verkaufte Pet, etc.
# Animation für Packs
# Pets passive Fähigkeiten: Z. B. 1 Dollar für Beenden eines Levels, 5 % mehr Schaden für alle Common-Pets etc.
# 30 Pets (vorerst) adden
#shop reset price nach jesder runde wieder auf 5






pet_1, pet_2 = random.sample(all_pets, 2)

print(pet_1, ": Attack:", all_pet_stats[pet_1]["attack"], "HP:", all_pet_stats[pet_1]["hp"], "Class:", all_pet_stats[pet_1]["class"], "Dodge Chance:", all_pet_stats[pet_1]["dodge_chance"], "%")
print(pet_2, ": Attack:", all_pet_stats[pet_2]["attack"], "HP:", all_pet_stats[pet_2]["hp"], "Class:", all_pet_stats[pet_2]["class"], "Dodge Chance:", all_pet_stats[pet_2]["dodge_chance"], "%")
CLASSES = {
    1: "Tank",
    2: "Poisoner",
    3: "Assassin",
    4: "Berserker",
    5: "Aerial",
    6: "Dodger",
    7: "Digger",
}



def modify_two_pets(pets: dict, pet_1, pet_2):
    """Wendet Klassenmodifikationen NUR zwischen pet_1 und pet_2 an."""
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

        # Poisoner vs Tank -> Poisoner -30% Attack
        if 2 in classes and 1 in other_classes:
            change_attack(attacker, -30)

        # Berserker vs Tank -> +20% Attack
        if 4 in classes and 1 in other_classes:
            change_attack(attacker, 20)

        # Dodger vs Assassin -> -10% Dodge
        if 6 in classes and 3 in other_classes:
            change_dodge(attacker, -10)

        # Aerial vs Digger -> Aerial +15% Attack
        if 5 in classes and 7 in other_classes:
            change_attack(attacker, 15)

        # Digger vs Tank -> Digger +10% Attack
        if 7 in classes and 1 in other_classes:
            change_attack(attacker, 10)

        # Assassin vs Tank -> -10% Attack
        if 3 in classes and 1 in other_classes:
            change_attack(attacker, -10)

        # dodjer or aerials vs poisner -> -20% Dodje
        if (5 in classes or 6 in classes) and 2 in other_classes:
            change_dodge(attacker, -20)

    # Regeln für beide Richtungen anwenden
    apply_rules(pet_1, pet_2)
    apply_rules(pet_2, pet_1)

    return mod_pets

mod_pets = modify_two_pets(all_pet_stats, pet_1, pet_2)

print(pet_1, ": Attack:", mod_pets[pet_1]["attack"], "HP:", mod_pets[pet_1]["hp"], "Class:", mod_pets[pet_1]["class"], "Dodge Chance:", mod_pets[pet_1]["dodge_chance"], "%")
print(pet_2, ": Attack:", mod_pets[pet_2]["attack"], "HP:", mod_pets[pet_2]["hp"], "Class:", mod_pets[pet_2]["class"], "Dodge Chance:", mod_pets[pet_2]["dodge_chance"], "%")





#class Pet:
#1 = Tank
#2 = Poisoner
#3 = Assassin
#4 = Berserker
#5 = Aerial
#6 = Dodger
#7 = Digger


