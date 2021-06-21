class Words:

    def __init__(self, value, known=False):
        self.value = value
        self.known = known


class Subject(Words):
    def __init__(self, genus, value, known=False):
        self.known = known
        self.value = value
        self.attributes = []
        self.genus = genus



class Entity(Words):
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



class Attribute(Words):
    def __init__(self, parent, value, type, known=False):
        self.known = known
        self.value = value
        self.parent = parent
        self.type = type


class Action(Words):
    def __init__(self, value, perfekt=None, known=False):
        self.known = known
        self.value = value
        self.perfekt = perfekt

