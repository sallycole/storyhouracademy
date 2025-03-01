const letters = ['b', 'ch', 'd', 'f', 'h', 'j', 'k\nck', 'l', 'm', 'n', 'ng', 'p', 'qu', 'r', 'sh', 't', 'th', 'v', 'w\nwh', 'z'];
const allSounds = ['b', 'ch', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'ng', 'p', 'qu', 'r', 'sh', 't', 'th', 'v', 'w', 'z'];
let remainingSounds = [];
let currentSound = '';
let results = [];

// Create a mapping of sounds to their S3 URLs
const soundUrls = {
    'b': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/b.mp3',
    'ch': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/ch.mp3',
    'd': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/d.mp3',
    'f': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/f.mp3',
    'h': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/h.mp3',
    'j': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/j.mp3',
    'k': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/k.mp3',
    'l': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/l.mp3',
    'm': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/m.mp3',
    'n': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/n.mp3',
    'ng': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/ng.mp3',
    'p': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/p.mp3',
    'qu': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/qu.mp3',
    'r': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/r.mp3',
    'sh': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/sh.mp3',
    't': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/t.mp3',
    'th': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/th.mp3',
    'v': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/v.mp3',
    'w': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/w.mp3',
    'z': 'https://storyhouracademy.s3.us-east-1.amazonaws.com/z.mp3'
};

function createLetterGrid() {
    const grid = document.getElementById('letterGrid');
    
    // Add CSS to ensure all tiles are the same size and properly spaced
    const style = document.createElement('style');
    style.textContent = `
        .letter-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            justify-content: center;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .letter-tile {
            width: 80px;
            height: 80px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            font-weight: normal;
            margin: 0 auto;
            background-color: #f0f0f0;
            border: 2px solid #ccc;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
        }
        
        .letter-tile:hover {
            background-color: #e0e0e0;
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .letter-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
            text-align: center;
        }
        
        .letter-content div {
            font-size: 24px;
            font-weight: normal;
            line-height: 1.2;
        }
        
        @media (max-width: 768px) {
            .letter-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        
        @media (max-width: 576px) {
            .letter-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
    `;
    document.head.appendChild(style);
    
    letters.forEach(letter => {
        const tile = document.createElement('div');
        tile.className = 'letter-tile';
        
        // Special handling for the k/ck tile and w/wh tile
        if (letter === 'k\nck' || letter === 'w\nwh') {
            // Create a container for the two letters
            const letterContent = document.createElement('div');
            letterContent.className = 'letter-content';
            
            // Add the first letter (k or w)
            const firstElement = document.createElement('div');
            firstElement.textContent = letter.split('\n')[0];
            
            // Add the second letter (ck or wh)
            const secondElement = document.createElement('div');
            secondElement.textContent = letter.split('\n')[1];
            
            // Add both to the container
            letterContent.appendChild(firstElement);
            letterContent.appendChild(secondElement);
            tile.appendChild(letterContent);
        } else {
            tile.textContent = letter;
        }
        
        // For the special tiles, we want to check against the first sound
        let soundToCheck;
        if (letter === 'k\nck') {
            soundToCheck = 'k';
        } else if (letter === 'w\nwh') {
            soundToCheck = 'w';
        } else {
            soundToCheck = letter.toLowerCase();
        }
        
        tile.addEventListener('click', () => checkAnswer(soundToCheck));
        grid.appendChild(tile);
    });
}

function initializeQuiz() {
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

    setTimeout(playNextSound, 1000);
}

function showStartScreen() {
    const container = document.querySelector('.container');
    container.innerHTML = `
        <h1>Mastery Test of Single-Sound Consonants and Consonant Digraphs</h1>
        <p class="instructions">Listen to the sound and click the letter or phonogram that represents the sound.</p>
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
        <h1>Mastery Test of Single-Sound Consonants and Consonant Digraphs</h1>
        <p class="instructions">Listen to the sound and click the letter or phonogram that represents the sound.</p>
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
    
    // Map sounds to their IPA representations
    const soundToIPA = {
        'b': '/b/',
        'ch': '/tʃ/ - /k/ - /ʃ/',
        'd': '/d/',
        'f': '/f/',
        'h': '/h/',
        'j': '/dʒ/',
        'k': '/k/',
        'l': '/l/',
        'm': '/m/',
        'n': '/n/',
        'ng': '/ŋ/',
        'p': '/p/',
        'qu': '/kw/',
        'r': '/ɹ/',
        'sh': '/ʃ/',
        't': '/t/',
        'th': '/θ/ and /ð/',
        'v': '/v/',
        'w': '/w/',
        'z': '/z/'
    };
    
    results.forEach(result => {
        let displaySound = soundToIPA[result.sound] || `/${result.sound}/`;
        
        let displaySelected;
        if (result.selected === 'qu') {
            displaySelected = 'qu';
        } else if (result.selected === 'k') {
            displaySelected = 'k/ck';
        } else if (result.selected === 'w') {
            displaySelected = 'w/wh';
        } else if (['ch', 'sh', 'ng', 'th'].includes(result.selected)) {
            displaySelected = result.selected;
        } else {
            displaySelected = result.selected;
        }
        
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
    
    document.getElementById('tryAgain').addEventListener('click', startQuiz);
}

document.addEventListener('DOMContentLoaded', showStartScreen); 