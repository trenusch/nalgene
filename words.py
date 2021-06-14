from abc import ABC


class Words(ABC):

    def __init__(self, value, known=False):
        self.value = value
        self.known = known

    def get_known(self):
        return self.known

    def set_known(self, value):
        self.known = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_attributes(self):
        return self.attributes


class Subject(Words):
    def __init__(self, genus, value, known=False):
        self.known = known
        self.value = value
        self.attributes = []
        self.genus = genus

    def get_genus(self):
        return self.genus


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

    def get_genus(self):
        return self.genus


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

    def get_perfekt(self):
        return self.perfekt
