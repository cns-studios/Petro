const http = require('http');
const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const cookieParser = require('cookie-parser');

const express = require('express');
const app = express();
const server = http.createServer(app);

const wss = new WebSocket.Server({ server });

const gameInstances = new Map();

app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    let sessionId = req.cookies.sessionId;
    if (!sessionId || !gameInstances.has(sessionId)) {
        sessionId = uuidv4();
        res.cookie('sessionId', sessionId, { maxAge: 900000, httpOnly: true });
    }
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.use((req, res, next) => {
  res.status(404).send("Sorry, can't find that!");
});

wss.on('connection', (ws, req) => {
    console.log(`[Server] New WebSocket connection.`);
    const cookieHeader = req.headers.cookie;
    if (!cookieHeader) { 
        console.log('[Server] No cookie header, closing connection.');
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
        console.log('[Server] No session ID in cookie, closing connection.');
        ws.close(); 
        return; 
    }
    console.log(`[Server] Connection associated with Session ID: ${sessionId}`);

    let gameProcess = gameInstances.get(sessionId);

    if (!gameProcess || gameProcess.killed) {
        console.log(`[Game] No existing game process for ${sessionId}. Spawning a new one.`);
        gameProcess = spawn('python', ['-u', 'game.py']);
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
            if (ws.readyState === WebSocket.OPEN) {
                ws.close();
            }
        });
    } else {
        console.log(`[Game] Re-using existing game process for ${sessionId} with PID: ${gameProcess.pid}`);
    }

    gameProcess.stdout.on('data', (data) => {
        const output = data.toString();
        console.log(`[Game -> Server] (SID: ${sessionId}): ${output.trim()}`);
        output.split('\n').filter(line => line.trim() !== '').forEach(line => {
            try {
                const gameState = JSON.parse(line);
                if (ws.readyState === WebSocket.OPEN) {
                    console.log(`[Server -> Client] (SID: ${sessionId}) Sending game state.`);
                    ws.send(JSON.stringify(gameState));
                }
            } catch (e) {
                console.error('[Server] Error parsing game state JSON:', e, 'Received:', line);
            }
        });
    });

    ws.on('message', (message) => {
        const command = message.toString();
        console.log(`[Client -> Server] (SID: ${sessionId}) Received command: ${command}`);
        if (gameProcess && !gameProcess.killed) {
            gameProcess.stdin.write(command + '\n');
        } else {
            console.error(`[Server] No game process found for ${sessionId} to send command to.`);
        }
    });

    ws.on('close', () => {
        console.log(`[Server] WebSocket closed for ${sessionId}. The game process will be kept alive for reconnection.`);
    })
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}. Access via http://localhost:${PORT}`);
});
