class MentalLexicon:
    def __init__(self):
        self.items = []
        self.words = []

    def add_item(self, item):
        self.items.append(item)
        if item.known:
            self.words.append(item.value)

    def contains_word(self, item):
        return item in self.words

    def from_word(self, word):
        try:
            return [item for item in self.items if item.value == word][0]
        except IndexError as e:
            return None

    def contains_concept(self, item):
        return item in [item.value for item in self.items]
