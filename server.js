const http = require('http');
const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');
const express = require('express');
const cookieParser = require('cookie-parser');
const { v4: uuidv4 } = require('uuid');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const gameInstances = new Map();

app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

function createGameProcess(sessionId) {
    console.log(`[Game] Spawning new game process for SID: ${sessionId}`);
    const gameProcess = spawn('python', ['-u', 'game.py']);
    gameInstances.set(sessionId, gameProcess);

    gameProcess.on('spawn', () => {
        console.log(`[Game] Successfully spawned process for ${sessionId} with PID: ${gameProcess.pid}`);
    });

    gameProcess.stderr.on('data', (data) => {
        console.error(`[Game ERROR] (SID: ${sessionId}): ${data.toString()}`);
    });

    gameProcess.on('close', (code) => {
        console.log(`[Game] Process for ${sessionId} exited with code ${code}`);
        gameInstances.delete(sessionId);
    });

    return gameProcess;
}

app.get('/', (req, res) => {
    let sessionId = req.cookies.sessionId;

    if (!sessionId) {
        sessionId = uuidv4();
        console.log(`[Server] No session ID found. Creating new one: ${sessionId}`);
        res.cookie('sessionId', sessionId, { maxAge: 900000, httpOnly: true });
        createGameProcess(sessionId);
    } else {
        console.log(`[Server] Found session ID: ${sessionId}`);
        if (!gameInstances.has(sessionId)) {
            console.log(`[Server] No game process found for existing session. Creating new one.`);
            createGameProcess(sessionId);
        }
    }
    
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

wss.on('connection', (ws, req) => {
    console.log(`[Server] New WebSocket connection attempt.`);
    const cookieHeader = req.headers.cookie;
    if (!cookieHeader) {
        console.log('[Server] WebSocket rejected: No cookie header.');
        ws.close();
        return;
    }

    const cookies = cookieHeader.split(';').reduce((acc, cookie) => {
        const [key, value] = cookie.trim().split('=');
        acc[key] = value;
        return acc;
    }, {});
    const sessionId = cookies.sessionId;

    if (!sessionId) {
        console.log('[Server] WebSocket rejected: No session ID in cookie.');
        ws.close();
        return;
    }

    const gameProcess = gameInstances.get(sessionId);

    if (!gameProcess || gameProcess.killed) {
        console.log(`[Server] WebSocket rejected: No live game process for SID: ${sessionId}.`);
        ws.close();
        return;
    }

    console.log(`[Server] WebSocket connected for SID: ${sessionId}`);

    const onData = (data) => {
        const output = data.toString();
        console.log(`[Game -> Server] (SID: ${sessionId}): ${output.trim()}`);
        output.split('\n').filter(line => line.trim() !== '').forEach(line => {
            try {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(line); // Send the raw JSON string
                }
            } catch (e) {
                console.error('[Server] Error sending game state:', e);
            }
        });
    };

    gameProcess.stdout.on('data', onData);

    ws.on('message', (message) => {
        const command = message.toString();
        console.log(`[Client -> Server] (SID: ${sessionId}) Received command: ${command}`);
        gameProcess.stdin.write(command + '\n');
    });

    ws.on('close', () => {
        console.log(`[Server] WebSocket closed for SID: ${sessionId}.`);
        // Remove the listener to prevent memory leaks
        gameProcess.stdout.removeListener('data', onData);
    });
});

app.use((req, res) => {
    res.status(404).send('File not found');
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});