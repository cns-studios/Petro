let ws;
let currentUsername;
let currentPin;
let battleState = null;
let userInventory = [];
let userMoney = 0;
let selectedPets = [];
let selectedBet = 0;

const RARITY_ORDER = {
    'common': 1,
    'rare': 2,
    'legendary': 3
};

function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        battleId: params.get('battleId'),
        username: params.get('username'),
        pin: params.get('pin')
    };
}

window.addEventListener('DOMContentLoaded', () => {
    const params = getQueryParams();
    
    if (!params.battleId || !params.username || !params.pin) {
        alert('Invalid battle parameters');
        window.location.href = '/game';
        return;
    }
    
    currentUsername = params.username;
    currentPin = params.pin;
    
    // Connect => data via ws
    connectBattle(params.battleId, params.username, params.pin);
});

function setupPregameUI() {
    setupPetSelection();
    setupBetSelection();
    setupStartButton();
}

function setupPetSelection() {
    const container = document.getElementById('pet-selection-container');
    
    // Sort pets by rarity - handle missing/invalid rarity values
    const sortedInventory = userInventory.map((pet, index) => ({
        ...pet,
        originalIndex: index,
        rarity: (pet.rarity || 'common').toString().toLowerCase()
    })).sort((a, b) => {
        const rarityA = RARITY_ORDER[a.rarity] || 999;
        const rarityB = RARITY_ORDER[b.rarity] || 999;
        return rarityA - rarityB;
    });
    
    container.innerHTML = sortedInventory.map(pet => {
        // Safely handle all pet properties lol
        const name = pet.name || 'Unknown Pet';
        const level = pet.level || 1;
        const hp = pet.hp || 0;
        const attack = pet.attack || 0;
        const dodgeChance = pet.dodge_chance || 0;
        const rarityClass = pet.rarity || 'common';
        const rarityDisplay = rarityClass.charAt(0).toUpperCase() + rarityClass.slice(1);
        
        return `
            <div class="pet-select-card" data-index="${pet.originalIndex}">
                <div class="pet-rarity ${rarityClass}">${rarityDisplay}</div>
                <strong>${name}</strong>
                <div>Level: ${level}</div>
                <div>HP: ${hp} | ATK: ${attack}</div>
                <div>Dodge: ${dodgeChance}%</div>
            </div>
        `;
    }).join('');
    
    const cards = container.querySelectorAll('.pet-select-card');
    cards.forEach(card => {
        card.addEventListener('click', () => togglePetSelection(card));
    });
}

function togglePetSelection(card) {
    const petIndex = card.dataset.index;
    const indexStr = petIndex.toString();
    const arrayIndex = selectedPets.indexOf(indexStr);
    
    if (arrayIndex > -1) {
        // Des
        selectedPets.splice(arrayIndex, 1);
        card.classList.remove('selected');
    } else {
        // Sel
        if (selectedPets.length < 3) {
            selectedPets.push(indexStr);
            card.classList.add('selected');
        } else {
            alert('You can only select 3 pets!');
        }
    }
    
    updateSelectedCount();
    updateStartButton();
}

function updateSelectedCount() {
    document.getElementById('selected-count').textContent = selectedPets.length;
}

function setupBetSelection() {
    const slider = document.getElementById('bet-slider');
    const betAmount = document.getElementById('bet-amount');
    const maxBetDisplay = document.getElementById('max-bet-display');
    
    slider.max = userMoney;
    maxBetDisplay.textContent = `Max: $${userMoney}`;
    
    slider.addEventListener('input', (e) => {
        selectedBet = parseInt(e.target.value);
        betAmount.textContent = selectedBet;
    });
}

function setupStartButton() {
    const startBtn = document.getElementById('startBattle-btn');
    startBtn.addEventListener('click', () => {
        if (selectedPets.length === 3) {
            startBattle();
        }
    });
}

function updateStartButton() {
    const startBtn = document.getElementById('startBattle-btn');
    startBtn.disabled = selectedPets.length !== 3;
}


function startBattle() {
    const selectedPetData = selectedPets.map(petIndex => {
        const pet = userInventory[parseInt(petIndex)];
        if (!pet) {
            console.error(`Pet at index ${petIndex} not found`);
            return null;
        }
        return {
            name: pet.name || 'Unknown Pet',
            hp: pet.hp || 100,
            attack: pet.attack || 10,
            dodge_chance: pet.dodge_chance || 0,
            level: pet.level || 1,
            rarity: pet.rarity || 'common'
        };
    }).filter(pet => pet !== null);
    
    if (selectedPetData.length !== 3) {
        alert('Please select exactly 3 valid pets');
        return;
    }
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            action: 'select_pets',
            pets: selectedPetData,
            bet: selectedBet
        }));
    }
}

