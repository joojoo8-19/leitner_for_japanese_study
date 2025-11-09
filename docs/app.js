let cards = [];
let todayCards = [];
let currentCardIndex = 0;
let progress = {};

// Load progress from localStorage or initialize
if (!localStorage.getItem('progress')) {
  localStorage.setItem('progress', JSON.stringify({}));
}
progress = JSON.parse(localStorage.getItem('progress'));

// Load cards from localStorage or fetch from JSON
async function loadCards() {
  if (!localStorage.getItem('cards')) {
    try {
      const res = await fetch('cards.json');
      const data = await res.json();
      localStorage.setItem('cards', JSON.stringify(data));
      cards = data;
      todayCards = getCardsForBox(1)
    } catch (err) {
      console.error(err);
    }
  } else {
    cards = JSON.parse(localStorage.getItem('cards'));
    todayCards = getCardsForBox(1)
  }
}

const questionText = document.getElementById('question-text');
const answerArea = document.getElementById('answer-card');
const answerJapanese = document.getElementById('answer-text');
const answerHiragana = document.getElementById('answer-hiragana');
const answerRomaji = document.getElementById('answer-romaji');
const revealBtn = document.getElementById('reveal-answer');
const correctBtn = document.getElementById('correct');
const incorrectBtn = document.getElementById('incorrect');
const controls = document.getElementById('answer-buttons');
const cardInfo = document.getElementById('card-info');

function saveProgress() {
  localStorage.setItem('progress', JSON.stringify(progress));
}

function getCardsForBox(boxNumber) {
  return cards.filter(card => {
    const box = progress[card.id] || 1;
    return box === boxNumber;
  });
}

function showCard() {
  if (currentCardIndex >= todayCards.length) {
    alert('오늘 학습할 카드가 없습니다.');
    return;
  }
  const card = todayCards[currentCardIndex];
  questionText.textContent = card.korean;
  answerJapanese.textContent = card.japanese;
  answerHiragana.textContent = card.pronunciation_hiragana;
  answerRomaji.textContent = card.pronunciation_romaji;
  answerArea.classList.add('hidden');
  controls.classList.add('hidden');
  cardInfo.textContent = `Card ${currentCardIndex + 1} / ${todayCards.length} | Box ${progress[card.id] || 1}`;
}

function nextCard() {
  currentCardIndex++;
  if (currentCardIndex < todayCards.length) {
    showCard();
  } else {
    alert('박스 학습이 끝났습니다!');
  }
}

// 초기화 함수
async function init() {
  await loadCards();
  showCard(); // fix : "no cards to study" alert show up when the page loads for the first time
}

function showAnswer(){
  answerArea.classList.remove('hidden');
  controls.classList.remove('hidden');
}

function hideAnswer(){
  answerArea.classList.add('hidden');
  controls.classList.add('hidden');
}

revealBtn.addEventListener('click', () => {
  showAnswer()
});

correctBtn.addEventListener('click', () => {
  hideAnswer()
  const card = todayCards[currentCardIndex];
  progress[card.id] = Math.min((progress[card.id] || 1) + 1, 5);
  saveProgress();
  nextCard();
});

incorrectBtn.addEventListener('click', () => {
  hideAnswer()
  const card = todayCards[currentCardIndex];
  progress[card.id] = 1;
  saveProgress();
  nextCard();
});

document.addEventListener("DOMContentLoaded", () => {
  init();
});

// 박스 버튼 클릭
document.getElementById('box-buttons').addEventListener('click', e => {
  if (e.target.tagName === 'BUTTON') {
    const box = parseInt(e.target.dataset.box);
    todayCards = getCardsForBox(box);
    if (todayCards.length === 0) {
      alert(`Box ${box}에 학습할 카드가 없습니다.`);
      return;
    }
    currentCardIndex = 0;
    showCard();
  }
});
