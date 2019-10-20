import Lexer.lexer as lexer
import Parser.parser as parser
import AbstractSyntaxTree.abstract_syntax_tree as abstract_syntax_tree
from State.State import State
from Lexer.Token import Token
from InternalError import InternalError
from Colour import bcolors
import sys
import updater
import os
import requests

DETAILED_ERROR = False

def remove_repeated_eos(tokens):
    out = []
    i = 0
    while i < len(tokens):
        out.append(tokens[i])
        if tokens[i].symbol == "\n":
            i += 1
            while i < len(tokens) and tokens[i].symbol == "\n":
                i += 1
        else:
            i += 1
    return out

def cut_of_eos(tokens):
    i = 0
    while tokens[i].symbol == "\n":
        i+=1
    begin_cut = i
    i = len(tokens) - 1
    while tokens[i].symbol == "\n":
        i-=1
    end_cut = i

    return tokens[begin_cut:end_cut+1]

def run (document):
    tokens = lexer.run(document)
    tokens = cut_of_eos(tokens)
    tokens = remove_repeated_eos(tokens)
    tokens.append(Token("\n", "", tokens[-1].line))

    parse_tree = None

    try:
        parse_tree = parser.parse(tokens)
    except InternalError as e:
        print(bcolors.HEADER + "There is a syntax error in your script!" + bcolors.ENDC)
        print(str(e.args[0]))

        if DETAILED_ERROR:
            print("\n\n-------Detailed Parse Tree-------")
            try:
                print(e.args[1])
            except:
                pass
        sys.exit(1)

    ast = None
    try:
        ast = abstract_syntax_tree.generate(parse_tree, None)
    except InternalError as e:
        print(bcolors.HEADER + "There is a parse tree sequence without a corresponding AST rule, this most likely "
                               "isn't an error with your script but with the interpreter." + bcolors.ENDC)
        try:
            body = ""
            for t in e.args[1].body:
                body += t.__repr__() + " "

            print(e.args[1].head + " -> " + body)
        except:
            pass
        sys.exit(1)

    state = State()

    try:
        ast.generate(state)
    except InternalError as e:
        msg = bcolors.FAIL + str(e.args[0]) + bcolors.ENDC
        print(bcolors.HEADER + "An error occurred while executing your script!" + bcolors.ENDC)
        print(msg)

        if DETAILED_ERROR:
            print("\n\n-------Detailed Abstract Syntax Tree-------")
            try:
                print(ast)
            except:
                pass

        sys.exit(1)

def main():
    global DETAILED_ERROR

    print("\033[90m" + "Albert Modenbach - Version " + str(updater.CURRENT_VERSION) + '\033[0m')

    try:
        val = updater.check_for_update()
    except requests.ConnectionError:
        val = {}

    if len(sys.argv) < 2:
        print(bcolors.FAIL + "Usage: interpreter [file path]" + bcolors.ENDC)
        sys.exit(1)

    if "-d" in sys.argv:
        DETAILED_ERROR = True

    if "-u" in sys.argv:
        try:
            updater.auto_update(val)
        except requests.ConnectionError:
            print(bcolors.FAIL + "A Network error occurred" + bcolors.ENDC)
            sys.exit(1)
        return

    file_path = sys.argv[1]
    try:
        f = open(file_path, 'r')
    except IOError:
        print(bcolors.FAIL + "File `" + file_path + "` doesn't exist."+ bcolors.ENDC)
        sys.exit(1)
    with f:
        s = f.read()

    f.close()

    s = s.replace("\t", "    ")

    s += "\n"

    if s == "\n":
        return
    run(s)

if __name__ == "__main__":
    main()