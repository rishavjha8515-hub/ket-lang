import random
import math
from parser import Number, String, Var, Superposition, Let, Say, BinOp, Tunnel

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

        if isinstance(node, BinOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.op == "+":
                return left + right
            if node.op == "-":
                return left - right
            if node.op == "*":
                return left * right
            if node.op == "/":
                return left / right
            
        raise Exception(f"Cannot evaluate: {node}")

    def execute(self, stmt):
        if isinstance(stmt, Let):
            self.vars[stmt.name] = self.evaluate(stmt.value)

        elif isinstance(stmt, Say):
            value = self.collapse(self.evaluate(stmt.value))
            print(value)
        elif isinstance(stmt, Tunnel):
            energy = self.evaluate(stmt.energy)
            height = self.evaluate(stmt.height)
            width = self.evaluate(stmt.width)

            if energy >= height:
                chance = 1.0
            else:
                kappa = math.sqrt(height - energy)
                chance = math.exp(-2 * kappa * width)

            if stmt.observed:
                print(f"Observed! Odds were {chance:.1%}, but watching collasped it. Reflected")
            elif random.random() < chance:
                print(f"Tunneled through! ({chance:.1%} chance)")
            else:
                print(f"Reflected. ({chance:.1%} chance)") #traded logic from stardance project
        else:
            raise Exception(f"Cannot execute: {stmt}")

    def run(self, program):
        for stmt in program:
            self.execute(stmt)