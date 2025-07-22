import time
import random 
import sys
import os
from Charaters_Card_Game import worm_stats,anaconda_stats,ant_stats,rat_stats,snail_stats,spider_stats,bee_stats, stag_beetle_stats, cat_stats




shop_refresh_price = 5
tss = 1.5                               # wartezeit zwischen nachricht und hauptmenu
money = 50000
stage = 1
Inventory = ["Worm"]
common_pets = ["Ant", "Rat", "Snail", "Spider", "Bee", "Stag Beetle"]
rare_pets = ["Cat"]
legendary_pets = ["Anaconda"]
pet_levels = {
    "Worm": 1,
    "Ant": 1,
    "Rat": 1,
    "Snail": 1,
    "Spider": 1,
    "Bee": 1,
    "Stag Beetle": 1,
    "Cat": 1,
    "Anaconda": 1,












}

def roll_packs(anzahl, chance):
    return sum(1 for _ in range(anzahl) if random.randint(0, chance) == 1)

upgrade_pack = roll_packs(10, 2)                 # durschnittlich 2.5 packs pro shop
legendary_upgrade_pack = roll_packs(5, 20)       # 0.25 also alle 4 shops
charakter_pack = roll_packs(3, 9)               # 0.3 alle 3 shops
buff_pack = roll_packs(10, 2)                      # 2.5 packs pro shop
    
def Fight():
    dubble_check = input("You are fighting on stage "+ str(stage)+". Are you sure you want to fight? N/Y")
    if dubble_check == "Y":
        print("yea")
    else:
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
    shop_packs = input("UP, BP,CP, LUP, RS or Main Menu?: ").lower()
    if shop_packs == "m":
        main_menu()
    elif shop_packs == "up":
        if upgrade_pack > 0:
            if money > 2:
                money -= 3
                upgrade_pack -= 1
                upgrade = random.choice(Inventory)
                if upgrade in pet_levels:
                    pet_levels[upgrade] += 1
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

    elif shop_packs == "bp":
        if buff_pack > 0:
            if money > 3:
                money -= 4
                buff_pack -= 1
                shop()
            else:
                print("not enough Money")
                time.sleep(2)
                shop()
        else:
            print("not on Stock")
            time.sleep(tss)
            
        shop()
    elif shop_packs == "cp":  
        if charakter_pack > 0:
            if money > 7:
                money -= 8
                charakter_pack -= 1
                c_r_l = random.randint(0,100)
                if c_r_l > 89:
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
                    r_p = random.choice(common_pets)
                    Inventory.append(r_p)
                    common_pets.remove(r_p)
                    print(f"You have got a common {r_p}.")
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
        
    elif shop_packs == "lup":
        if legendary_upgrade_pack > 0:
            if money > 9:
                money -= 10
                legendary_upgrade_pack -= 1
                upgrade = random.choice(Inventory)
                if upgrade in pet_levels:
                    pet_levels[upgrade] += 5
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
    elif shop_packs == "rs":
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
    elif shop_packs == "e":
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
        print("Your Inventory:")
        print(",".join([f"{pet} (Lv.{pet_levels.get(pet, 1)})" for pet in Inventory]))
        wait = input()  
        main_menu()
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

main_menu()






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
#dodge chance hinzufügen: z.b biene hat sehr hohe dodje wahrscheinlichkeit. und hat so 20% wahrscheinlichkeit das die gegbnerische attacke nicht hittet
#
#
#





















