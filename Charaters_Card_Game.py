level_multiplayer = 1
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








# rare
cat_stats = {"attack": 17 * level_multiplayer, "hp": 30 * level_multiplayer, "rarity": 2}






# legandary
anaconda_stats = {"attack": 30 * level_multiplayer, "hp": 80 * level_multiplayer, "rarity": 3}

