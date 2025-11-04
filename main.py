import json
import os
import random
from ui import Ui
from data.card_model import CardModel

CARDS_FILE = "data/cards.json"
PROGRESS_FILE = "data/progress.json"

with open(CARDS_FILE, encoding="utf-8") as file:
    cards = json.load(file)

if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, encoding="utf-8") as file:
        progress = json.load(file)
else:
    with open(PROGRESS_FILE, encoding="utf-8", mode="a") as file:
        # every cards start from box 1
        progress = {str(card["id"]): 1 for card in cards}
        json.dump(progress, file)


def get_cards_for_today():
    """오늘 복습해야 할 카드 선택"""
    today_cards = []
    for card in cards:
        card = CardModel(
            id=card["id"],
            korean=card["korean"],
            english=card["english"],
            japanese=card["japanese"],
            pronunciation_romaji=card["pronunciation_romaji"],
            pronunciation_hiragana=card["pronunciation_hiragana"]
        )
        box = progress[str(card.id)]
        # 복습 주기 (box 번호에 따라 다름)
        if box == 1:
            today_cards.append(card)
        elif box == 2 and random.random() < 0.5:
            today_cards.append(card)
        elif box == 3 and random.random() < 0.25:
            today_cards.append(card)
        elif box == 4 and random.random() < 0.15:
            today_cards.append(card)
        elif box == 5 and random.random() < 0.05:
            today_cards.append(card)
    return today_cards

def start_study():
    today_cards = get_cards_for_today()
    random.shuffle(today_cards)

    ui = Ui(today_cards=today_cards, progress=progress)
    ui.draw()

    # 진행상황 저장
    with open(PROGRESS_FILE, mode="w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

start_study()