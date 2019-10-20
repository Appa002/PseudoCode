from Parser.Capture import Capture
from InternalError import InternalError
from Colour import bcolors

deepest_idx = 0

def _do_symbol_equal(tokens, symbols):
    global deepest_idx

    out = []

    if len(symbols) > len(tokens):
        return []

    sym_idx = 0
    for i in range(len(symbols)):
        if callable(symbols[i]):
            x = symbols[i](tokens[sym_idx:])
            if x == True:
                continue
            if x:
                out.append(x)
            else:
                return []
            sym_idx += x.get_size()
            continue

        if sym_idx < len(tokens) and tokens[sym_idx].symbol == symbols[i]:
            out.append(tokens[sym_idx])
        else:
            return []
        sym_idx += 1

    if sym_idx > deepest_idx:
        deepest_idx = sym_idx

    return out


def _expr_primary(tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, ["LITERAL"])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["SYMBOL"])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["(", _expr, ")"])
    if out: return Capture("expr", out, tokens[0].line)

def _expr_logic_q(tokens):
    if len(tokens) == 0:
        return []

    # Logic ----------------------------------------
    out = _do_symbol_equal(tokens, ["=", _expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["<=", _expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, [">=", _expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["<", _expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, [">", _expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["!=", _expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)

    return True

def _expr_logic(tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, [_expr_primary, _expr_logic_q])
    if out: return Capture("expr", out, tokens[0].line)



def _expr_term_q(tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, ["*", _expr_logic, _expr_term_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["/", _expr_logic, _expr_term_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["%", _expr_logic, _expr_term_q])
    if out: return Capture("expr", out, tokens[0].line)

    return True

def _expr_term(tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, [_expr_logic, _expr_term_q])
    if out: return Capture("expr", out, tokens[0].line)

def _expr_q (tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, ["+", _expr_term, _expr_q])
    if out: return Capture("expr", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["-", _expr_term, _expr_q])
    if out: return Capture("expr", out, tokens[0].line)

    return True

def _expr(tokens):
    if len(tokens) == 0:
        return []

    # Maths -----------------------------------
    out = _do_symbol_equal(tokens, [_expr_term, _expr_q])
    if out: return Capture("expr", out, tokens[0].line)


def _loop(tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, ["loop", "SYMBOL", "from", _expr, "to", _expr, "\n", _start, "end", "loop"])
    if out: return Capture("loop", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["loop", "while", _expr, "\n", _start, "end", "loop"])
    if out: return Capture("loop", out, tokens[0].line)


def _keyword(tokens):
    if len(tokens) == 0:
        return []

    # Output ----------------------------------------
    out = _do_symbol_equal(tokens, ["output", _expr])
    if out: return Capture("keyword", out, tokens[0].line)

    # Input ----------------------------------------
    out = _do_symbol_equal(tokens, ["input", "SYMBOL"])
    if out: return Capture("keyword", out, tokens[0].line)

    # Debugger -----------------------------------------
    out = _do_symbol_equal(tokens, ["debugger"])
    if out: return Capture("keyword", out, tokens[0].line)


def _else_condition(tokens):
    if len(tokens) == 0:
        return []

    out = _do_symbol_equal(tokens, ["else", "then", "\n", _start, "end", "if"])
    if out: return Capture("else_condition", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["else", "if", _expr, "then", "\n", _start, _else_condition])
    if out: return Capture("else_condition", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["else", "if", _expr, "then", "\n", _start, "end", "if"])
    if out: return Capture("else_condition", out, tokens[0].line)

def _condition(tokens):
    if len(tokens) == 0:
        return []

    # If ----------------------------------------
    out = _do_symbol_equal(tokens, ["if", _expr, "then", "\n", _start, "end", "if"])
    if out: return Capture("condition", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["if", _expr, "then", "\n", _start, _else_condition])
    if out: return Capture("condition", out, tokens[0].line)


def _start(tokens):
    if len(tokens) == 0:
        return []

    # Assignment --------------------------------------
    out = _do_symbol_equal(tokens, ["SYMBOL", "=", _expr, "\n", _start])
    if out: return Capture("start", out, tokens[0].line)

    out = _do_symbol_equal(tokens, ["SYMBOL", "=", _expr, "\n"])
    if out: return Capture("start", out, tokens[0].line)

    # Expression --------------------------------------
    out = _do_symbol_equal(tokens, [_expr, "\n", _start])
    if out: return Capture("start", out, tokens[0].line)

    out = _do_symbol_equal(tokens, [_expr, "\n"])
    if out: return Capture("start", out, tokens[0].line)

    # Loops ------------------------------------------

    out = _do_symbol_equal(tokens, [_loop, "\n", _start])
    if out: return Capture("start", out, tokens[0].line)

    out = _do_symbol_equal(tokens, [_loop, "\n"])
    if out: return Capture("start", out, tokens[0].line)

    # Keywords ---------------------------------------

    out = _do_symbol_equal(tokens, [_keyword, "\n", _start])
    if out: return Capture("start", out, tokens[0].line)

    out = _do_symbol_equal(tokens, [_keyword, "\n"])
    if out: return Capture("start", out, tokens[0].line)

    # Conditions -------------------------------------

    out = _do_symbol_equal(tokens, [_condition, "\n", _start])
    if out: return Capture("start", out, tokens[0].line)

    out = _do_symbol_equal(tokens, [_condition, "\n"])
    if out: return Capture("start", out, tokens[0].line)


def parse(tokens):
    x = _start(tokens)
    if not x or x.get_size() < len(tokens):
        msg = ""
        line = 0
        if deepest_idx < len(tokens):
            msg += tokens[deepest_idx].symbol
            line = tokens[deepest_idx].line
        else:
            msg += tokens[-1].symbol
            line = tokens[-1].symbol

        msg = msg.replace("\n", "\\n")

        raise InternalError(bcolors.FAIL + "Unexpected " + bcolors.BOLD  + msg + bcolors.ENDC + bcolors.FAIL + ", in line: " + str(line) + bcolors.ENDC, x)
    return x