let ws;
let stateRequestTimeout = null;

//Cookie Handler
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


// Check authentication on page load
window.addEventListener('DOMContentLoaded', () => {
    const username = getCookie('username');
    const pin = getCookie('pin');

    if (!username || !pin) {
        window.location.href = '/login';
    } else {
        connectWebSocket(username, pin);
    }
});

function connectWebSocket(username, pin) {
    console.log('Attempting to connect with:', { username, pin }); // DEBUG
    
    ws = new WebSocket(`ws://${window.location.host}?username=${encodeURIComponent(username)}&pin=${encodeURIComponent(pin)}`);

    ws.onopen = () => {
        console.log('Connected to the server.');        
        stateRequestTimeout = setTimeout(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                console.log('Requesting matchmaking queue...');

            }
        }, 100);
    };

    ws.onmessage = (event) => {
        const gameState = JSON.parse(event.data);
        updateUI(gameState);
    };

    ws.onclose = (event) => {
        console.log('Disconnected from the server.', event.reason);
        console.log('Event code:', event.code, 'Was clean:', event.wasClean); // DEBUG
        
        if (stateRequestTimeout) {
            clearTimeout(stateRequestTimeout);
            stateRequestTimeout = null;
        }
        
        if (!event.wasClean || event.code === 1008) {
            setTimeout(() => {
                deleteCookie('username');
                deleteCookie('pin');
                window.location.href = '/login';
            }, 2000);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};

function updateUI(state) {

};