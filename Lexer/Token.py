class Token:
    def __init__(self, symbol, data, line):
        self.symbol = symbol
        self.data = data
        self.line = line

    def __repr__(self):
        return "eos" if self.symbol == "\n" else self.symbol

    def __str__(self, indent = "", is_last = False):
        s = indent
        if (is_last):
            s += "\\-"
            indent += "     "
        else:
            s += "|-"
            indent += "|    "

        rep = "eos" if self.symbol == "\n" else self.symbol

        if str(self.data) != "":
            return s + "[" + rep + " ("+ str(self.data) +")" + "]\n"
        else:
            return s + "["+rep+"]\n"