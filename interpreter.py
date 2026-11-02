import random
import math
from parser import Number, String, Var, Superposition, Let, Say, BinOp, Tunnel, Passport, Entangle

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.links = {}

    def collapse(self, value):
        if isinstance(value, Superposition):
            return random.choice([self.evaluate(o) for o in value.options])
        return value

    def collapse_var(self, name):
        value = self.vars[name]
        if not isinstance(value, Superposition):
            return value

        index = random.randrange(len(value.options))
        result = self.evaluate(value.options[index])
        self.vars[name] = result

        partner = self.links.get(name)
        if partner is not None:
            other = self.vars[partner]
            if isinstance(other, Superposition):
                self.vars[partner] = self.evaluate(other.options[index])

        return result
    
    def evaluate(self, node):
        if isinstance(node, (Number, String)):
            return node.value

        if isinstance(node, Superposition):
            return node

        if isinstance(node, Var):
            if node.name not in self.vars:
                raise Exception(f"Unknown variable: {node.name}")
            return self.collapse_var(node.name)

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
                print(f"Observed! Odds were {chance:.1%}, but watching collapsed it. Reflected.")
            elif random.random() < chance:
                print(f"Tunneled through! ({chance:.1%} chance)")
            else:
                print(f"Reflected. ({chance:.1%} chance)") #traded logic from stardance project
        elif isinstance(stmt, Passport):
            if stmt.name not in self.vars:
                raise Exception(f"Unknown variable: {stmt.name}")

            value = self.vars[stmt.name]
            print("--- KET PASSPORT ---")
            print(f"Name: {stmt.name}")

            if isinstance(value, Superposition):
                print("State: superposition")
                print(f"Could be {len(value.options)} values")
            else:
                print("State: collapsed")
                print(f"Value: {value}")
        elif isinstance(stmt, Entangle):
            for name in (stmt.first, stmt.second):
                if name not in self.vars:
                    raise Exception(f"Unknown variable: {name}")
                if not isinstance(self.vars[name], Superposition):
                    raise Exception(f"{name} is already collapsed, cannot entangle")

            a = self.vars[stmt.first]
            b = self.vars[stmt.second]
            if len(a.options) != len(b.options):
                raise Exception("Entangled variables need the same number of options")

            self.links[stmt.first] = stmt.second
            self.links[stmt.second] = stmt.first
        else:
            raise Exception(f"Cannot execute: {stmt}")

    def run(self, program):
        for stmt in program:
            self.execute(stmt)