const authContainer = document.getElementById('auth-container');
const gameContainer = document.getElementById('game-container');

const loginView = document.getElementById('login-view');
const signupView = document.getElementById('signup-view');

const showSignupBtn = document.getElementById('show-signup');
const showLoginBtn = document.getElementById('show-login');

const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');

const loginUsernameEl = document.getElementById('login-username');
const loginPinEl = document.getElementById('login-pin');

const signupUsernameEl = document.getElementById('signup-username');
const signupResultEl = document.getElementById('signup-result');

const saveBtn = document.getElementById('save-btn');

let ws;
let currentUsername = null;
let currentPin = null;

// --- Cookie Management ---
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

// --- Check for saved credentials on page load ---
window.addEventListener('DOMContentLoaded', async () => {
    const savedUsername = getCookie('username');
    const savedPin = getCookie('pin');
    
    if (savedUsername && savedPin) {
        // Try to auto-login with saved credentials
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: savedUsername, pin: savedPin })
            });

            if (response.ok) {
                console.log('Auto-login successful');
                currentUsername = savedUsername;
                currentPin = savedPin;
                authContainer.style.display = 'none';
                gameContainer.style.display = 'block';
                connectWebSocket(savedUsername, savedPin);
            } else {
                // Invalid saved credentials, clear them
                deleteCookie('username');
                deleteCookie('pin');
                console.log('Auto-login failed, invalid saved credentials');
            }
        } catch (error) {
            console.error('Auto-login error:', error);
            deleteCookie('username');
            deleteCookie('pin');
        }
    }
});

// --- Add logout button handler ---
function logout() {
    deleteCookie('username');
    deleteCookie('pin');
    currentUsername = null;
    currentPin = null;
    if (ws) {
        ws.close();
    }
    gameContainer.style.display = 'none';
    authContainer.style.display = 'block';
    loginUsernameEl.value = '';
    loginPinEl.value = '';
}

// --- Auth UI Logic ---
showSignupBtn.addEventListener('click', (e) => {
    e.preventDefault();
    loginView.style.display = 'none';
    signupView.style.display = 'block';
});

showLoginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    signupView.style.display = 'none';
    loginView.style.display = 'block';
});

signupBtn.addEventListener('click', async () => {
    const username = signupUsernameEl.value;
    if (!username) {
        alert('Please enter a username.');
        return;
    }

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username })
        });

        const result = await response.json();
        signupResultEl.style.display = 'block';

        if (response.ok) {
            signupResultEl.innerHTML = `Signup successful! Your PIN is: <strong>${result.pin}</strong>. Please save it and log in.`;
            signupResultEl.style.color = 'green';
        } else {
            signupResultEl.textContent = result.message;
            signupResultEl.style.color = 'red';
        }
    } catch (error) {
        signupResultEl.style.display = 'block';
        signupResultEl.textContent = 'An error occurred. Please try again.';
        signupResultEl.style.color = 'red';
        console.error('Signup error:', error);
    }
});

loginBtn.addEventListener('click', async () => {
    const username = loginUsernameEl.value;
    const pin = loginPinEl.value;

    if (!username || !pin) {
        alert('Please enter both username and PIN.');
        return;
    }

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, pin })
        });

        if (response.ok) {
            console.log('Login successful');
            currentUsername = username;
            currentPin = pin;
            
            // Save credentials in cookies (expires in 7 days)
            setCookie('username', username, 7);
            setCookie('pin', pin, 7);
            
            authContainer.style.display = 'none';
            gameContainer.style.display = 'block';
            connectWebSocket(username, pin);
        } else {
            const result = await response.json();
            alert(`Login failed: ${result.message}`);
        }
    } catch (error) {
        alert('An error occurred during login. Please try again.');
        console.error('Login error:', error);
    }
});

saveBtn.addEventListener('click', () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('save');
    }
});

// --- Game and WebSocket Logic ---

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

function connectWebSocket(username, pin) {
    ws = new WebSocket(`ws://${window.location.host}?username=${encodeURIComponent(username)}&pin=${encodeURIComponent(pin)}`);

    ws.onopen = () => {
        console.log('Connected to the server.');
        messageEl.textContent = 'Connected! Loading game state...';
        
        // Request initial state after a short delay to ensure game process is ready
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
        
        // Clear any pending state request
        if (stateRequestTimeout) {
            clearTimeout(stateRequestTimeout);
            stateRequestTimeout = null;
        }
        
        // Don't automatically show auth container if we have saved credentials
        // This allows for reconnection attempts
        if (!getCookie('username') || !getCookie('pin')) {
            gameContainer.style.display = 'none';
            authContainer.style.display = 'block';
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
        // Clear the message after a few seconds if it's a status update
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
            petCard.innerHTML = `
                <div class="name">${pet.name} (Lv. ${pet.level})</div>
                <div>ATK: ${pet.attack} | HP: ${pet.hp}</div>
                <div>Dodge: ${pet.dodge_chance}%</div>
                <div>Rarity: ${pet.rarity}</div>
            `;
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