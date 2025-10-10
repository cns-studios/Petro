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

window.addEventListener('DOMContentLoaded', async () => {
    const savedUsername = getCookie('username');
    const savedPin = getCookie('pin');
    
    if (savedUsername && savedPin) {
        // If cookies are present, try to go to the game page.
        // index.html will validate the cookies.
        window.location.href = '/game.html';
    }
});

showLoginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    signupView.style.display = 'none';
    loginView.style.display = 'block';
});

showSignupBtn.addEventListener('click', (e) => {
    e.preventDefault();
    signupView.style.display = 'block';
    loginView.style.display = 'none';
})

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
            
            setCookie('username', username, 7);
            setCookie('pin', pin, 7);

            window.location.href = '/game.html';
        } else {
            const result = await response.json();
            alert(`Login failed: ${result.message}`);
        }
    } catch (error) {
        alert('An error occurred during login. Please try again.');
        console.error('Login error:', error);
    }
});
