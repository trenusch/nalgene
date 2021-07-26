class MentalLexicon:
    def __init__(self):
        self.items = []
        self.words = []

    def add_item(self, item):
        if item.value not in [concept.value for concept in self.items]:
            self.items.append(item)
            if item.known:
                self.words.append(item.value)
        else:
            self.items.remove(self.from_word(item.value))
            if item.value in self.words:
                self.words.remove(item.value)
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

    def remove_item(self, item):
        if item.value in self.words:
            self.words.remove(item.value)
        if item in self.items:
            self.items.remove(item)