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

window.addEventListener('DOMContentLoaded', async () => {
    const savedUsername = getCookie('username');
    const savedPin = getCookie('pin');
    
    if (savedUsername && savedPin) {
        // Validate credentials before redirecting
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: savedUsername, pin: savedPin })
            });

            if (response.ok) {
                window.location.href = '/game';
                return;
            } else {
                // Invalid cookies, clear them
                deleteCookie('username');
                deleteCookie('pin');
            }
        } catch (error) {
            console.error('Auto-login failed:', error);
            deleteCookie('username');
            deleteCookie('pin');
        }
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
    const username = loginUsernameEl.value.trim();
    const pin = loginPinEl.value.trim();

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

        const result = await response.json();
        console.log('Login response:', result);

        if (response.ok) {
            console.log('Login successful, setting cookies...');
            
            setCookie('username', username, 7);
            setCookie('pin', pin, 7);
            
            const verifyUsername = getCookie('username');
            const verifyPin = getCookie('pin');
            console.log('Cookies set:', { verifyUsername, verifyPin });
            
            // Small delay for cookie writting
            setTimeout(() => {
                window.location.href = '/game';
            }, 100);
        } else {
            alert(`Login failed: ${result.message}`);
        }
    } catch (error) {
        alert('An error occurred during login. Please try again.');
        console.error('Login error:', error);
    }
});



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