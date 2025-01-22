// Add these constants at the top of game.js
const CARDS_PER_LEVEL = {
    1: 10,  // Level 1: 10 cards (5 pairs)
    2: 20,  // Level 2: 20 cards (10 pairs)
    3: 30   // Level 3: 30 cards (15 pairs)
};

const GRID_COLUMNS = {
    1: 5,   // Level 1: 5 columns (2 rows)
    2: 5,   // Level 2: 5 columns (4 rows)
    3: 6    // Level 3: 6 columns (5 rows)
};

function initGame() {
    const numCards = CARDS_PER_LEVEL[state.level];
    const numPairs = numCards / 2;
    
    // Create pairs of numbers
    tiles = [];
    for (let i = 0; i < numPairs; i++) {
        tiles.push(i);
        tiles.push(i);
    }
    
    // Shuffle tiles
    for (let i = tiles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [tiles[i], tiles[j]] = [tiles[j], tiles[i]];
    }
    
    hide = new Array(numCards).fill(true);
    revealedTiles = [];
    levelCompleted = false;
    state.moves = 0;
    state.startTime = Date.now();
    
    createGameBoard();
    updateDisplay();
}

function createGameBoard() {
    const gameBoard = document.getElementById('game-board');
    gameBoard.innerHTML = '';
    
    // Set the number of cards based on level
    const numCards = state.level * 10;
    
    // Create and add cards
    for (let i = 0; i < numCards; i++) {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.innerHTML = `
            <div class="card-face card-back"></div>
            <div class="card-face card-front">${tiles[i]}</div>
        `;
        card.dataset.index = i;
        card.addEventListener('click', () => handleCardClick(i));
        gameBoard.appendChild(card);
    }
    
    // Set the grid columns based on level
    const columns = state.level === 3 ? 6 : 5;
    gameBoard.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
}

function handleCardClick(index) {
    if (revealedTiles.length === 2 || !hide[index] || levelCompleted) return;
    
    flipCard(index);
    revealedTiles.push(index);
    state.moves++;
    updateDisplay();
    
    if (revealedTiles.length === 2) {
        const [tile1, tile2] = revealedTiles;
        if (tiles[tile1] !== tiles[tile2]) {
            setTimeout(() => {
                hideCards([tile1, tile2]);
                revealedTiles = [];
            }, 500);
        } else {
            revealedTiles = [];
            checkLevelCompletion();
        }
    }
}

function flipCard(index) {
    const card = document.querySelector(`[data-index="${index}"]`);
    card.classList.add('flipped');
    hide[index] = false;
}

function hideCards(indices) {
    indices.forEach(index => {
        const card = document.querySelector(`[data-index="${index}"]`);
        card.classList.remove('flipped');
        hide[index] = true;
    });
}

function markAsMatched(indices) {
    indices.forEach(index => {
        const card = document.querySelector(`[data-index="${index}"]`);
        card.classList.add('matched');
    });
}

function checkLevelCompletion() {
    if (hide.every(h => !h)) {
        levelCompleted = true;
        const elapsedTime = (Date.now() - state.startTime) / 1000;
        state.timePerLevel.push(elapsedTime);
        state.movesPerLevel.push(state.moves);
        
        if (state.level === 3) {
            setTimeout(showWinScreen, 1000);
        } else {
            setTimeout(() => {
                state.level++;
                initGame();
            }, 1000);
        }
    }
}

// Add this function to handle game board resizing
function updateGameBoardSize() {
    const gameBoard = document.getElementById('game-board');
    gameBoard.dataset.level = state.level;
    
    // Adjust container size based on level
    const container = document.querySelector('.game-container');
    container.style.maxWidth = state.level === 3 ? '1200px' : '1000px';
}

// Update initGame to call the new function
const originalInitGame = initGame;
initGame = function() {
    originalInitGame();
    updateGameBoardSize();
}

function updateDisplay() {
    document.getElementById('current-level').textContent = state.level;
    document.getElementById('move-count').textContent = state.moves;
    const elapsedTime = (Date.now() - state.startTime) / 1000;
    document.getElementById('time').textContent = `${elapsedTime.toFixed(2)}s`;
    
    if (!levelCompleted) {
        requestAnimationFrame(updateDisplay);
    }
}

function showWinScreen() {
    const winScreen = document.getElementById('win-screen');
    const results = document.getElementById('results');
    results.innerHTML = '';
    
    for (let i = 0; i < state.timePerLevel.length; i++) {
        results.innerHTML += `
            <p>Level ${i + 1}: Time: ${state.timePerLevel[i].toFixed(2)}s, 
               Moves: ${state.movesPerLevel[i]}</p>
        `;
    }
    
    winScreen.style.display = 'block';
}

function submitScore() {
    const playerName = document.getElementById('player-name').value;
    if (!playerName) return;
    
    const totalTime = state.timePerLevel.reduce((a, b) => a + b, 0);
    const totalMoves = state.movesPerLevel.reduce((a, b) => a + b, 0);
    
    leaderboard.push({
        name: playerName,
        time: totalTime,
        moves: totalMoves
    });
    
    leaderboard.sort((a, b) => a.time - b.time);
    displayLeaderboard();
}

function displayLeaderboard() {
    const winScreen = document.getElementById('win-screen');
    const leaderboardDiv = document.getElementById('leaderboard');
    const entries = document.getElementById('leaderboard-entries');
    
    winScreen.style.display = 'none';
    leaderboardDiv.style.display = 'block';
    
    entries.innerHTML = leaderboard
        .slice(0, 5)
        .map((entry, index) => `
            <div class="leaderboard-entry">
                <span>${index + 1}. ${entry.name}</span>
                <span>Time: ${entry.time.toFixed(2)}s, Moves: ${entry.moves}</span>
            </div>
        `)
        .join('');
}

// Initialize the game when the page loads
window.addEventListener('load', initGame);