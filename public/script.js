const saveBtn = document.getElementById('save-btn');

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
        // The server will validate the credentials on WebSocket connection
        connectWebSocket(username, pin);
    }
});

function Petsell() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('sell_all_pets');
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }


}
function Sell_spezific_pet(item) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(`spezific_pet_sell ${item}`);
    } else {
        messageEl.textContent = 'Connection lost. Please refresh the page.';
        console.error('WebSocket is not connected');
    }
}


saveBtn.addEventListener('click', () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send('save');
    }
});


function  WebSocket(username, pin) {
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