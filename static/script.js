let allQuestions = [];
let currentPlayer = "";
let currentQuestionIndex = 0;
let selectedQuestions = [];
let score = 0;
let attempt = 0;
let totalQuestions = 3;
let scores = JSON.parse(localStorage.getItem("scores") || "[]");

async function startGame() {
  const player = document.getElementById("playerSelect").value;
  if (!player) return alert("Please select a player name.");

  currentPlayer = player;
  score = 0;
  currentQuestionIndex = 0;
  attempt = 0;
  document.querySelector(".start-screen").classList.add("hidden");
  document.getElementById("quizBox").classList.remove("hidden");

  const response = await fetch("questions.json");
  const data = await response.json();
  allQuestions = Object.values(data).flat();
  selectedQuestions = shuffle(allQuestions).slice(0, totalQuestions);

  showQuestion();
}

function showQuestion() {
  const question = selectedQuestions[currentQuestionIndex];
  document.getElementById("questionText").innerText = `Question ${currentQuestionIndex + 1}: ${question.question}`;

  // Add question image
  const imageBox = document.getElementById("questionImage");
  if (question.image) {
    imageBox.innerHTML = `<img src="${question.image}" class="question-image" alt="Play Diagram">`;
  } else {
    imageBox.innerHTML = ""; // fallback
  }

  // Reset options
  const optionsBox = document.getElementById("options");
  const feedback = document.getElementById("feedback");
  optionsBox.innerHTML = "";
  feedback.innerText = "";
  attempt = 0;

  shuffle(question.options).forEach(option => {
    const btn = document.createElement("button");
    btn.innerText = option;
    btn.className = "option-btn";
    btn.onclick = () => checkAnswer(option, question.correct_answer);
    optionsBox.appendChild(btn);
  });
}


function checkAnswer(selected, correct) {
  const feedback = document.getElementById("feedback");
  attempt++;

  if (selected === correct) {
    if (attempt === 1) score += 5;
    else if (attempt === 2) score += 2;
    feedback.innerText = `✅ Correct! You earned ${attempt === 1 ? 5 : 2} points.`;
    setTimeout(() => {
      currentQuestionIndex++;
      if (currentQuestionIndex < totalQuestions) {
        showQuestion();
      } else {
        endGame();
      }
    }, 1000);
  } else {
    if (attempt === 2) {
      feedback.innerText = `❌ Incorrect. The correct answer was: ${correct}`;
      setTimeout(() => {
        currentQuestionIndex++;
        if (currentQuestionIndex < totalQuestions) {
          showQuestion();
        } else {
          endGame();
        }
      }, 2000);
    } else {
      feedback.innerText = "❌ Try again.";
    }
  }
}

function endGame() {
  document.getElementById("quizBox").classList.add("hidden");
  document.getElementById("scoreBoard").classList.remove("hidden");
  document.getElementById("finalScore").innerText = `${currentPlayer}, your final score is ${score}`;

  scores.push({ name: currentPlayer, score });
  scores.sort((a, b) => b.score - a.score);
  localStorage.setItem("scores", JSON.stringify(scores));

  const topScores = scores.slice(0, 10);
  const list = document.getElementById("topScores");
  list.innerHTML = "";
  topScores.forEach(s => {
    const li = document.createElement("li");
    li.innerText = `${s.name}: ${s.score}`;
    list.appendChild(li);
  });
}

function shuffle(arr) {
  return arr.sort(() => Math.random() - 0.5);
}

function updateScoreboard() {
  const scoreboardDiv = document.getElementById("scoreboard");
  const storedScores = JSON.parse(localStorage.getItem("scores")) || [];

  // Get highest score for each player
  const highestScoresMap = {};
  storedScores.forEach(entry => {
    if (!highestScoresMap[entry.name] || entry.score > highestScoresMap[entry.name]) {
      highestScoresMap[entry.name] = entry.score;
    }
  });

  // Convert map to array
  const uniqueHighScores = Object.entries(highestScoresMap).map(([name, score]) => ({ name, score }));

  // Sort descending and take top 10
  uniqueHighScores.sort((a, b) => b.score - a.score);
  const topScores = uniqueHighScores.slice(0, 10);

  // Render fresh scoreboard
  scoreboardDiv.innerHTML = `
    <h3>Top 10 Scores</h3>
    <ul>
      ${topScores.map(entry => `<li>${entry.name}: ${entry.score} points</li>`).join("")}
    </ul>
    <br>
    <button onclick="playAgain()">Play Again</button>
  `;
}


function playAgain() {
  document.querySelector(".score-screen").style.display = "none";
  document.querySelector(".start-screen").style.display = "block";
}

