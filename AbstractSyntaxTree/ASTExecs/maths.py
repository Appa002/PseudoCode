from State.InterpreterValue import SpoofInterpreterValue
from InternalError import InternalError

def _addition(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)


    if type(a) != type(b):
        if type(a) == type("string"):
            b = str(b)
        elif type(b) == type("string"):
            a = str(a)

    return SpoofInterpreterValue(a + b)

def _subtraction(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of arithmetic expression not of same type, in line: " + str(node[0].line))

    if type(a) != type(0.2) or type(b) != type(0.3):
        raise InternalError("Arithmetic expression requires operands to be of type number, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a - b)

def _multiplication(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of arithmetic expression not of same type, in line: " + str(node[0].line))

    if type(a) != type(0.2) or type(b) != type(0.3):
        raise InternalError(
            "Arithmetic expression requires operands to be of type number, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a * b)

def _division(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of arithmetic expression not of same type, in line: " + str(node[0].line))

    if type(a) != type(0.2) or type(b) != type(0.3):
        raise InternalError(
            "Arithmetic expression requires operands to be of type number, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a / b)

def _modulo(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of arithmetic expression not of same type, in line: " + str(node[0].line))

    if type(a) != type(0.2) or type(b) != type(0.3):
        raise InternalError(
            "Arithmetic expression requires operands to be of type number, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a % b)

