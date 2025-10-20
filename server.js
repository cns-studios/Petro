const http = require('http');
const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const url = require('url');
const request = require('request');
const fs = require('fs');

const connectionAttempts = new Map();
const app = express();
const server = http.createServer(app);

// Create ws servers with da noServer option bc stackoverflow told me so (no idea what ts does)
const wss = new WebSocket.Server({ noServer: true });
const wss_battle = new WebSocket.Server({ noServer: true });

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
});if (!fs.existsSync(path.join(__dirname, 'db', 'users.db'))) {
    console.log('No database found, creating a new one.');
    db.serialize(() => {
        db.run(`CREATE TABLE users (
            username TEXT PRIMARY KEY,
            pin TEXT NOT NULL,
            game_state TEXT
        )`);
    });
}

let service_mode = false; //Service mode stopps everyone from connecting for example during updates

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
    const gameProcess = spawn(pythonCmd, ['-u', path.join(__dirname, 'src', 'logic.py'), username]);
    
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

    // Battle ws Server
    const wss_battle = new WebSocket.Server({ noServer: true });

    wss_battle.on('connection', (ws, req, battleId, username) => {
        console.log(`[Battle WS] Player ${username} connected to battle #${battleId}`);

        const battle = activeBattles.get(parseInt(battleId));
        if (!battle) {
            console.log(`[Battle WS] Battle #${battleId} not found`);
            ws.close(1008, 'Battle not found');
            return;
        }

        const battleProcess = battle.process;

        const onData = (data) => {
            const output = data.toString();
            output.split('\n').filter(line => line.trim() !== '').forEach(line => {
                try {
                    const parsed = JSON.parse(line);
                    // Send updates to the specific player or broadcast to both
                    if (ws.readyState === WebSocket.OPEN) {
                        console.log(`[Battle -> Client] Battle #${battleId}: ${line.trim()}`);
                        ws.send(line);
                    }
                } catch (e) {
                    console.error(`[Battle] Failed to parse output: ${line}`);
                }
            });
        };

        const onProcessClose = (code) => {
            console.log(`[Battle WS] Battle #${battleId} process closed`);
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'battle_ended', message: 'Battle ended' }));
                ws.close(1000, 'Battle ended');
            }
            cleanup();
        };

        const cleanup = () => {
            battleProcess.stdout.removeListener('data', onData);
            battleProcess.removeListener('close', onProcessClose);
        };

        battleProcess.stdout.on('data', onData);
        battleProcess.once('close', onProcessClose);

        ws.on('message', (message) => {
            const command = message.toString();
            console.log(`[Battle Client -> Server] ${username} in battle #${battleId}: ${command}`);
            if (!battleProcess.killed) {
                battleProcess.stdin.write(`${username}:${command}\n`);
            }
        });

        ws.on('close', () => {
            console.log(`[Battle WS] ${username} disconnected from battle #${battleId}`);
            cleanup();
        });

        ws.on('error', (error) => {
            console.error(`[Battle WS] Error for ${username} in battle #${battleId}:`, error);
            cleanup();
        });
    });

    
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
            
            if (command === "join_matchmaking") {
                console.log(`[Matchmaking] ${username} joining matchmaking`);
                
                const matchResult = findMatch(username);
                
                if (matchResult.matched) {
                    // Create battle process
                    const battleProcess = createBattleProcess(
                        matchResult.battleId, 
                        username, 
                        matchResult.opponent
                    );
                    
                    ws.send(JSON.stringify({
                        type: 'match_found',
                        battleId: matchResult.battleId,
                        opponent: matchResult.opponent
                    }));
                } else {
                    // Add ws reference to queue
                    const queueEntry = matchmakingQueue.find(p => p.username === username);
                    if (queueEntry) {
                        queueEntry.ws = ws;
                    }
                    
                    ws.send(JSON.stringify({
                        type: 'searching',
                        message: 'Searching for opponent...',
                        queuePosition: matchmakingQueue.length
                    }));
                }
            } else if (command === "leave_matchmaking") {
                const index = matchmakingQueue.findIndex(p => p.username === username);
                if (index !== -1) {
                    matchmakingQueue.splice(index, 1);
                    console.log(`[Matchmaking] ${username} left queue`);
                    ws.send(JSON.stringify({
                        type: 'left_queue',
                        message: 'Left matchmaking queue'
                    }));
                }
            } else if (!gameProcess.killed) {
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

app.get('/', (req, res) => {
    res.redirect(path.join(__dirname, 'public', 'login.html')); 
});

app.post('/update', (req, res) => {
    console.log(req.body);
    res.send('Update request received');
    if (req.body.pass === 'adfs') {
        update_server();
    }
});

app.get('/game', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'game.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
    
});

app.get('/matchmaking', (req, res) => {
    if (service_mode) {
        res.send("Not available during updates");
    } else {
        res.sendFile(path.join(__dirname, 'public', 'matchmaking.html'));
    }
    console.log(`[Server] New Matchmaking attempt`)
});

