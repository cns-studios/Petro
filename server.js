//Dependencies
const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const { spawn } = require('child_process');
const webSocket = require('ws');
const crypto = require('crypto');
const cookieParser = require('cookie-parser');
const db = require('./src/db');

//Config
dotenv.config();
db.initializeDatabase();

//Init
const app = express();
const port = process.env.PORT || 3000;
const clients = new Map();

//Middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(cookieParser());


// User Registration
app.post('/api/register', (req, res) => {
    let pin;
    let userExists = true;
    while (userExists) {
        pin = Math.floor(100000 + Math.random() * 900000).toString();
        userExists = db.findUserByPin(pin);
    }
    db.createUser(pin);
    res.status(201).json({ pin });
});

// User Login
app.post('/api/login', (req, res) => {
    const { pin } = req.body;
    const user = db.findUserByPin(pin);
    if (!user) {
        return res.status(401).json({ error: 'Invalid PIN' });
    }
    const sessionToken = crypto.randomUUID();
    res.cookie('session_token', sessionToken, { httpOnly: true, maxAge: 3600000 });
    app.set(sessionToken, user.id);
    res.status(200).json({ message: 'Login successful' });
});

// API for Python to send updates to the client
app.post('/api/game/update', (req, res) => {
    const { userId, action, data } = req.body;
    const client = clients.get(userId);

    if (client && client.ws.readyState === webSocket.OPEN) {
        client.ws.send(JSON.stringify({ action, data }));
        res.status(200).json({ status: 'success' });
    } else {
        console.error(`Could not send update to user ${userId}. Client not found or connection closed.`);
        res.status(404).json({ error: 'Client not found or connection closed' });
    }
});

// Save Game State (can be removed WITH SOME CHANGES, THAT DOESNT EXIST YET!!)
app.post('/api/game/save', (req, res) => {
    const { userId, money, stage, inventory } = req.body;
    if (!userId || money === undefined || stage === undefined || !inventory) {
        return res.status(400).json({ error: 'Missing required game state data.' });
    }
    try {
        db.saveGameState(userId, money, stage, inventory);
        res.status(200).json({ status: 'success' });
    } catch (error) {
        console.error('Error saving game state:', error);
        res.status(500).json({ error: 'Failed to save game state.' });
    }
});




//Main Proccess
const server = app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

const wss = new webSocket.Server({ server });

wss.on('connection', (ws, req) => {
    const cookieHeader = req.headers.cookie || '';
    const cookies = cookieHeader.split(';').reduce((acc, cookie) => {
        const [key, value] = cookie.trim().split('=');
        if (key) acc[key] = value;
        return acc;
    }, {});

    const sessionToken = cookies.session_token;
    const userId = sessionToken ? app.get(sessionToken) : null;

    if (!userId) {
        ws.close(1008, 'Unauthorized');
        return;
    }

    console.log(`User ${userId} connected via WebSocket.`);
    let gameState = db.getGameState(userId);
    if (!gameState) {
        console.log(`No game state found for user ${userId}. Creating a new one.`);
        db.createInitialGameState(userId);
        gameState = db.getGameState(userId);
        if (!gameState) {
            ws.close(1011, 'Internal Error: Could not create game state.');
            return;
        }
    }

    const pythonExecutable = process.platform === 'win32'
        ? path.join(__dirname, '.venv', 'Scripts', 'python.exe')
        : path.join(__dirname, '.venv', 'bin', 'python');

    const pythonProcess = spawn(pythonExecutable, [
        './game.py',
        userId,
        gameState.money,
        gameState.stage,
        gameState.inventory
    ]);

    clients.set(userId, { ws, pythonProcess });

    pythonProcess.stdout.on('data', (data) => {
        console.log(`[User ${userId}] Python Raw: ${data.toString()}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`[User ${userId}] Python Error: ${data.toString()}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`[User ${userId}] Python process exited with code ${code}`);
        if (clients.has(userId)) {
            clients.get(userId).ws.close();
            clients.delete(userId);
        }
    });

    ws.on('message', (message) => {
        const messageString = message.toString();
        console.log(`Received command from user ${userId}: ${messageString}`);
        pythonProcess.stdin.write(messageString + '\n');
    });

    ws.on('close', () => {
        console.log(`User ${userId} disconnected, killing python process...`);
        if (clients.has(userId)) {
            clients.get(userId).pythonProcess.kill();
            clients.delete(userId);
        }
    });
});