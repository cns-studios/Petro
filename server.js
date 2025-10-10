const http = require('http');
const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const url = require('url');

const connectionAttempts = new Map();
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const db = new sqlite3.Database(path.join(__dirname, 'db', 'users.db'), (err) => {
    if (err) {
        console.error('Error opening database', err.message);
    } else {
        console.log('Connected to the SQLite database.');
        db.run(`CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            pin TEXT NOT NULL,
            game_state TEXT
        )`);
    }
});

const gameInstances = new Map();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

function createGameProcess(username) {
    if (connectionAttempts.has(username)) {
        console.log(`[Game] Process creation already in progress for ${username}`);
        return connectionAttempts.get(username);
    }

    console.log(`[Game] Spawning new game process for user: ${username}`);
    
    const pythonCmd = process.platform === 'win32' ? 'py' : 'python3';
    const gameProcess = spawn(pythonCmd, ['-u', path.join(__dirname, 'source', 'logic.py'), username]);
    
    connectionAttempts.set(username, gameProcess);
    gameInstances.set(username, gameProcess);

    gameProcess.on('spawn', () => {
        console.log(`[Game] Successfully spawned process for ${username} with PID: ${gameProcess.pid}`);
        connectionAttempts.delete(username);
    });

    gameProcess.stderr.on('data', (data) => {
        console.error(`[Game ERROR] (User: ${username}): ${data.toString()}`);
    });

    gameProcess.on('close', (code) => {
        console.log(`[Game] Process for ${username} exited with code ${code}`);
        gameInstances.delete(username);
        connectionAttempts.delete(username);
    });

    gameProcess.on('error', (err) => {
        console.error(`[Game] Failed to start process for ${username}:`, err);
        gameInstances.delete(username);
        connectionAttempts.delete(username);
    });

    return gameProcess;
}

app.post('/signup', (req, res) => {
    const { username } = req.body;
    if (!username) {
        return res.status(400).json({ message: 'Username is required.' });
    }

    const pin = Math.floor(1000 + Math.random() * 9000).toString();

    db.run('INSERT INTO users (username, pin) VALUES (?, ?)', [username, pin], function(err) {
        if (err) {
            console.error('Signup error:', err.message);
            return res.status(409).json({ message: 'Username already taken.' });
        }
        console.log(`[Server] New user created: ${username}`);
        res.status(201).json({ username, pin });
    });
});

app.post('/login', (req, res) => {
    const { username, pin } = req.body;
    if (!username || !pin) {
        return res.status(400).json({ message: 'Username and PIN are required.' });
    }

    db.get('SELECT * FROM users WHERE username = ? AND pin = ?', [username, pin], (err, row) => {
        if (err) {
            console.error('Login error:', err.message);
            return res.status(500).json({ message: 'Internal server error.' });
        }
        if (row) {
            console.log(`[Server] User logged in: ${username}`);
            res.status(200).json({ message: 'Login successful.' });
        } else {
            res.status(401).json({ message: 'Invalid username or PIN.' });
        }
    });
});

wss.on('connection', (ws, req) => {
    const { query } = url.parse(req.url, true);
    const { username, pin } = query;

    console.log(`[Server] New WebSocket connection attempt for user: ${username}`);

    if (!username || !pin) {
        console.log('[Server] WebSocket connection rejected: Missing credentials.');
        ws.close(1008, 'Missing credentials');
        return;
    }

    db.get('SELECT * FROM users WHERE username = ? AND pin = ?', [username, pin], (err, user) => {
        if (err || !user) {
            console.log(`[Server] WebSocket connection rejected: Invalid credentials for user ${username}.`);
            ws.close(1008, 'Invalid credentials');
            return;
        }

        console.log(`[Server] WebSocket connected for user: ${username}`);

        let gameProcess = gameInstances.get(username);
        if (!gameProcess || gameProcess.killed) {
            console.log(`[Server] No live game process for ${username}. Creating new one.`);
            gameProcess = createGameProcess(username);
        }

        const onData = (data) => {
            const output = data.toString();
            output.split('\n').filter(line => line.trim() !== '').forEach(line => {
                if (ws.readyState === WebSocket.OPEN) {
                    console.log(`[Game -> Server] (User: ${username}): ${line.trim()}`);
                    ws.send(line);
                }
            });
        };

        const onProcessClose = (code) => {
            console.log(`[Server] Game process closed unexpectedly for ${username}`);
            if (ws.readyState === WebSocket.OPEN) {
                ws.close(1011, 'Game process terminated');
            }
            cleanup();
        };

        const cleanup = () => {
            gameProcess.stdout.removeListener('data', onData);
            gameProcess.removeListener('close', onProcessClose);
        };

        gameProcess.stdout.on('data', onData);
        gameProcess.once('close', onProcessClose);

        ws.on('message', (message) => {
            const command = message.toString();
            console.log(`[Client -> Server] (User: ${username}) Received command: ${command}`);
            if (!gameProcess.killed) {
                gameProcess.stdin.write(command + '\n');
            }
        });

        ws.on('close', () => {
            console.log(`[Server] WebSocket closed for user: ${username}.`);
            cleanup();
        });

        ws.on('error', (error) => {
            console.error(`[Server] WebSocket error for user ${username}:`, error);
            cleanup();
        });
    });
});

app.use((req, res) => {
    res.status(404).send('File not found');
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}. Access at http://localhost:${PORT}`);
});