app.get('/battle', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'battle.html'));
});

app.use((req, res) => {
    res.status(404).send('File not found');
});

// Handle WebSocket upgrade - route to appropriate handler
server.on('upgrade', (request, socket, head) => {
    const pathname = url.parse(request.url).pathname;
    const { query } = url.parse(request.url, true);
    
    console.log(`[WebSocket] Upgrade request for path: ${pathname}`);
    
    if (pathname === '/battle') {
        // Battle ws
        const { battleId, username, pin } = query;
        
        console.log(`[Battle WS] Upgrade attempt for battle #${battleId} by ${username}`);
        
        if (!battleId || !username || !pin) {
            console.log('[Battle WS] Missing parameters, destroying socket');
            socket.destroy();
            return;
        }
        
        db.get('SELECT * FROM users WHERE username = ? AND pin = ?', [username, pin], (err, user) => {
            if (err || !user) {
                console.log(`[Battle WS] Invalid credentials for ${username}`);
                socket.destroy();
                return;
            }
            
            wss_battle.handleUpgrade(request, socket, head, (ws) => {
                wss_battle.emit('connection', ws, request, battleId, username);
            });
        });
    } else {
        // normal ws for every else shitty json communication (json shit was implemented by me, still ass af)
        const { username, pin } = query;
        
        if (!username || !pin) {
            console.log('[WebSocket] Missing credentials, destroying socket');
            socket.destroy();
            return;
        }
        
        wss.handleUpgrade(request, socket, head, (ws) => {
            wss.emit('connection', ws, request);
        });
    }
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}. Access at http://localhost:${PORT}`);
});


// Matchmaking and the queue shit
const matchmakingQueue = [];
const activeBattles = new Map(); // FORMAType shii: battleId -> {player1, player2, process}
let battleIdCounter = 0;

function findMatch(username) {
    // Remove player from queue if already there  --> GETOUTTTTT
    const existingIndex = matchmakingQueue.findIndex(p => p.username === username);
    if (existingIndex !== -1) {
        matchmakingQueue.splice(existingIndex, 1);
    }
    
    if (matchmakingQueue.length > 0) {
        // Match found:
        const opponent = matchmakingQueue.shift();
        const battleId = ++battleIdCounter;
        
        console.log(`[Matchmaking] Match found! ${username} vs ${opponent.username} (Battle #${battleId})`);
        
        // Notify players
        if (opponent.ws && opponent.ws.readyState === WebSocket.OPEN) {
            opponent.ws.send(JSON.stringify({
                type: 'match_found',
                battleId: battleId,
                opponent: username
            }));
        }
        
        return { matched: true, opponent: opponent.username, battleId };
    } else {
        // Add to da damnnn queue
        matchmakingQueue.push({ username });
        console.log(`[Matchmaking] ${username} added to queue. Queue size: ${matchmakingQueue.length}`);
        return { matched: false };
    }
}

function update_server() {
    service_mode = true;
    console.log('Updating server...');
    console.log("Waiting for all battles to finish(" + battleIdCounter + ")");
    var update_interval = setInterval(() => {
        if (battleIdCounter === 0) {
            console.log("Proceeding to update");
            request.post(
                'http://localhost:8888/update',
                { json: { pass: 'adfs' } },
                function (error, response, body) {
                    if (!error && response.statusCode == 200) {
                        console.log(body);
                    }
                }
            );
            clearInterval(update_interval);
        }
    }, 1000);
}


function createBattleProcess(battleId, player1, player2) {
    if (activeBattles.has(battleId)) {
        console.log(`[Battle] Battle #${battleId} already exists`);
        return activeBattles.get(battleId).process;
    }

    console.log(`[Battle] Creating battle #${battleId}: ${player1} vs ${player2}`);
    
    const pythonCmd = process.platform === 'win32' ? 'py' : 'python3';
    const battleProcess = spawn(pythonCmd, [
        '-u', 
        path.join(__dirname, 'src', 'ingame.py'),
        battleId.toString(),
        player1,
        player2
    ]);
    
    activeBattles.set(battleId, {
        player1,
        player2,
        process: battleProcess
    });

    battleProcess.on('spawn', () => {
        console.log(`[Battle] Battle #${battleId} process spawned with PID: ${battleProcess.pid}`);
    });

    battleProcess.stderr.on('data', (data) => {
        console.error(`[Battle ERROR] #${battleId}: ${data.toString()}`);
    });

    battleProcess.on('close', (code) => {
        console.log(`[Battle] Battle #${battleId} ended with code ${code}`);
        activeBattles.delete(battleId);
    });

    battleProcess.on('error', (err) => {
        console.error(`[Battle] Failed to start battle #${battleId}:`, err);
        activeBattles.delete(battleId);
    });

    return battleProcess;
}
