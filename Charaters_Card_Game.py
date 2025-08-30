
level_multiplayer = 1


starter_pets = ["Worm"]

common_pets = ["Ant", "Rat", "Snail", "Spider", "Bee", "Stag Beetle", "Grasshopper", "Ladybug", "Butterfly", "Moth", "Cockroach", "Fly", "Mosquito", "Beetle", "Slug", "Centipede", "Millipede", "Earwig", "Pill Bug", "Springtail", "Aphid", "Caterpillar", "Maggot", "Tick", "Flea", "Hamster", "Mouse", "Shrew"]

rare_pets = ["Cat", "Raccoon", "Peregrine Falcon", "Red Fox", "Lynx", "Otter", "Hawk", "Owl", "Raven", "Cobra", "Monitor Lizard", "Badger", "Wolverine", "Jackal"]

legendary_pets = ["Anaconda", "Tiger", "Wolf", "Eagle", "Shark", "Crocodile", "Lion", "Bear", "Falcon", "Python","Komodo Dragon", "Elephant"]

pet_levels = {
    "Worm": 1,
    "Ant": 1,
    "Rat": 1,
    "Snail": 1,
    "Spider": 1,
    "Bee": 1,
    "Stag Beetle": 1,
    "Grasshopper": 1,
    "Ladybug": 1,
    "Butterfly": 1,
    "Moth": 1,
    "Cockroach": 1,
    "Fly": 1,
    "Mosquito": 1,
    "Beetle": 1,
    "Slug": 1,
    "Centipede": 1,
    "Millipede": 1,
    "Earwig": 1,
    "Pill Bug": 1,
    "Springtail": 1,
    "Aphid": 1,
    "Caterpillar": 1,
    "Maggot": 1,
    "Tick": 1,
    "Flea": 1,
    "Hamster": 1,
    "Mouse": 1,
    "Shrew": 1,
    "Cat": 1,
    "Raccoon": 1,
    "Peregrine Falcon": 1,
    "Red Fox": 1,
    "Lynx": 1,
    "Otter": 1,
    "Hawk": 1,
    "Owl": 1,
    "Raven": 1,
    "Cobra": 1,
    "Monitor Lizard": 1,
    "Komodo Dragon": 1,
    "Badger": 1,
    "Wolverine": 1,
    "Jackal": 1,
    "Anaconda": 1,
    "Tiger": 1,
    "Wolf": 1,
    "Eagle": 1,
    "Shark": 1,
    "Crocodile": 1,
    "Lion": 1,
    "Bear": 1,
    "Falcon": 1,
    "Python": 1,
    "Elephant":1,
}



#class Pet:
#1 = Tank
#2 = Poisoner
#3 = Assassin
#4 = Berserker
#5 = Aerial
#6 = Dodger
#7 = Digger

