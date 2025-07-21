import time
import random 
money = 1000
def roll_packs(anzahl, chance):
    return sum(1 for _ in range(anzahl) if random.randint(0, chance) == 1)

upgrade_pack = roll_packs(5, 2)                 # durschnittlich 2.5 packs pro shop
legendary_upgrade_pack = roll_packs(5, 20)       # 0.25 also alle 4 shops
charakter_pack = roll_packs(1, 3)               # 0.3 alle 3 shops
buff_pack = roll_packs(5, 2)                      # 2.5 packs pro shop


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
    print("------------------------------")
    print("Money:"+str(money)+"$")
    print()
    print("1.)  "+str(upgrade_pack)+" Upgrade Pack available                  3$")
    print("2.)  "+str(buff_pack)+" Buff Pack available                     4$")
    print("3.)  "+str(charakter_pack)+" Charakter Pack available                8$")
    print("4.)  "+str(legendary_upgrade_pack)+" Legendary Upgrade Pack available        10$")
    shop_packs = input("1, 2, 3, 4 or No?: ")
    if shop_packs == "No":
        main_menu()  # Zurück zum Hauptmenü
    elif shop_packs == "1":
        if upgrade_pack > 0:  # Geändert von >= 0 zu > 0
            if money >= 3:  # Geändert von >= 2 zu >= 3 (Preis ist 3$)
                money -= 3
                upgrade_pack -= 1
                print("Upgrade Pack purchased!")
                time.sleep(1)
            else:
                print("not enough Money")
                time.sleep(1)
        else:
            print("not on Stock")
            time.sleep(1)
        shop()  # Zurück zum Shop

    elif shop_packs == "2":
        if buff_pack > 0:  # Geändert von >= 0 zu > 0
            if money >= 4:  # Geändert von >= 3 zu >= 4 (Preis ist 4$)
                money -= 4
                buff_pack -= 1
                print("Buff Pack purchased!")
                time.sleep(1)
            else:
                print("not enough Money")
                time.sleep(1)
        else:
            print("not on Stock")
            time.sleep(1)
        shop()  # Zurück zum Shop
        
    elif shop_packs == "3": 
        if charakter_pack > 0:  # Geändert von >= 0 zu > 0
            if money >= 8:  # Geändert von >= 7 zu >= 8 (Preis ist 8$)
                money -= 8
                charakter_pack -= 1
                print("Character Pack purchased!")
                time.sleep(1)
            else:
                print("not enough Money")
                time.sleep(1)
        else:
            print("not on Stock")
            time.sleep(1)
        shop()  # Zurück zum Shop
        
    elif shop_packs == "4":
        if legendary_upgrade_pack > 0:  # Geändert von >= 0 zu > 0
            if money >= 10:  # Geändert von >= 9 zu >= 10 (Preis ist 10$)
                money -= 10
                legendary_upgrade_pack -= 1
                print("Legendary Upgrade Pack purchased!")
                time.sleep(1)
            else:
                print("not enough Money")
                time.sleep(1)
        else:
            print("not on Stock")
            time.sleep(1)
        shop()  # Zurück zum Shop
    else:
        print("Invalid option!")
        time.sleep(1)
        shop()  # Zurück zum Shop für ungültige Eingaben


def main_menu():
    print("------------------------------")
    
    print("Your Inventory:")
    print(",".join(Inventar))
    print("------------------------------")
    print("Money:"+str(money)+"$")
    print("------------------------------")
    print("Main Menu:")
    print("I Inventory")
    print("F Fight")
    print("S Shop")
    user_Request = input("")
    print("------------------------------")

    if user_Request == "I":
        print("Your Inventory:")
        print(",".join(Inventar))
        time.sleep(2)
        main_menu()
    if user_Request == "F":
        Fight()
    if user_Request == "S":
        shop()

main_menu()