from State.InterpreterValue import SpoofInterpreterValue
from InternalError import InternalError

def _equal(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of logic expression not of same type, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a == b)

def _not_equal(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of logic expression not of same type, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a != b)

def _less_equal(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of logic expression not of same type, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a <= b)

def _greater_equal(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of logic expression not of same type, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a >= b)

def _less(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of logic expression not of same type, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a < b)

def _greater(node, state):
    a = node[0].generate(state).get(state)
    b = node[1].generate(state).get(state)

    if type(a) != type(b):
        raise InternalError("LHS and RHS of logic expression not of same type, in line: " + str(node[0].line))

    return SpoofInterpreterValue(a > b)