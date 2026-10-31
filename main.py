import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

source = open(sys.argv[11]).read()
tokens = Lexer(source).tokenize()
program = Parser(tokens).parse_program()
Interpreter().run(program)