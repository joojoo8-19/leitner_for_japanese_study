import streamlit as st
import random
import json
from data.card_model import CardModel

# ====== 데이터 로드 ======
with open("../data/cards.json", "r", encoding="utf-8") as f:
    cards_data = json.load(f)

cards = [
    CardModel(**card)
    for card in cards_data
]

# 진행도 파일
PROGRESS_FILE = "../data/progress.json"
try:
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        progress = json.load(f)
except FileNotFoundError:
    progress = {str(card.id): 1 for card in cards}


# ====== 함수 ======
def get_cards_for_today():
    today = []
    for card in cards:
        box = progress[str(card.id)]
        if box == 1:
            today.append(card)
        elif box == 2 and random.random() < 0.5:
            today.append(card)
        elif box == 3 and random.random() < 0.25:
            today.append(card)
        elif box == 4 and random.random() < 0.15:
            today.append(card)
        elif box == 5 and random.random() < 0.05:
            today.append(card)
    return today

# ====== UI ======
st.title("🇯🇵 100 Japanese Sentences with Leitner System")

if "index" not in st.session_state:
    st.session_state.index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "today_cards" not in st.session_state:
    st.session_state.today_cards = get_cards_for_today()

today_cards = st.session_state.today_cards

if not today_cards:
    st.success("오늘 학습할 카드가 없습니다 🎉")
else:
    if st.session_state.index >= len(today_cards):
        st.success("오늘의 모든 카드를 완료했습니다 🎉")
        st.stop()

    card = today_cards[st.session_state.index]

    st.write(f"**Card {st.session_state.index + 1} / {len(today_cards)}**")
    st.write(f"**Box:** {progress[str(card.id)]}")
    st.divider()

    st.write("### 🇰🇷 Korean")
    st.markdown(f"**{card.korean}**")

    if not st.session_state.show_answer:
        if st.button("🔍 Reveal Answer"):
            st.session_state.show_answer = True
            st.rerun()  # 👈 버튼 즉시 반응하게 만듦
    else:
        st.divider()
        st.write("### 🇯🇵 Japanese")
        st.markdown(f"{card.japanese}")
        st.markdown(f"{card.pronunciation_hiragana}")
        st.markdown(f"({card.pronunciation_romaji})")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Correct"):
                progress[str(card.id)] = min(progress[str(card.id)] + 1, 5)
                st.session_state.show_answer = False
                st.session_state.index += 1
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(progress, f, ensure_ascii=False, indent=2)
                st.rerun()  # 👈 즉시 다음 카드로 넘어가게
        with col2:
            if st.button("❌ Incorrect"):
                progress[str(card.id)] = 1
                st.session_state.show_answer = False
                st.session_state.index += 1
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(progress, f, ensure_ascii=False, indent=2)
                st.rerun()  # 👈 즉시 다음 카드로 넘어가게