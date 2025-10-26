import sys
import json
import random
import sqlite3
import os
import copy
from assets.pets import all_pet_stats as global_pet_stats, common_pets as global_common_pets, rare_pets as global_rare_pets, legendary_pets as global_legendary_pets, pet_levels as global_pet_levels, all_pets

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'users.db')

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
                'legendary': game.available_legendary_pets,
                'prehistoric': game.available_prehistoric_pets
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



if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else None
    if not username:
        print(json.dumps({"message": "Error: Username not provided."}))
        sys.exit(1)
    
    if not username.replace("_", "").replace("-", "").isalnum():
        print(json.dumps({"message": "Error: Invalid username format."}))
        sys.exit(1)

    try:
        from shop import Game
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