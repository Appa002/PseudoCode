from Parser.Capture import Capture
from Lexer.Token import Token
from AbstractSyntaxTree.ASTNode import ASTNode
import AbstractSyntaxTree.ASTExecs.maths as maths
import AbstractSyntaxTree.ASTExecs.control_flow as control_flow
import AbstractSyntaxTree.ASTExecs.data as data
import AbstractSyntaxTree.ASTExecs.logic as logic
import AbstractSyntaxTree.ASTExecs.side_effects as side_effects
from InternalError import InternalError

def matches (parse_tree, head, body):
    if parse_tree.head != head:
        return False

    if len(parse_tree.body) != len(body):
        return False

    for i in range(len(body)):
        if isinstance(parse_tree.body[i], Token):
            if parse_tree.body[i].symbol != body[i]:
                return False
        elif isinstance(parse_tree.body[i], Capture):
            if parse_tree.body[i].head != body[i]:
                return False
        else:
            raise Exception("Error: WTF")

    return True

def _generation_expr(parse_tree, carry):
    # Expression ---------------------------------------------------------------------------
    # --- Maths ---
    if matches(parse_tree, "expr", ["+", "expr"]):
        return ASTNode(maths._addition, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["+", "expr", "expr"]):
        x = ASTNode(maths._addition, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", ["-", "expr"]):
        return ASTNode(maths._subtraction, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["-", "expr", "expr"]):
        x = ASTNode(maths._subtraction, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)


    elif matches(parse_tree, "expr", ["*", "expr"]):
        return ASTNode(maths._multiplication, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["*", "expr", "expr"]):
        x = ASTNode(maths._multiplication, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", ["/", "expr"]):
        return ASTNode(maths._division, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["/", "expr", "expr"]):
        x = ASTNode(maths._division, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", ["%", "expr"]):
        return ASTNode(maths._modulo, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["%", "expr", "expr"]):
        x = ASTNode(maths._modulo, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    # --- Logic ---
    elif matches(parse_tree, "expr", ["=", "expr"]):
        return ASTNode(logic._equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["=", "expr", "expr"]):
        x = ASTNode(logic._equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", ["<=", "expr"]):
        return ASTNode(logic._less_equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["<=", "expr", "expr"]):
        x = ASTNode(logic._less_equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", [">=", "expr"]):
        return ASTNode(logic._greater_equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", [">=", "expr", "expr"]):
        x = ASTNode(logic._greater_equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", ["<", "expr"]):
        return ASTNode(logic._less, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["<", "expr", "expr"]):
        x = ASTNode(logic._less, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", [">", "expr"]):
        return ASTNode(logic._greater, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", [">", "expr", "expr"]):
        x = ASTNode(logic._greater, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    elif matches(parse_tree, "expr", ["!=", "expr"]):
        return ASTNode(logic._not_equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["!=", "expr", "expr"]):
        x = ASTNode(logic._not_equal, [carry, generate(parse_tree.body[1], None)], parse_tree.body[0].line)
        return generate(parse_tree.body[2], x)

    # Data ---------------------------------------------------------------------------

    elif matches(parse_tree, "expr", ["LITERAL"]):
        return ASTNode(data._literal, [parse_tree.body[0]], parse_tree.body[0].line)

    elif matches(parse_tree, "expr", ["SYMBOL"]):
        return ASTNode(data._symbol, [parse_tree.body[0]], parse_tree.body[0].line)

    # Special --------------------------------------------------------------------------

    elif matches(parse_tree, "expr", ["expr", "expr"]):
        x = generate(parse_tree.body[0], carry)
        return generate(parse_tree.body[1], x)

    elif matches(parse_tree, "expr", ["expr"]):
        return generate(parse_tree.body[0], None)

    elif matches(parse_tree, "expr", ["(", "expr", ")"]):
        return generate(parse_tree.body[1], None)

    return False

def _generation_loop(parse_tree, carry):
    if matches(parse_tree, "loop", ["loop", "SYMBOL", "from", "expr", "to", "expr", "\n", "start", "end", "loop"]):
        return ASTNode(control_flow._for_loop, [parse_tree.body[1],
                                              generate(parse_tree.body[3], None),
                                              generate(parse_tree.body[5], None),
                                              generate(parse_tree.body[7], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "loop", ["loop", "while", "expr", "\n", "start","end", "loop"]):
        return ASTNode(control_flow._while_loop, [generate(parse_tree.body[2], None), generate(parse_tree.body[4], None)], parse_tree.body[0].line)

    return False

def _generation_keyword(parse_tree, carry):
    if matches(parse_tree, "keyword", ["output", "LITERAL"]):
        return ASTNode(side_effects._output, [
            ASTNode(data._literal, [parse_tree.body[1]], parse_tree.body[1].line)], parse_tree.body[0].line)

    elif matches(parse_tree, "keyword", ["output", "expr"]):
        return ASTNode(side_effects._output, [generate(parse_tree.body[1], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "keyword", ["input", "SYMBOL"]):
        return ASTNode(side_effects._input, [parse_tree.body[1]], parse_tree.body[0].line)

    elif matches(parse_tree, "keyword", ["debugger"]):
        return ASTNode(side_effects._debugger, [], parse_tree.body[0].line)

    return False

def _generation_condition(parse_tree, carry):
    # If Condition -----------------------------------------------------------------------------------------------------

    if matches(parse_tree, "condition", ["if", "expr", "then", "\n", "start", "end", "if"]):
        return ASTNode(control_flow._if_stmt, [generate(parse_tree.body[1], None), generate(parse_tree.body[4], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "condition", ["if", "expr", "then", "\n", "start", "else_condition"]):
        return ASTNode(control_flow._if_stmt, [generate(parse_tree.body[1], None),
                                               generate(parse_tree.body[4], None),
                                               generate(parse_tree.body[5], None)], parse_tree.body[0].line)

    # Else Condition ---------------------------------------------------------------------------------------------------

    elif matches(parse_tree, "else_condition", ["else", "then", "\n", "start", "end", "if"]):
        return ASTNode(control_flow._if_stmt, [generate(parse_tree.body[3], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "else_condition", ["else", "if", "expr", "then", "\n", "start", "end", "if"]):
        return ASTNode(control_flow._if_stmt, [generate(parse_tree.body[2], None), generate(parse_tree.body[5], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "else_condition", ["else", "if", "expr", "then", "\n", "start", "else_condition"]):
        return ASTNode(control_flow._if_stmt, [generate(parse_tree.body[2], None),
                                               generate(parse_tree.body[5], None),
                                               generate(parse_tree.body[6], None)], parse_tree.body[0].line)


    return False


def generate(parse_tree, carry):
    if matches(parse_tree, "start", ["SYMBOL", "=", "expr", "\n", "start"]):
        c = ASTNode(data._assignment, [parse_tree.body[0], generate(parse_tree.body[2], None)], parse_tree.body[0].line)
        return ASTNode(control_flow._sequence, [c, generate(parse_tree.body[4], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["SYMBOL", "=", "expr", "\n"]):
        return ASTNode(data._assignment, [parse_tree.body[0], generate(parse_tree.body[2], None)], parse_tree.body[0].line)

    x = _generation_expr(parse_tree, carry)
    if x: return x

    x = _generation_loop(parse_tree, carry)
    if x: return x

    x = _generation_keyword(parse_tree, carry)
    if x: return x

    x = _generation_condition(parse_tree, carry)
    if x: return x

    elif matches(parse_tree, "start", ["expr", "\n"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["expr", "\n", "start"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None), generate(parse_tree.body[2], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["loop", "\n"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["loop", "\n", "start"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None), generate(parse_tree.body[2], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["keyword", "\n"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["keyword", "\n", "start"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None), generate(parse_tree.body[2], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["condition", "\n"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None)], parse_tree.body[0].line)

    elif matches(parse_tree, "start", ["condition", "\n", "start"]):
        return ASTNode(control_flow._sequence, [generate(parse_tree.body[0], None), generate(parse_tree.body[2], None)], parse_tree.body[0].line)

    raise InternalError("Unknown parse tree sequence:\n" + str(parse_tree), parse_tree)

"""
    
"""