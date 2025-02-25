const letters = ['b', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'qu', 'r', 's', 't', 'v', 'w', 'z'];
const allSounds = ['b', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'qu', 'r', 't', 'v', 'w', 'z'];
let remainingSounds = [];
let currentSound = '';
let results = [];

// Create a mapping of sounds to their S3 URLs
const soundUrls = {
    'b': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/b.mp3',
    'd': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/d.mp3',
    'f': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/f.mp3',
    'h': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/h.mp3',
    'j': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/j.mp3',
    'k': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/k.mp3',
    'l': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/l.mp3',
    'm': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/m.mp3',
    'n': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/n.mp3',
    'p': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/p.mp3',
    'qu': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/qu.mp3',
    'r': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/r.mp3',
    't': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/t.mp3',
    'v': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/v.mp3',
    'w': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/w.mp3',
    'z': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/z.mp3'
};

function createLetterGrid() {
    const grid = document.getElementById('letterGrid');
    letters.forEach(letter => {
        const tile = document.createElement('div');
        tile.className = 'letter-tile';
        tile.textContent = letter;
        tile.addEventListener('click', () => checkAnswer(letter));
        grid.appendChild(tile);
    });
}

function initializeQuiz() {
    // Reset and shuffle the sounds
    remainingSounds = [...allSounds];
    shuffleArray(remainingSounds);
    results = [];
    document.getElementById('score').textContent = `Progress: 0/${allSounds.length}`;
    playNextSound();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function playNextSound() {
    if (remainingSounds.length === 0) {
        showFinalResults();
        return;
    }
    
    currentSound = remainingSounds[0];
    playCurrentSound();
    document.getElementById('feedback').textContent = '';
}

function playCurrentSound() {
    const audioUrl = soundUrls[currentSound];
    const audio = new Audio(audioUrl);
    audio.play().catch(error => {
        console.error('Error playing sound:', error);
        document.getElementById('feedback').textContent = 'Error playing sound. Please try again.';
    });
}

function checkAnswer(selectedLetter) {
    if (!currentSound || remainingSounds.length === 0) return;

    const correct = selectedLetter === currentSound;
    const feedback = document.getElementById('feedback');
    
    results.push({
        sound: currentSound,
        selected: selectedLetter,
        correct: correct
    });

    feedback.textContent = correct ? 'Correct!' : 'Incorrect';
    feedback.style.color = correct ? 'green' : 'red';
    
    remainingSounds.shift();
    document.getElementById('score').textContent = 
        `Progress: ${results.length}/${allSounds.length}`;

    // Wait a moment before moving to next sound
    setTimeout(playNextSound, 1000);
}

function showStartScreen() {
    const container = document.querySelector('.container');
    container.innerHTML = `
        <h1>Mastery Test of Single-Sound Consonants</h1>
        <p class="instructions">Listen to the sound and click the letter that represents the sound.</p>
        <div class="quiz-controls">
            <button id="startQuiz" class="play-button">
                Start Quiz
            </button>
        </div>
    `;
    
    document.getElementById('startQuiz').addEventListener('click', startQuiz);
}

function startQuiz() {
    const container = document.querySelector('.container');
    container.innerHTML = `
        <h1>Mastery Test of Single-Sound Consonants</h1>
        <p class="instructions">Listen to the sound and click the letter that represents the sound.</p>
        <div class="quiz-controls">
            <button id="playSound" class="play-button">
                Replay Sound
            </button>
            <p id="feedback" class="feedback"></p>
            <p id="score" class="score">Progress: 0/${allSounds.length}</p>
        </div>
        <div id="letterGrid" class="letter-grid">
        </div>
    `;

    createLetterGrid();
    initializeQuiz();
    
    document.getElementById('playSound').addEventListener('click', () => {
        if (currentSound) {
            playCurrentSound();
        }
    });
}

function showFinalResults() {
    const container = document.querySelector('.container');
    const correct = results.filter(r => r.correct).length;
    
    let resultsHTML = `
        <h2>Quiz Complete!</h2>
        <p>Final Score: ${correct}/${allSounds.length}</p>
        <h3>Results:</h3>
        <ul style="list-style: none; padding: 0;">
    `;
    
    results.forEach(result => {
        const displaySound = result.sound === 'qu' ? '/kw/' : `/${result.sound}/`;
        const displaySelected = result.selected;
        
        resultsHTML += `
            <li style="margin: 10px 0; color: ${result.correct ? 'green' : 'red'}">
                Sound: "${displaySound}" - You selected: "${displaySelected}" 
                ${result.correct ? '✓' : '✗'}
            </li>
        `;
    });
    
    resultsHTML += `
        </ul>
        <button id="tryAgain" class="play-button">Try Again</button>
    `;
    
    container.innerHTML = resultsHTML;
    
    // Add event listener to the new try again button
    document.getElementById('tryAgain').addEventListener('click', startQuiz);
}

// Remove the old initialization code and replace with:
document.addEventListener('DOMContentLoaded', showStartScreen); 