# common
worm_stats = {"attack": 1 * level_multiplayer, "hp": 10 * level_multiplayer, "rarity": 0, "dodge_chance": 5, "class": [7]}
ant_stats = {"attack": 2 * level_multiplayer, "hp": 15 * level_multiplayer, "rarity": 1, "dodge_chance": 10, "class": [7]}
rat_stats = {"attack": 5 * level_multiplayer, "hp": 25 * level_multiplayer, "rarity": 1, "dodge_chance": 12, "class": [6]}
snail_stats = {"attack": 1 * level_multiplayer, "hp": 35 * level_multiplayer, "rarity": 1, "dodge_chance": 2, "class": [1]}
spider_stats = {"attack": 5 * level_multiplayer, "hp": 20 * level_multiplayer, "rarity": 1, "dodge_chance": 15, "class": [2, 6]}
bee_stats = {"attack": 8 * level_multiplayer, "hp": 5 * level_multiplayer, "rarity": 1, "dodge_chance": 25, "class": [5, 6, 2]}
stag_beetle_stats = {"attack": 8 * level_multiplayer, "hp": 10 * level_multiplayer, "rarity": 1, "dodge_chance": 10, "class": [4]}
cricket_stats = {"attack": 3 * level_multiplayer, "hp": 12 * level_multiplayer, "rarity": 1, "dodge_chance": 20, "class": [6]}
grasshopper_stats = {"attack": 4 * level_multiplayer, "hp": 18 * level_multiplayer, "rarity": 1, "dodge_chance": 18, "class": [6]}
ladybug_stats = {"attack": 6 * level_multiplayer, "hp": 8 * level_multiplayer, "rarity": 1, "dodge_chance": 10, "class": [5]}
butterfly_stats = {"attack": 3 * level_multiplayer, "hp": 6 * level_multiplayer, "rarity": 1, "dodge_chance": 22, "class": [5, 6]}
moth_stats = {"attack": 2 * level_multiplayer, "hp": 7 * level_multiplayer, "rarity": 1, "dodge_chance": 18, "class": [5, 6]}
cockroach_stats = {"attack": 4 * level_multiplayer, "hp": 22 * level_multiplayer, "rarity": 1, "dodge_chance": 30, "class": [6]}
fly_stats = {"attack": 2 * level_multiplayer, "hp": 4 * level_multiplayer, "rarity": 1, "dodge_chance": 40, "class": [5, 6]}
mosquito_stats = {"attack": 1 * level_multiplayer, "hp": 3 * level_multiplayer, "rarity": 1, "dodge_chance": 38, "class": [5, 6, 2]}
beetle_stats = {"attack": 7 * level_multiplayer, "hp": 14 * level_multiplayer, "rarity": 1, "dodge_chance": 8, "class": [1]}
slug_stats = {"attack": 0.5 * level_multiplayer, "hp": 1 * level_multiplayer, "rarity": 1, "dodge_chance": 0, "class": [2]}
centipede_stats = {"attack": 9 * level_multiplayer, "hp": 8 * level_multiplayer, "rarity": 1, "dodge_chance": 25, "class": [2, 3]}
millipede_stats = {"attack": 2 * level_multiplayer, "hp": 16 * level_multiplayer, "rarity": 1, "dodge_chance": 5, "class": [1]}
earwig_stats = {"attack": 3 * level_multiplayer, "hp": 9 * level_multiplayer, "rarity": 1, "dodge_chance": 12, "class": [3]}
pill_bug_stats = {"attack": 2 * level_multiplayer, "hp": 20 * level_multiplayer, "rarity": 1, "dodge_chance": 4, "class": [1]}
springtail_stats = {"attack": 1 * level_multiplayer, "hp": 2 * level_multiplayer, "rarity": 1, "dodge_chance": 35, "class": [6]}
aphid_stats = {"attack": 1 * level_multiplayer, "hp": 1 * level_multiplayer, "rarity": 1, "dodge_chance": 37, "class": [6]}
caterpillar_stats = {"attack": 2 * level_multiplayer, "hp": 12 * level_multiplayer, "rarity": 1, "dodge_chance": 6, "class": [1]}
maggot_stats = {"attack": 1 * level_multiplayer, "hp": 5 * level_multiplayer, "rarity": 1, "dodge_chance": 3, "class": [7]}
tick_stats = {"attack": 3 * level_multiplayer, "hp": 4 * level_multiplayer, "rarity": 1, "dodge_chance": 28, "class": [2, 6]}
flea_stats = {"attack": 2 * level_multiplayer, "hp": 2 * level_multiplayer, "rarity": 1, "dodge_chance": 33, "class": [6]}
hamster_stats = {"attack": 6 * level_multiplayer, "hp": 18 * level_multiplayer, "rarity": 1, "dodge_chance": 8, "class": [6]}
mouse_stats = {"attack": 4 * level_multiplayer, "hp": 12 * level_multiplayer, "rarity": 1, "dodge_chance": 12, "class": [6]}
shrew_stats = {"attack": 8 * level_multiplayer, "hp": 8 * level_multiplayer, "rarity": 1, "dodge_chance": 14, "class": [3]}

