from State.InterpreterValue import InterpreterValue, SpoofInterpreterValue
from InternalError import InternalError
from Colour import bcolors

def _literal(node, state):
    val = node[0].data
    try:
        val = float(val)
    except ValueError:
        pass

    return SpoofInterpreterValue(val)

def _symbol(node, state):
    sym = node[0].data
    if sym not in state.memory:
        raise InternalError("Undefined variable `" + sym + "` in line: " + str(node[0].line))

    return InterpreterValue(sym)


def _assignment(node, state):
    sym = node[0].data
    value = node[1].generate(state).get(state)

    if not sym.isupper() and not sym in state.memory:
        print(bcolors.OKBLUE + "Warning: Variable names should be all uppercase, in line: " + str(node[0].line) + bcolors.ENDC)

    if sym in state.memory and type(state.memory[sym]) != type(value):
        raise InternalError("Variable of type " + type(state.memory[sym]).__name__ + "assigned type " + type(
            value).__name__ + "in line: " + str(node[0].line))

    state.memory[sym] = value