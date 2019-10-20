from Colour import bcolors

def _input(node, state):
    if not node[0].data.isupper():
        print(bcolors.OKBLUE + "Warning: Variable names should be all uppercase, in line: " + str(node[0].line) + bcolors.ENDC)

    state.register(node[0].data, 0)
    val = input("Input for " + node[0].data + ": ")

    try:
        val = float(val)
    except ValueError:
        pass
    state.memory[node[0].data] = val

def _output(node, state):
    x = node[0].generate(state).get(state)
    if type(x) == float and int(x) == x:
        x = int(x)

    print(str(x))

def _debugger(node, state):
    print("")
    print(bcolors.UNDERLINE + "Debugger" + bcolors.ENDC)
    for var in state.memory:
        type_str = "number" if type(state.memory[var]).__name__  == "float" else "string"
        print(var + "  ->  " + str(state.memory[var]) + "  ; " + type_str)
    print("")