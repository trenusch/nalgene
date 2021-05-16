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

class Subject:
    def __init__(self, genus, value, known=False):
        self.known = known
        self.value = value
        self.attributes = []
        self.genus = genus


class Entity:
    def __init__(self, genus, value, known=False):
        self.value = value
        self.known = known
        self.parents = []
        self.children = []
        self.attributes = []
        self.genus = genus

    def add_parents(self, parent):
        self.parents.append(parent)

    def add_children(self, child):
        self.children.append(child)

    def add_attributes(self, attribute):
        self.attributes.append(attribute)


class Attribute:
    def __init__(self, parent, value, known=False):
        self.known = known
        self.value = value
        self.parent = parent


class Action:
    def __init__(self, value, perfekt=None, known=False):
        self.known = known
        self.value = value
        self.perfekt = perfekt
