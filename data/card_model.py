class CardModel:
    def __init__(self, id:int, korean, english, japanese, pronunciation_hiragana, pronunciation_romaji):
        self.id = id
        self.korean = korean
        self.english = english
        self.japanese = japanese
        self.pronunciation_hiragana = pronunciation_hiragana
        self.pronunciation_romaji = pronunciation_romaji

    def to_dict(self):
        return {
            "id": self.id,
            "korean": self.korean,
            "english": self.english,
            "japanese": self.japanese,
            "pronunciation_hiragana": self.pronunciation_hiragana,
            "pronunciation_romaji": self.pronunciation_romaji,
        }