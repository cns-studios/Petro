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
    
    // Store original index with pet dada
    const sortedInventory = userInventory.map((pet, index) => ({
        ...pet,
        originalIndex: index
    })).sort((a, b) => {
        const rarityA = RARITY_ORDER[a.rarity?.toLowerCase()] || 999;
        const rarityB = RARITY_ORDER[b.rarity?.toLowerCase()] || 999;
        return rarityA - rarityB;
    });
    
    container.innerHTML = sortedInventory.map(pet => `
        <div class="pet-select-card" data-index="${pet.originalIndex}">
            <div class="pet-rarity ${pet.rarity?.toLowerCase() || 'common'}">${pet.rarity || 'Common'}</div>
            <strong>${pet.name}</strong>
            <div>Level: ${pet.level || 1}</div>
            <div>HP: ${pet.hp} | ATK: ${pet.attack}</div>
            <div>Dodge: ${pet.dodge_chance || 0}%</div>
        </div>
    `).join('');
    
    const cards = container.querySelectorAll('.pet-select-card');
    cards.forEach(card => {
        card.addEventListener('click', () => togglePetSelection(card));
    });
}

function togglePetSelection(card) {
    const petId = card.dataset.petId;
    const index = selectedPets.indexOf(petId);
    
    if (index > -1) {
        // Desel
        selectedPets.splice(index, 1);
        card.classList.remove('selected');
    } else {
        // Sel
        if (selectedPets.length < 3) {
            selectedPets.push(petId);
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
    // Get pet objects from inventory
    const selectedPetData = selectedPets.map(petId => {
        return userInventory[parseInt(petId)];
    });
    
    // Send selection to da damnn server
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
        ws.send(JSON.stringify({
            action: 'get_pregame_data'
        }));
    };
    
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log('Battle update:', data);
            if (data.type === 'pregame_data') {
                // Received inventory dada
                userInventory = data.inventory || [];
                userMoney = data.money || 0;
                setupPregameUI();
            } else if (data.type === 'battle_state') {
                battleState = data;
                
                if (data.phase === 'pregame') {
                    // Still in pregameeee
                    if (data.waiting_for) {
                        document.getElementById('pregame').innerHTML += 
                            `<p>Waiting for ${data.waiting_for} to select pets...</p>`;
                    }
                } else if (data.phase === 'battle' || !data.phase) {
                    // Battle start
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