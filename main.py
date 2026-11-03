import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def base_path():
   return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

def run_file(path):
    source = open(path).read()
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()
    Interpreter().run(program)

if len(sys.argv) > 1:
    run_file(sys.argv[1])
else:
    default = os.path.join(base_path(), "examples", "hello.ket")
    print("Ket demo (examples/hello.ket)\n")
    run_file(default)
    input("\n Press Enter to exit...")