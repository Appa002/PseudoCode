from InternalError import InternalError

def _sequence(node, state):
    node[0].generate(state)
    if len(node) > 1:
        node[1].generate(state)


def _for_loop(node, state):
    index = node[1].generate(state).get(state)
    limit = node[2].generate(state).get(state)
    state.register(node[0].data, index)

    try:
        index <= limit
    except TypeError:
        raise InternalError("Types in for loop don't support comparison, in line: " + str(node[0].line))

    while index <= limit:
        state.assign(node[0].data, index)
        node[3].generate(state)
        try:
            index += 1
        except TypeError:
            raise InternalError("Not an iterator, in for loop in line: " + str(node[0].line))


def _while_loop(node, state):
    while node[0].generate(state).get(state):
        node[1].generate(state)


def _if_stmt(node, state):
    if len(node) == 1:
        node[0].generate(state)
        return

    if node[0].generate(state).get(state):
        node[1].generate(state)
    elif len(node) > 2:
        node[2].generate(state)