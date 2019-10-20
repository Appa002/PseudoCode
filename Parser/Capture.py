class Capture:
    def __init__(self, head, body, line):
        self.head = head
        self.body = body
        self.line = line

    def get_size(self):
        s = len(self.body)
        for it in self.body:
            if isinstance(it, Capture):
                s += it.get_size()
                s -= 1
        return s

    def __repr__(self):
        return str(self.head)

    def __str__(self, indent = "", is_last = False):
        s = indent
        if (is_last):
            s += "\\-"
            indent += "     "
        else:
            s += "|-"
            indent += "|    "

        s += "["+self.head+"]\n"

        for child in self.body:
            s += child.__str__(indent, child == self.body[-1])
        return s

