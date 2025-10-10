let ws;

function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
}

function logout() {
    deleteCookie('username');
    deleteCookie('pin');
    if (ws) {
        ws.close();
    }
    window.location.href = '/login.html';
}

window.addEventListener('DOMContentLoaded', () => {
    const username = getCookie('username');
    const pin = getCookie('pin');

    if (!username || !pin) {
        window.location.href = '/login.html';
    } else {
        connectWebSocket(username, pin);
    }
});

const moneyEl = document.getElementById('money');
const stageEl = document.getElementById('stage');
const inventoryEl = document.getElementById('inventory');
const messageEl = document.getElementById('message');

const shopUpEl = document.getElementById('shop-up');
const shopBpEl = document.getElementById('shop-bp');
const shopCpEl = document.getElementById('shop-cp');
const shopLupEl = document.getElementById('shop-lup');
const rerollPriceEl = document.getElementById('reroll-price');

const buffSelectionModal = document.getElementById('buff-selection');
const buffChoicesEl = document.getElementById('buff-choices');

const BUFF_DESCRIPTIONS = {
    1: "+1 Attack for all Pets",
    2: "+1 HP for all Pets",
    3: "+2% Dodge Chance for all Pets",
    4: "+2 Attack for all Common Pets", 
    5: "+2 HP for all Common Pets",
    6: "+3 Attack for all Rare Pets",
    7: "+3 HP for all Rare Pets",
    8: "+5 Attack for all Legendary Pets",
    9: "+5 HP for all Legendary Pets",
    10: "+1 Money for every Pet in Inventory",
    11: "+2 Money for every Common Pet and -1 for each Rare Pet in Inventory",
    12: "Double the Money you have (Max. 25)",
    13: "+1 Level for all Pets",
};

let stateRequestTimeout = null;

function Petsell() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('sell_all_pets');
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}

function Sell_spezific_pet(item) {
    // This function is now handled by the click event on the pet card
    messageEl.textContent = 'Click on the pet you want to sell.';
}

document.getElementById('save-btn').addEventListener('click', () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('save');
    }
});

function connectWebSocket(username, pin) {
    ws = new WebSocket(`ws://${window.location.host}?username=${encodeURIComponent(username)}&pin=${encodeURIComponent(pin)}`);

    ws.onopen = () => {
        console.log('Connected to the server.');
        messageEl.textContent = 'Connected! Loading game state...';
        
        stateRequestTimeout = setTimeout(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                console.log('Requesting initial game state...');
                ws.send('get_state');
            }
        }, 100);
    };

    ws.onmessage = (event) => {
        const gameState = JSON.parse(event.data);
        updateUI(gameState);
    };

    ws.onclose = (event) => {
        console.log('Disconnected from the server.', event.reason);
        messageEl.textContent = `Connection lost: ${event.reason || 'Please refresh'}`;
        
        if (stateRequestTimeout) {
            clearTimeout(stateRequestTimeout);
            stateRequestTimeout = null;
        }
        
        // If connection is closed (e.g. invalid credentials), redirect to login
        if (!event.wasClean) {
            window.location.href = '/login.html';
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        messageEl.textContent = 'A connection error occurred.';
    };
}

function updateUI(state) {
    if (state.money !== undefined) moneyEl.textContent = state.money;
    if (state.stage !== undefined) stageEl.textContent = state.stage;
    
    if (state.message) {
        messageEl.textContent = state.message;
        if (state.message !== 'Choose a buff.' && !state.message.includes('Welcome')) {
            setTimeout(() => {
                if (messageEl.textContent === state.message) {
                    messageEl.textContent = '';
                }
            }, 4000);
        }
    }

   if (state.inventory) {
    inventoryEl.innerHTML = '';
    state.inventory.forEach(pet => {
        const petCard = document.createElement('div');
        petCard.className = 'pet-card';
        petCard.classList.add(`rarity-${pet.rarity === 1 ? 'common' : pet.rarity === 2 ? 'rare' : 'legendary'}`);
        petCard.style.cursor = 'cursor';
        petCard.innerHTML = `
            <div class="name">${pet.name} (Lv. ${pet.level})</div>
            <div>ATK: ${pet.attack} | HP: ${pet.hp}</div>
            <div>Dodge: ${pet.dodge_chance}%</div>
            <div>Rarity: ${pet.rarity}</div>
        `;
        petCard.addEventListener('click', () => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(`spezific_pet_sell ${pet.name}`);
                } else {
                    messageEl.textContent = 'Connection lost. Please refresh the page.';
                    console.error('WebSocket is not connected');
    }
        });
        inventoryEl.appendChild(petCard);
    });
    }

    if (state.shop) {
        shopUpEl.textContent = state.shop.upgrade_pack;
        shopBpEl.textContent = state.shop.buff_pack;
        shopCpEl.textContent = state.shop.charakter_pack;
        shopLupEl.textContent = state.shop.legendary_upgrade_pack;
        rerollPriceEl.textContent = state.shop.shop_refresh_price;
    }

    if (state.pending_buff_choices && state.pending_buff_choices.length > 0) {
        buffChoicesEl.innerHTML = '';
        state.pending_buff_choices.forEach((buffId, index) => {
            const choiceDiv = document.createElement('div');
            choiceDiv.className = 'buff-choice';
            choiceDiv.textContent = BUFF_DESCRIPTIONS[buffId] || `Unknown Buff ${buffId}`;
            choiceDiv.onclick = () => selectBuff(index);
            buffChoicesEl.appendChild(choiceDiv);
        });
        buffSelectionModal.style.display = 'flex';
    } else {
        buffSelectionModal.style.display = 'none';
    }
}

function buy(item) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(`shop_buy ${item}`);
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}

function rerollShop() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('shop_reroll');
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}

function selectBuff(index) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(`select_buff ${index}`);
        buffSelectionModal.style.display = 'none';
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}           <div>Dodge: ${pet.dodge_chance}%</div>
            <div>Rarity: ${pet.rarity}</div>
        `;
        petCard.addEventListener('click', () => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(`spezific_pet_sell ${pet.name}`);
                } else {
                    messageEl.textContent = 'Connection lost. Please refresh the page.';
                    console.error('WebSocket is not connected');
    }
        });
        inventoryEl.appendChild(petCard);
    });
    }

    if (state.shop) {
        shopUpEl.textContent = state.shop.upgrade_pack;
        shopBpEl.textContent = state.shop.buff_pack;
        shopCpEl.textContent = state.shop.charakter_pack;
        shopLupEl.textContent = state.shop.legendary_upgrade_pack;
        rerollPriceEl.textContent = state.shop.shop_refresh_price;
    }

    if (state.pending_buff_choices && state.pending_buff_choices.length > 0) {
        buffChoicesEl.innerHTML = '';
        state.pending_buff_choices.forEach((buffId, index) => {
            const choiceDiv = document.createElement('div');
            choiceDiv.className = 'buff-choice';
            choiceDiv.textContent = BUFF_DESCRIPTIONS[buffId] || `Unknown Buff ${buffId}`;
            choiceDiv.onclick = () => selectBuff(index);
            buffChoicesEl.appendChild(choiceDiv);
        });
        buffSelectionModal.style.display = 'flex';
    } else {
        buffSelectionModal.style.display = 'none';
    }
}

function buy(item) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(`shop_buy ${item}`);
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}

function rerollShop() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('shop_reroll');
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}

function selectBuff(index) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(`select_buff ${index}`);
        buffSelectionModal.style.display = 'none';
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}