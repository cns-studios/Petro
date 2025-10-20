import sys
import json
import random
import time
from logic import pull_state

class Battle:

    # TEMPORARY GAME FOR DEBUGGING BJARNE!11!1!!!!

    def __init__(self, battle_id, player1_name, player2_name):
        self.battle_id = battle_id
        self.player1_name = player1_name
        self.player2_name = player2_name
        
        # Load player inventories
        p1_state = pull_state(player1_name)
        p2_state = pull_state(player2_name)
        
        if not p1_state or not p2_state:
            self.send_error("Failed to load player data")
            sys.exit(1)
        
        # Get first 3 pets from each player's inventory
        self.player1_pets = self.load_pets(p1_state)
        self.player2_pets = self.load_pets(p2_state)
        
        self.current_turn = player1_name
        self.turn_number = 1
        self.battle_log = []
        
        # Current active pets (index)
        self.p1_active = 0
        self.p2_active = 0
        
        self.winner = None
        
    def load_pets(self, state):
        pets = []
        inventory = state.get('inventory', [])[:3]
        
        for pet_data in inventory:
            pets.append({
                'name': pet_data['name'],
                'hp': pet_data['hp'],
                'max_hp': pet_data['hp'],
                'attack': pet_data['attack'],
                'dodge_chance': pet_data['dodge_chance'],
                'level': pet_data['level'],
                'alive': True
            })
        
        return pets
    
    def get_state(self, message=""):
        """Return current state"""
        return {
            'type': 'battle_state',
            'battle_id': self.battle_id,
            'player1': {
                'name': self.player1_name,
                'pets': self.player1_pets,
                'active_pet': self.p1_active
            },
            'player2': {
                'name': self.player2_name,
                'pets': self.player2_pets,
                'active_pet': self.p2_active
            },
            'current_turn': self.current_turn,
            'turn_number': self.turn_number,
            'battle_log': self.battle_log[-5:],
            'message': message,
            'winner': self.winner
        }
    
    def send_state(self, message=""):
        print(json.dumps(self.get_state(message)))
        sys.stdout.flush()
    
    def send_error(self, error_msg):
        print(json.dumps({'type': 'error', 'message': error_msg}))
        sys.stdout.flush()
    
    def add_log(self, message):
        self.battle_log.append(f"Turn {self.turn_number}: {message}")
    
    def get_active_pet(self, player):
        """Get the current active pet for a player"""
        if player == self.player1_name:
            return self.player1_pets[self.p1_active] if self.p1_active < len(self.player1_pets) else None
        else:
            return self.player2_pets[self.p2_active] if self.p2_active < len(self.player2_pets) else None
    
    def switch_to_next_pet(self, player):
        """Switch to next alive pet"""
        if player == self.player1_name:
            pets = self.player1_pets
            for i, pet in enumerate(pets):
                if pet['alive'] and i != self.p1_active:
                    self.p1_active = i
                    return True
            return False
        else:
            pets = self.player2_pets
            for i, pet in enumerate(pets):
                if pet['alive'] and i != self.p2_active:
                    self.p2_active = i
                    return True
            return False
    
    def check_winner(self):
        p1_alive = any(pet['alive'] for pet in self.player1_pets)
        p2_alive = any(pet['alive'] for pet in self.player2_pets)
        
        if not p1_alive:
            self.winner = self.player2_name
            return True
        elif not p2_alive:
            self.winner = self.player1_name
            return True
        return False
    
    def execute_attack(self, attacker_name):
        if attacker_name != self.current_turn:
            self.send_state("Not your turn!")
            return
        
        if attacker_name == self.player1_name:
            attacker = self.player1_pets[self.p1_active]
            defender = self.player2_pets[self.p2_active]
            defender_name = self.player2_name
        else:
            attacker = self.player2_pets[self.p2_active]
            defender = self.player1_pets[self.p1_active]
            defender_name = self.player1_name
        
        if random.randint(1, 100) <= defender['dodge_chance']:
            self.add_log(f"{defender['name']} dodged {attacker['name']}'s attack!")
        else:
            damage = attacker['attack']
            defender['hp'] -= damage
            self.add_log(f"{attacker['name']} dealt {damage} damage to {defender['name']}")
            
            if defender['hp'] <= 0:
                defender['hp'] = 0
                defender['alive'] = False
                self.add_log(f"{defender['name']} fainted!")
                
                if not self.switch_to_next_pet(defender_name):
                    if self.check_winner():
                        self.add_log(f"{self.winner} wins the battle!")
                        self.send_state(f"{self.winner} is victorious!")
                        return
        
        # swutch turns
        self.current_turn = self.player2_name if self.current_turn == self.player1_name else self.player1_name
        self.turn_number += 1
        
        self.send_state(f"{self.current_turn}'s turn")
    
    def process_command(self, username, command):
        parts = command.strip().lower().split()
        action = parts[0] if parts else ""
        
        if action == "get_state":
            self.send_state("Battle in progress")
        elif action == "attack":
            self.execute_attack(username)
        elif action == "switch":
            if len(parts) < 2:
                self.send_state("Specify pet index to switch")
                return
            try:
                pet_index = int(parts[1])
                if username == self.player1_name:
                    if 0 <= pet_index < len(self.player1_pets) and self.player1_pets[pet_index]['alive']:
                        self.p1_active = pet_index
                        self.add_log(f"{username} switched to {self.player1_pets[pet_index]['name']}")
                        self.send_state(f"{username} switched pets")
                else:
                    if 0 <= pet_index < len(self.player2_pets) and self.player2_pets[pet_index]['alive']:
                        self.p2_active = pet_index
                        self.add_log(f"{username} switched to {self.player2_pets[pet_index]['name']}")
                        self.send_state(f"{username} switched pets")
            except (ValueError, IndexError):
                self.send_state("Invalid pet index")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"type": "error", "message": "Invalid arguments"}))
        sys.exit(1)
    
    battle_id = sys.argv[1]
    player1 = sys.argv[2]
    player2 = sys.argv[3]
    
    battle = Battle(battle_id, player1, player2)
    battle.send_state(f"Battle started! {player1} vs {player2}")
    
    try:
        for line in sys.stdin:
            command = line.strip()
            if not command or command == "exit":
                break
            
            if ':' in command:
                username, cmd = command.split(':', 1)
                battle.process_command(username, cmd)
            else:
                battle.send_state("Invalid command format")
                
    except Exception as e:
        print(json.dumps({"type": "error", "message": str(e)}))
        sys.stderr.write(f"Battle error: {str(e)}\n")