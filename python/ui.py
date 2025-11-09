import tkinter
from tkinter import ttk
from data.card_model import CardModel

class Ui:
    def __init__(self, today_cards:list[CardModel], progress):
        self.window = tkinter.Tk()
        self.window.title("Learn 100 Japanese Sentences with Leitner System")
        self.window.config(padx=20, pady=20)

        self.current_box = 1
        self.today_cards = today_cards
        self.current_card_index = 0
        self.current_card = today_cards[self.current_card_index]
        self.progress = progress

        self.answer_visible = False

        self._setup_widgets()

    def _setup_widgets(self):
        self.title = tkinter.Label(text="Japanese Study")
        self.title.grid(column=0, row=0)
        self.kor_button = tkinter.Button(text="🇰🇷 Korean")
        self.eng_button = tkinter.Button(text="🇺🇸 English")
        self.kor_button.grid(column=3, row=0)
        self.eng_button.grid(column=4, row=0)

        self.divider = ttk.Separator(orient='horizontal')
        self.divider.grid(column=0, row=1,columnspan=5, pady=10, sticky='ew')

        self.box1_button = tkinter.Button(text="Box 1", command=lambda:self.filter_cards_by_box(1))
        self.box1_button.grid(column=0, row=2)
        self.box2_button = tkinter.Button(text="Box 2", command=lambda:self.filter_cards_by_box(2))
        self.box2_button.grid(column=1, row=2)
        self.box3_button = tkinter.Button(text="Box 3", command=lambda:self.filter_cards_by_box(3))
        self.box3_button.grid(column=2, row=2)
        self.box4_button = tkinter.Button(text="Box 4", command=lambda:self.filter_cards_by_box(4))
        self.box4_button.grid(column=3, row=2)
        self.box5_button = tkinter.Button(text="Box 5", command=lambda:self.filter_cards_by_box(5))
        self.box5_button.grid(column=4, row=2)

        self.divider3 = ttk.Separator(orient='horizontal')
        self.divider3.grid(column=0, row=3, columnspan=5, pady=10, sticky='ew')

        self.card_number = tkinter.Label(text=f"Card {self.current_card_index+1} of {len(self.today_cards)}")
        self.box_status = tkinter.Label(text=f"Box {self.progress[str(self.current_card.id)]}")
        self.card_number.grid(column=0, row=4)
        self.box_status.grid(column=4, row=4)

        self.question_canvas = tkinter.Canvas(width=300, height=90)
        self.question_canvas.grid(column=0, columnspan=5, row=5, pady=5, padx=5)
        self.current_lang = self.question_canvas.create_text(10, 30, text="🇰🇷 Korean", anchor="w")
        self.current_question = (
            self.question_canvas.create_text(10, 60, text=self.current_card.korean, anchor="w")
        )
        
        self.answer_button = tkinter.Button(text="Reveal Answer", command=self.show_answer)
        self.answer_button.grid(column=0, columnspan=5, row=6)

        self.answer_canvas = tkinter.Canvas(width=300, height=150, highlightthickness=0)
        self.answer_canvas.create_text(10, 30, text="🇯🇵 Japanese", anchor="w")
        self.answer_japanese = self.answer_canvas.create_text(10, 60, text=self.current_card.japanese, anchor="w")
        self.answer_hiragana = self.answer_canvas.create_text(10, 90, text=self.current_card.pronunciation_hiragana, anchor="w")
        self.answer_romaji = self.answer_canvas.create_text(10, 120, text=self.current_card.pronunciation_romaji, anchor="w")

        self.divider2 = ttk.Separator(orient='horizontal')

        self.correct_button = tkinter.Button(text="✓ Correct", command=self.on_correct)
        self.incorrect_button = tkinter.Button(text="⌧ Incorrect", command=self.on_incorrect)

    def show_answer(self):
        if not self.answer_visible:
            self.answer_visible = True

            self.answer_canvas.grid(column=0, columnspan=5, row=7, pady=5, padx=5)
            self.divider2.grid(column=0, row=8, columnspan=5, pady=10, sticky='ew')
            self.correct_button.grid(column=0, columnspan=2, row=9)
            self.incorrect_button.grid(column=4, columnspan=2, row=9)

            self.window.update()

    def change_box(self, target:int):
        self.current_box = target

    def filter_cards_by_box(self, target:int):
        self.change_box(target)
        filtered = [card for card in self.today_cards if self.progress[str(card.id)] == self.current_box]
        print(filtered)

    def show_next_card(self):
        if self.current_card_index < len(self.today_cards):
            self.answer_visible = False
            self.current_card_index += 1
            self.current_card = self.today_cards[self.current_card_index]

            self.question_canvas.itemconfigure(self.current_question, text=self.current_card.korean)
            self.answer_canvas.itemconfigure(self.answer_japanese, text=self.current_card.japanese)
            self.answer_canvas.itemconfigure(self.answer_hiragana, text=self.current_card.pronunciation_hiragana)
            self.answer_canvas.itemconfigure(self.answer_romaji, text=self.current_card.pronunciation_romaji)

            self.answer_canvas.grid_remove()
            self.window.update()

    def on_correct(self):
        if self.progress[str(self.current_card.id)] < 5:
            self.progress[str(self.current_card.id)] += 1
            print(f"✅ 정답! → Box {self.progress[str(self.current_card.id)]}")
        else:
            print("🎉 이미 최고 단계 (Box 5)")
        self.show_next_card()

    def on_incorrect(self):
        self.progress[str(self.current_card.id)] = 1
        print("❌ 오답 → Box 1로 이동")
        self.show_next_card()

    def draw(self):
        self.window.mainloop()