function connectBattle(battleId, username, pin) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/battle?battleId=${battleId}&username=${encodeURIComponent(username)}&pin=${encodeURIComponent(pin)}`);
    
    ws.onopen = () => {
        console.log('Connected to battle');
        ws.send('get_pregame_data');  // Send as simple string
    };
    
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log('Battle update:', data);
            
            if (data.type === 'pregame_data') {
                // Validate and clean inventory data
                userInventory = (data.inventory || []).map(pet => ({
                    name: pet.name || 'Unknown',
                    hp: parseInt(pet.hp) || 100,
                    attack: parseInt(pet.attack) || 10,
                    dodge_chance: parseInt(pet.dodge_chance) || 0,
                    level: parseInt(pet.level) || 1,
                    rarity: (pet.rarity || 'common').toString().toLowerCase()
                }));
                userMoney = parseInt(data.money) || 0;
                setupPregameUI();
            } else if (data.type === 'battle_state') {
                battleState = data;
                
                if (data.phase === 'pregame') {
                    if (data.waiting_for) {
                        const waitingDiv = document.getElementById('waiting-message');
                        if (!waitingDiv) {
                            const div = document.createElement('div');
                            div.id = 'waiting-message';
                            div.innerHTML = `<p>Waiting for ${data.waiting_for} to select pets...</p>`;
                            document.getElementById('pregame').appendChild(div);
                        }
                    }
                } else if (data.phase === 'battle') {
                    document.getElementById('pregame').style.display = 'none';
                    document.getElementById('ingame').style.display = 'block';
                    updateBattleUI(data);
                }
            } else if (data.type === 'selection_confirmed') {
                document.getElementById('startBattle-btn').disabled = true;
                document.getElementById('startBattle-btn').textContent = 'Waiting for opponent...';
            } else if (data.type === 'battle_start') {
                document.getElementById('pregame').style.display = 'none';
                document.getElementById('ingame').style.display = 'block';
            } else if (data.type === 'battle_ended') {
                setTimeout(() => {
                    window.location.href = '/game';
                }, 5000);
            } else if (data.type === 'error') {
                alert(data.message);
            }
        } catch (e) {
            console.error('Failed to parse battle data:', e);
            console.error('Raw data:', event.data);
        }
    };
    
    ws.onclose = () => {
        console.log('Battle connection closed');
    };
    
    ws.onerror = (error) => {
        console.error('Battle WebSocket error:', error);
    };
}

function updateBattleUI(state) {
    // turn indicator
    const turnIndicator = document.getElementById('turn-indicator');
    const isMyTurn = state.current_turn === currentUsername;
    turnIndicator.innerHTML = `<h2>Turn ${state.turn_number} - ${isMyTurn ? 'YOUR TURN' : state.current_turn + "'s Turn"}</h2>`;
    
    // player sections
    document.getElementById('player1-name').textContent = state.player1.name;
    document.getElementById('player2-name').textContent = state.player2.name;
    
    document.getElementById('player1-section').classList.toggle('active', state.current_turn === state.player1.name);
    document.getElementById('player2-section').classList.toggle('active', state.current_turn === state.player2.name);
    
    updatePets('player1-pets', state.player1.pets, state.player1.active_pet);
    updatePets('player2-pets', state.player2.pets, state.player2.active_pet);
    
    // battle log
    const logMessages = document.getElementById('log-messages');
    logMessages.innerHTML = state.battle_log.map(msg => `<p>${msg}</p>`).join('');
    logMessages.scrollTop = logMessages.scrollHeight;
    
    // Enable/disable attack button
    document.getElementById('attack-btn').disabled = !isMyTurn || state.winner;
    
    if (state.winner) {
        const banner = document.getElementById('winner-banner');
        banner.textContent = state.winner === currentUsername ? 'YOU WIN!' : state.winner + ' WINS!';
        banner.style.display = 'block';
    }
}

function updatePets(elementId, pets, activeIndex) {
    const container = document.getElementById(elementId);
    container.innerHTML = pets.map((pet, index) => {
        const hpPercent = (pet.hp / pet.max_hp) * 100;
        return `
            <div class="pet-card ${index === activeIndex ? 'active' : ''} ${!pet.alive ? 'dead' : ''}">
                <strong>${pet.name}</strong> (Lv. ${pet.level})
                <div>ATK: ${pet.attack} | Dodge: ${pet.dodge_chance}%</div>
                <div>HP: ${pet.hp}/${pet.max_hp}</div>
                <div class="hp-bar">
                    <div class="hp-fill" style="width: ${hpPercent}%"></div>
                </div>
            </div>
        `;
    }).join('');
}

function attack() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('attack');
    }
}