class InterpreterValue:
    def __init__(self, sym):
        self.sym = sym

    def assign(self, value, state):
        state.memory[self.sym] = value

    def get(self, state):
        return state.memory[self.sym]


class SpoofInterpreterValue:
    def __init__(self, value):
        self.value = value

    def assign(self, value, state):
        self.value = value

    def get(self, state):
        return self.value