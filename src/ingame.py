import sys
import json
import random
import time
from logic import pull_state

class Battle:
    def __init__(self, battle_id, player1_name, player2_name):
        self.battle_id = battle_id
        self.player1_name = player1_name
        self.player2_name = player2_name
        
        # Load player states
        self.p1_state = pull_state(player1_name)
        self.p2_state = pull_state(player2_name)
        
        if not self.p1_state or not self.p2_state:
            self.send_error("Failed to load player data")
            sys.exit(1)
        
        # Pregame phase
        self.phase = 'pregame'
        self.player1_ready = False
        self.player2_ready = False
        self.player1_pets = []
        self.player2_pets = []
        self.player1_bet = 0
        self.player2_bet = 0
        
        # Battle state
        self.current_turn = player1_name
        self.turn_number = 1
        self.battle_log = []
        self.p1_active = 0
        self.p2_active = 0
        self.winner = None

    def send_pregame_data(self, username):
        state = self.p1_state if username == self.player1_name else self.p2_state
        inventory = state.get('inventory', [])
        money = state.get('money', 0)
        
        self.send_json({
            'type': 'pregame_data',
            'inventory': inventory,
            'money': money
        })
        
    def get_state(self, message=""):
        if self.phase == 'pregame':
            waiting_for = []
            if not self.player1_ready:
                waiting_for.append(self.player1_name)
            if not self.player2_ready:
                waiting_for.append(self.player2_name)
                
            return {
                'type': 'battle_state',
                'phase': 'pregame',
                'battle_id': self.battle_id,
                'waiting_for': ', '.join(waiting_for) if waiting_for else None,
                'message': message
            }
        else:
            return {
                'type': 'battle_state',
                'phase': 'battle',
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
    
    def send_json(self, data):
        print(json.dumps(data))
        sys.stdout.flush()
    
    def add_log(self, message):
        self.battle_log.append(f"Turn {self.turn_number}: {message}")
    
    def handle_pet_selection(self, username, data):
        try:
            pets_data = data.get('pets', [])
            bet = data.get('bet', 0)
            
            # Convert pets for da battle format
            pets = []
            for pet_data in pets_data[:3]:  # max 3 pets
                pets.append({
                    'name': pet_data['name'],
                    'hp': pet_data['hp'],
                    'max_hp': pet_data['hp'],
                    'attack': pet_data['attack'],
                    'dodge_chance': pet_data.get('dodge_chance', 0),
                    'level': pet_data.get('level', 1),
                    'alive': True
                })
            
            if username == self.player1_name:
                self.player1_pets = pets
                self.player1_bet = bet
                self.player1_ready = True
            else:
                self.player2_pets = pets
                self.player2_bet = bet
                self.player2_ready = True
            
            self.send_json({
                'type': 'selection_confirmed',
                'message': f'{username} is ready'
            })
            
            if self.player1_ready and self.player2_ready:
                self.start_battle()
        except Exception as e:
            self.send_error(f"Failed to process selection: {str(e)}")
    
    def start_battle(self):
        """Start the actual battle"""
        self.phase = 'battle'
        self.add_log(f"Battle started! {self.player1_name} vs {self.player2_name}")
        self.send_json({'type': 'battle_start'})
        self.send_state("Battle has begun!")
    
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
        if self.phase != 'battle':
            self.send_error("Battle hasn't started yet!")
            return
            
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
        
        # Switch turns
        self.current_turn = self.player2_name if self.current_turn == self.player1_name else self.player1_name
        self.turn_number += 1
        
        self.send_state(f"{self.current_turn}'s turn")
    
    def process_command(self, username, command):
        # Try to parse as JSON first
        try:
            data = json.loads(command)
            if data.get('action') == 'select_pets':
                self.handle_pet_selection(username, data)
                return
        except json.JSONDecodeError:
            pass
        
        # Handle text commands
        parts = command.strip().lower().split()
        action = parts[0] if parts else ""
        
        if action == "get_state":
            self.send_state("Battle state")
        elif action == "get_pregame_data":
            self.send_pregame_data(username)
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
    battle.send_state(f"[Ingame] Battle lobby created! {player1} vs {player2}")
    
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