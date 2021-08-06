from words import *


class MentalLexicon:
    def __init__(self):
        self.items = []
        self.words = []

    def add_item(self, item):
        item = eval(item)
        if item.value not in [concept.value for concept in self.items]:
            self.items.append(item)
            if item.known:
                self.words.append(item.value)
        else:
            self.items.remove(self.from_word(item.value))
            self.items.append(item)
            if item.value in self.words:
                self.words.remove(item.value)
            if item.known:
                self.words.append(item.value)
        if type(item) == Attribute:
            parent = self.from_word(item.parent)
            if parent is not None:
                parent.add_attribute(item)

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