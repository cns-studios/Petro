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

const ws = new WebSocket(`ws://${window.location.host}`);

const BUFF_DESCRIPTIONS = {
    1: "+1 Attack for all Pets",
    2: "+1 HP for all Pets",
    3: "+2% Dodge Chance for all Pets",
    13: "+1 Level for all Pets",
};

ws.onopen = () => {
    console.log('Connected to the server.');
};

ws.onmessage = (event) => {
    const gameState = JSON.parse(event.data);
    updateUI(gameState);
};

ws.onclose = () => {
    console.log('Disconnected from the server.');
    messageEl.textContent = 'Connection lost. Please refresh the page.';
};

function updateUI(state) {
    moneyEl.textContent = state.money;
    stageEl.textContent = state.stage;
    
    if (state.message) {
        messageEl.textContent = state.message;
    }

    // Update Inventory
    inventoryEl.innerHTML = '';
    state.inventory.forEach(pet => {
        const petCard = document.createElement('div');
        petCard.className = 'pet-card';
        petCard.innerHTML = `
            <div class="name">${pet.name} (Lv. ${pet.level})</div>
            <div>ATK: ${pet.attack} | HP: ${pet.hp}</div>
            <div>Dodge: ${pet.dodge_chance}%</div>
            <div>Rarity: ${pet.rarity}</div>
        `;
        inventoryEl.appendChild(petCard);
    });

    // Update Shop
    shopUpEl.textContent = state.shop.upgrade_pack;
    shopBpEl.textContent = state.shop.buff_pack;
    shopCpEl.textContent = state.shop.charakter_pack;
    shopLupEl.textContent = state.shop.legendary_upgrade_pack;
    rerollPriceEl.textContent = state.shop.shop_refresh_price;

    // Handle Buff Choices
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
    ws.send(`shop_buy ${item}`);
}

function rerollShop() {
    ws.send('shop_reroll');
}

function selectBuff(index) {
    ws.send(`select_buff ${index}`);
    buffSelectionModal.style.display = 'none';
}
