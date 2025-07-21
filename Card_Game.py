import time
import random 
import sys
import os

def roll_packs(anzahl, chance):
    return sum(1 for _ in range(anzahl) if random.randint(0, chance) == 1)

upgrade_pack = roll_packs(5, 2)                 # durschnittlich 2.5 packs pro shop
legendary_upgrade_pack = roll_packs(5, 20)       # 0.25 also alle 4 shops
charakter_pack = roll_packs(1, 3)               # 0.3 alle 3 shops
buff_pack = roll_packs(5, 2)                      # 2.5 packs pro shop
tss = 1.5                               # wartezeit zwischen nachricht und hauptmenu
money = 10
stage = 1
Inventar = ["Wurm"]

wurm_stats = {"level": 1, "attack": 1, "hp": 10}

def Wurm():
    attack = wurm_stats["attack"]
    hp = wurm_stats["hp"] 
    level = wurm_stats["level"]

ant_stats = {"level": 1, "attack": 2, "hp": 15}

def Ant():
    attack = ant_stats["attack"]
    hp = ant_stats["hp"] 
    level = ant_stats["level"]
    
def Fight():
    dubble_check = input("You are fighting on stage "+ str(stage)+". Are you sure you want to fight? N/Y")
    if dubble_check == "Y":
        print("yea")
    else:
        main_menu()

    
def shop():
    global money, upgrade_pack, buff_pack, charakter_pack, legendary_upgrade_pack
    liness = [
    "------------------------------",
    "Money:"+str(money)+"$",
    "",
    "1.)  "+str(upgrade_pack)+" Upgrade Pack available                   3$",
    "2.)  "+str(buff_pack)+" Buff Pack available                      4$",
    "3.)  "+str(charakter_pack)+" Charakter Pack available                 8$",
    "4.)  "+str(legendary_upgrade_pack)+" Legendary Upgrade Pack available         10$",
    ]
    for line in liness:
        print(line)
        time.sleep(0.03)
    shop_packs = input("1, 2, 3, 4 or No?: ")
    if shop_packs == "No":
        main_menu()
    elif shop_packs == "1":
        if upgrade_pack > 0:
            if money > 2:
                money -= 3
                upgrade_pack -= 1
                main_menu()
            else:
                print("not enogh Money")
                time.sleep(tss)
                main_menu()
        else:
            print("not on Stock")
            time.sleep(tss)
            
        main_menu()

    elif shop_packs == "2":
        if buff_pack > 0:
            if money > 3:
                money -= 4
                buff_pack -= 1
                main_menu()
            else:
                print("not enogh Money")
                time.sleep(2)
                main_menu()
        else:
            print("not on Stock")
            time.sleep(tss)
            
        main_menu()
    elif shop_packs == "3":  
        if charakter_pack > 0:
            if money > 7:
                money -= 8
                charakter_pack -= 1
                main_menu()
            else:
                print("not enogh Money")
                time.sleep(tss)
                main_menu()
        else:
            print("not on Stock")
            time.sleep(tss)
        main_menu()
        
    elif shop_packs == "4":
        if legendary_upgrade_pack > 0:
            if money > 9:
                money -= 10
                legendary_upgrade_pack - 1
                main_menu()
            else:
                print("not enogh Money")
                time.sleep(tss)
                main_menu()
        else:
            print("not on Stock")
            time.sleep(tss)
            
        main_menu()
        
    else:
        main_menu()


def main_menu():
    global money
    
   
    lines = [
        "------------------------------",
        "Your Inventory:",
        ",".join(Inventar),
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
    
    user_Request = input("")
    print("------------------------------")
    
    if user_Request == "I":
        print("Your Inventory:")
        print(",".join(Inventar))
        time.sleep(2)
        money += 100  
        main_menu()
    if user_Request == "F":
        Fight()
    if user_Request == "S":
        shop()

main_menu()