# rare
cat_stats = {"attack": 17 * level_multiplayer, "hp": 30 * level_multiplayer, "rarity": 2, "dodge_chance": 18, "class": [3, 6]}
raccoon_stats = {"attack": 22 * level_multiplayer, "hp": 35 * level_multiplayer, "rarity": 2, "dodge_chance": 15, "class": [6]}
peregrine_falcon_stats = {"attack": 28 * level_multiplayer, "hp": 25 * level_multiplayer, "rarity": 2, "dodge_chance": 30, "class": [5, 3]}
red_fox_stats = {"attack": 20 * level_multiplayer, "hp": 30 * level_multiplayer, "rarity": 2, "dodge_chance": 16, "class": [3, 6]}
lynx_stats = {"attack": 25 * level_multiplayer, "hp": 40 * level_multiplayer, "rarity": 2, "dodge_chance": 14, "class": [3]}
otter_stats = {"attack": 15 * level_multiplayer, "hp": 35 * level_multiplayer, "rarity": 2, "dodge_chance": 10, "class": [1]}
hawk_stats = {"attack": 24 * level_multiplayer, "hp": 20 * level_multiplayer, "rarity": 2, "dodge_chance": 22, "class": [5, 3]}
owl_stats = {"attack": 18 * level_multiplayer, "hp": 28 * level_multiplayer, "rarity": 2, "dodge_chance": 18, "class": [5, 3]}
raven_stats = {"attack": 16 * level_multiplayer, "hp": 22 * level_multiplayer, "rarity": 2, "dodge_chance": 20, "class": [5, 6]}
cobra_stats = {"attack": 26 * level_multiplayer, "hp": 32 * level_multiplayer, "rarity": 2, "dodge_chance": 5, "class": [2, 3]}
monitor_lizard_stats = {"attack": 23 * level_multiplayer, "hp": 45 * level_multiplayer, "rarity": 2, "dodge_chance": 4, "class": [3]}
badger_stats = {"attack": 19 * level_multiplayer, "hp": 50 * level_multiplayer, "rarity": 2, "dodge_chance": 6, "class": [1, 7]}
wolverine_stats = {"attack": 27 * level_multiplayer, "hp": 42 * level_multiplayer, "rarity": 2, "dodge_chance": 8, "class": [4]}
jackal_stats = {"attack": 21 * level_multiplayer, "hp": 28 * level_multiplayer, "rarity": 2, "dodge_chance": 12, "class": [3, 6]}

# legendary
anaconda_stats = {"attack": 35 * level_multiplayer, "hp": 80 * level_multiplayer, "rarity": 3, "dodge_chance": 2, "class": [1, 2]}
tiger_stats = {"attack": 45 * level_multiplayer, "hp": 70 * level_multiplayer, "rarity": 3, "dodge_chance": 6, "class": [3, 4]}
wolf_stats = {"attack": 40 * level_multiplayer, "hp": 65 * level_multiplayer, "rarity": 3, "dodge_chance": 10, "class": [3]}
eagle_stats = {"attack": 35 * level_multiplayer, "hp": 50 * level_multiplayer, "rarity": 3, "dodge_chance": 28, "class": [5, 3]}
shark_stats = {"attack": 50 * level_multiplayer, "hp": 90 * level_multiplayer, "rarity": 3, "dodge_chance": 0, "class": [4]}
crocodile_stats = {"attack": 55 * level_multiplayer, "hp": 100 * level_multiplayer, "rarity": 3, "dodge_chance": 1, "class": [1, 4]}
lion_stats = {"attack": 48 * level_multiplayer, "hp": 75 * level_multiplayer, "rarity": 3, "dodge_chance": 4, "class": [4]}
bear_stats = {"attack": 38 * level_multiplayer, "hp": 120 * level_multiplayer, "rarity": 3, "dodge_chance": 3, "class": [1]}
falcon_stats = {"attack": 32 * level_multiplayer, "hp": 40 * level_multiplayer, "rarity": 3, "dodge_chance": 25, "class": [5, 3]}
python_stats = {"attack": 28 * level_multiplayer, "hp": 85 * level_multiplayer, "rarity": 3, "dodge_chance": 9, "class": [1, 2]}
komodo_dragon_stats = {"attack": 40 * level_multiplayer, "hp": 70 * level_multiplayer, "rarity": 3, "dodge_chance": 2, "class": [2, 4]}
elephant_stats = {"attack": 30 * level_multiplayer, "hp": 150 * level_multiplayer, "rarity": 3, "dodge_chance": 0, "class": [1]}



