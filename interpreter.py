import random
from parser import Number, String, Var, Superposition, Let, Say

class Interpreter:
    def __init__(self):
        self.vars = {}

    def collapse(self, value):
        if isinstance(value, Superposition):
            return random.choice([self.evaluate(o) for o in value.options])
        return value

    def evaluate(self, node):
        if isinstance(node, (Number, String)):
            return node.value

        if isinstance(node, Superposition):
            return node

        if isinstance(node, Var):
            if node.name not in self.vars:
                raise Exception(f"Unknown variable: {node.name}")
            value = self.collapse(self.vars[node.name])
            self.vars[node.name] = value
            return value

        raise Exception(f"Cannot evaluate: {node}")

    def execute(self, stmt):
        if isinstance(stmt, Let):
            self.vars[stmt.name] = self.evaluate(stmt.value)

        elif isinstance(stmt, Say):
            value = self.collapse(self.evaluate(stmt.value))
            print(value)
        else:
            raise Exception(f"Cannot execute: {stmt}")

    def run(self, program):
        for stmt in program:
            self.execute(stmt)