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
    const cookieHeader = req.headers.cookie;
    if (!cookieHeader) { ws.close(); return; }
    const cookies = cookieHeader.split(';').reduce((acc, cookie) => {
        const [key, value] = cookie.trim().split('=');
        acc[key] = value;
        return acc;
    }, {});

    const sessionId = cookies.sessionId;
    if (!sessionId) { ws.close(); return; }

    let gameProcess = gameInstances.get(sessionId);

    if (!gameProcess || gameProcess.killed) {
        gameProcess = spawn('python', ['-u', 'game.py']);
        gameInstances.set(sessionId, gameProcess);

        gameProcess.stderr.on('data', (data) => {
            console.error(`Game Error (SID: ${sessionId}): ${data}`);
        });

        gameProcess.on('close', (code) => {
            console.log(`Game process (SID: ${sessionId}) exited with code ${code}`);
            gameInstances.delete(sessionId);
            ws.close();
        });
    }

    gameProcess.stdout.on('data', (data) => {
        const output = data.toString();
        output.split('\n').filter(line => line.trim() !== '').forEach(line => {
            try {
                const gameState = JSON.parse(line);
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify(gameState));
                }
            } catch (e) {
                console.error('Error parsing game state JSON:', e, 'Received:', line);
            }
        });
    });

    ws.on('message', (message) => {
        const command = message.toString();
        if (gameProcess && !gameProcess.killed) {
            gameProcess.stdin.write(command + '\n');
        }
    });

    ws.on('close', () => {
        // The python process is intentionally not killed when the websocket closes
        // so the user can reconnect on page refresh.
        // A timeout could be added here to kill inactive processes.
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}. Access via http://localhost:${PORT}`);
});