all_pet_stats = {
    "Worm": worm_stats,
    "Ant": ant_stats,
    "Rat": rat_stats,
    "Snail": snail_stats,
    "Spider": spider_stats,
    "Bee": bee_stats,
    "Stag Beetle": stag_beetle_stats,
    "Grasshopper": grasshopper_stats,
    "Ladybug": ladybug_stats,
    "Butterfly": butterfly_stats,
    "Moth": moth_stats,
    "Cockroach": cockroach_stats,
    "Fly": fly_stats,
    "Mosquito": mosquito_stats,
    "Beetle": beetle_stats,
    "Slug": slug_stats,
    "Centipede": centipede_stats,
    "Millipede": millipede_stats,
    "Earwig": earwig_stats,
    "Pill Bug": pill_bug_stats,
    "Springtail": springtail_stats,
    "Aphid": aphid_stats,
    "Caterpillar": caterpillar_stats,
    "Maggot": maggot_stats,
    "Tick": tick_stats,
    "Flea": flea_stats,
    "Hamster": hamster_stats,
    "Mouse": mouse_stats,
    "Shrew": shrew_stats,
    "Cat": cat_stats,
    "Raccoon": raccoon_stats,
    "Peregrine Falcon": peregrine_falcon_stats,
    "Red Fox": red_fox_stats,
    "Lynx": lynx_stats,
    "Otter": otter_stats,
    "Hawk": hawk_stats,
    "Owl": owl_stats,
    "Raven": raven_stats,
    "Cobra": cobra_stats,
    "Monitor Lizard": monitor_lizard_stats,
    "Badger": badger_stats,
    "Wolverine": wolverine_stats,
    "Jackal": jackal_stats,
    "Anaconda": anaconda_stats,
    "Tiger": tiger_stats,
    "Wolf": wolf_stats,
    "Eagle": eagle_stats,
    "Shark": shark_stats,
    "Crocodile": crocodile_stats,
    "Lion": lion_stats,
    "Bear": bear_stats,
    "Falcon": falcon_stats,
    "Python": python_stats,
    "Komodo Dragon": komodo_dragon_stats,
    "Elephant": elephant_stats
}


all_pets = [
        "Worm",
        "Ant",
        "Rat",
        "Snail",
        "Spider",
        "Bee",
        "Stag Beetle,"
        "Grasshopper",
        "Ladybug",
        "Butterfly",
        "Moth",
        "Cockroach",
        "Fly",
        "Mosquito",
        "Beetle",
        "Slug",
        "Centipede",
        "Millipede",
        "Earwig",
        "Pill Bug",
        "Springtail",
        "Aphid",
        "Caterpillar",
        "Maggot",
        "Tick",
        "Flea",
        "Hamster",
        "Mouse",
        "Shrew",
        "Cat",
        "Raccoon",
        "Peregrine Falcon",
        "Red Fox",
        "Lynx",
        "Otter",
        "Hawk",
        "Owl",
        "Raven",
        "Cobra",
        "Monitor Lizard",
        "Badger",
        "Wolverine",
        "Jackal",
        "Anaconda",
        "Tiger",
        "Wolf",
        "Eagle",
        "Shark",
        "Crocodile",
        "Lion",
        "Bear",
        "Falcon",
        "Python",
        "Komodo Dragon",
        "Elephant"
        ]

