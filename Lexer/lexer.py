from Lexer.Token import Token

SPECIAL_CHARS = ["+", "-", "=", "*", "/", "(", ")", "\"", "\n", ">=", "<=", "+=", "-=", " ", "<", ">"]
pos = 0
tokens = []
cur_line = 1

def is_number(c):
    return 48 <= ord(c) <= 57


def handle_number(document):
    global pos, cur_line
    total_str = ""
    while pos < len(document) and is_number(document[pos]) or document[pos] == ".":
        total_str += document[pos]
        pos += 1

    tokens.append(Token("LITERAL", float(total_str), cur_line))


def handle_string(document):
    global pos, tokens, cur_line
    pos += 1
    string = ""
    while pos < len(document) and document[pos] != "\"":
        string += document[pos]
        pos += 1

    if pos >= len(document):
        raise Exception("Unclosed string, in line: " + cur_line)

    tokens.append(Token("LITERAL", string, cur_line))


def is_keyword (str):
    keywords = ["input", "output", "loop", "until", "while", "end", "to", "from", "if", "then", "else", "debugger"]
    return str in keywords


def is_special (str):
    return str in SPECIAL_CHARS

def run (document):
    global pos, tokens, cur_line

    global pos, cur_line

    buffer = ""

    while pos < len(document):
        if document[pos] in SPECIAL_CHARS:
            if len(buffer) > 0:
                if is_keyword(buffer):
                    tokens.append(Token(buffer, "", cur_line))
                else:
                    tokens.append(Token("SYMBOL", buffer, cur_line))
                buffer = ""
                continue

            if pos + 1 < len(document) and document[pos] + document[pos + 1] in [">=", "==", "<=", "+=", "-="]:
                tokens.append(Token(document[pos] + document[pos + 1], "", cur_line))
                pos += 2
            else:
                if document[pos] == "\"":
                    handle_string(document)
                elif document[pos] != " ":
                    tokens.append(Token(document[pos], "", cur_line))
                pos += 1

        elif is_number(document[pos]) and len(buffer) == 0:
            handle_number(document)
        else:
            buffer += document[pos]
            pos += 1

        if pos < len(document) and document[pos] == "\n":
            cur_line += 1
    return tokens