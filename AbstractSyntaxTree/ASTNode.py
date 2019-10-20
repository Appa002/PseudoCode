class ASTNode:
    def __init__(self, exec, body, line):
        self.body = body
        self.exec = exec
        self.line = line

    def generate(self, state):
        return self.exec(self.body, state)

    def __str__(self, indent="", is_last=False):
        s = indent
        if (is_last):
            s += "\\-"
            indent += "     "
        else:
            s += "|-"
            indent += "|    "

        s += "[" + str(self.exec.__name__) + "]\n"

        for child in self.body:
            s+= child.__str__(indent, child == self.body[-1])

        return s
