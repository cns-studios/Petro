
level_multiplayer = 1




common_pets = ["Ant", "Rat", "Snail", "Spider", "Bee", "Stag Beetle", "Cricket", "Grasshopper", "Ladybug", "Butterfly", "Moth", "Cockroach", "Fly", "Mosquito", "Beetle", "Slug", "Centipede", "Millipede", "Earwig", "Pill Bug", "Springtail", "Aphid", "Caterpillar", "Maggot", "Tick", "Flea", "Hamster", "Mouse", "Shrew"]

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
    "Cricket": 1,
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

cp = len(common_pets)

# starter
worm_stats = {"attack": 1 * level_multiplayer, "hp": 10 * level_multiplayer, "rarity": 0}

# common                                                                                           # 0 = starter, 1 = common, 2 = rare, 3 = legendary
ant_stats = {"attack": 2 * level_multiplayer, "hp": 15 * level_multiplayer, "rarity": 1} 
rat_stats = {"attack": 5 * level_multiplayer, "hp": 25 * level_multiplayer, "rarity": 1}
snail_stats = {"attack": 1 * level_multiplayer, "hp": 35 * level_multiplayer, "rarity": 1}
spider_stats = {"attack": 5 * level_multiplayer, "hp": 20 * level_multiplayer, "rarity": 1}
bee_stats = {"attack": 8 * level_multiplayer, "hp": 5 * level_multiplayer, "rarity": 1}
stag_beetle_stats = {"attack": 8 * level_multiplayer, "hp": 10 * level_multiplayer, "rarity": 1}
cricket_stats = {"attack": 3 * level_multiplayer, "hp": 12 * level_multiplayer, "rarity": 1}
grasshopper_stats = {"attack": 4 * level_multiplayer, "hp": 18 * level_multiplayer, "rarity": 1}
ladybug_stats = {"attack": 6 * level_multiplayer, "hp": 8 * level_multiplayer, "rarity": 1}
butterfly_stats = {"attack": 3 * level_multiplayer, "hp": 6 * level_multiplayer, "rarity": 1}
moth_stats = {"attack": 2 * level_multiplayer, "hp": 7 * level_multiplayer, "rarity": 1}
cockroach_stats = {"attack": 4 * level_multiplayer, "hp": 22 * level_multiplayer, "rarity": 1}
fly_stats = {"attack": 2 * level_multiplayer, "hp": 4 * level_multiplayer, "rarity": 1}
mosquito_stats = {"attack": 1 * level_multiplayer, "hp": 3 * level_multiplayer, "rarity": 1}
beetle_stats = {"attack": 7 * level_multiplayer, "hp": 14 * level_multiplayer, "rarity": 1}
slug_stats = {"attack": 1 * level_multiplayer, "hp": 30 * level_multiplayer, "rarity": 1}
centipede_stats = {"attack": 9 * level_multiplayer, "hp": 8 * level_multiplayer, "rarity": 1}
millipede_stats = {"attack": 2 * level_multiplayer, "hp": 16 * level_multiplayer, "rarity": 1}
earwig_stats = {"attack": 3 * level_multiplayer, "hp": 9 * level_multiplayer, "rarity": 1}
pill_bug_stats = {"attack": 2 * level_multiplayer, "hp": 20 * level_multiplayer, "rarity": 1}
springtail_stats = {"attack": 1 * level_multiplayer, "hp": 2 * level_multiplayer, "rarity": 1}
aphid_stats = {"attack": 1 * level_multiplayer, "hp": 1 * level_multiplayer, "rarity": 1}
caterpillar_stats = {"attack": 2 * level_multiplayer, "hp": 12 * level_multiplayer, "rarity": 1}
maggot_stats = {"attack": 1 * level_multiplayer, "hp": 5 * level_multiplayer, "rarity": 1}
tick_stats = {"attack": 3 * level_multiplayer, "hp": 4 * level_multiplayer, "rarity": 1}
flea_stats = {"attack": 2 * level_multiplayer, "hp": 2 * level_multiplayer, "rarity": 1}
hamster_stats = {"attack": 6 * level_multiplayer, "hp": 18 * level_multiplayer, "rarity": 1}
mouse_stats = {"attack": 4 * level_multiplayer, "hp": 12 * level_multiplayer, "rarity": 1}
shrew_stats = {"attack": 8 * level_multiplayer, "hp": 8 * level_multiplayer, "rarity": 1}

# rare
cat_stats = {"attack": 17 * level_multiplayer, "hp": 30 * level_multiplayer, "rarity": 2}
raccoon_stats = {"attack": 22 * level_multiplayer, "hp": 35 * level_multiplayer, "rarity": 2}
peregrine_falcon_stats = {"attack": 28 * level_multiplayer, "hp": 25 * level_multiplayer, "rarity": 2}
red_fox_stats = {"attack": 20 * level_multiplayer, "hp": 30 * level_multiplayer, "rarity": 2}
lynx_stats = {"attack": 25 * level_multiplayer, "hp": 40 * level_multiplayer, "rarity": 2}
otter_stats = {"attack": 15 * level_multiplayer, "hp": 35 * level_multiplayer, "rarity": 2}
hawk_stats = {"attack": 24 * level_multiplayer, "hp": 20 * level_multiplayer, "rarity": 2}
owl_stats = {"attack": 18 * level_multiplayer, "hp": 28 * level_multiplayer, "rarity": 2}
raven_stats = {"attack": 16 * level_multiplayer, "hp": 22 * level_multiplayer, "rarity": 2}
cobra_stats = {"attack": 26 * level_multiplayer, "hp": 32 * level_multiplayer, "rarity": 2}
monitor_lizard_stats = {"attack": 23 * level_multiplayer, "hp": 45 * level_multiplayer, "rarity": 2}
badger_stats = {"attack": 19 * level_multiplayer, "hp": 50 * level_multiplayer, "rarity": 2}
wolverine_stats = {"attack": 27 * level_multiplayer, "hp": 42 * level_multiplayer, "rarity": 2}
jackal_stats = {"attack": 21 * level_multiplayer, "hp": 28 * level_multiplayer, "rarity": 2}

# legendary
anaconda_stats = {"attack": 35 * level_multiplayer, "hp": 80 * level_multiplayer, "rarity": 3}
tiger_stats = {"attack": 45 * level_multiplayer, "hp": 70 * level_multiplayer, "rarity": 3}
wolf_stats = {"attack": 40 * level_multiplayer, "hp": 65 * level_multiplayer, "rarity": 3}
eagle_stats = {"attack": 35 * level_multiplayer, "hp": 50 * level_multiplayer, "rarity": 3}
shark_stats = {"attack": 50 * level_multiplayer, "hp": 90 * level_multiplayer, "rarity": 3}
crocodile_stats = {"attack": 55 * level_multiplayer, "hp": 100 * level_multiplayer, "rarity": 3}
lion_stats = {"attack": 48 * level_multiplayer, "hp": 75 * level_multiplayer, "rarity": 3}
bear_stats = {"attack": 38 * level_multiplayer, "hp": 120 * level_multiplayer, "rarity": 3}
falcon_stats = {"attack": 32 * level_multiplayer, "hp": 40 * level_multiplayer, "rarity": 3}
python_stats = {"attack": 28 * level_multiplayer, "hp": 85 * level_multiplayer, "rarity": 3}
komodo_dragon_stats = {"attack": 40 * level_multiplayer, "hp": 70 * level_multiplayer, "rarity": 3}
elephant_stats = {"attack": 30 * level_multiplayer, "hp": 150 * level_multiplayer, "rarity": 3}