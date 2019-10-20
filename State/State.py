from InternalError import InternalError

class State:
    def __init__(self):
        self.memory = {}

    def register(self, sym, value):
        self.memory[sym] = value

    def assign(self, sym, value):
        if sym not in self.memory:
            raise InternalError("Undefined variable `"+sym+"` in line: ")

        if type(self.memory[sym]) != type(value):
            raise InternalError("Variable of type " + type(self.memory[sym]).__name__ + "assigned type " + type(value).__name__ + "in line: ")

        self.memory[sym] = value
