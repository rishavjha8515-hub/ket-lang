from lexer import Lexer

class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class String:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value!r})"

class Var:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"

class Superposition:
    def __init__(self, options):
        self.options = options

    def __repr__(self):
        return f"Superposition({self.options})"

class Let:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Let({self.name}, {self.value})"

class Say:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Say({self.value})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"
class Tunnel:
    def __init__(self, energy, height, width, observed=False):
        self.energy = energy
        self.height = height
        self.width = width
        self.observed = observed

    def __repr__(self):
        return f"Tunnel({self.energy}, {self.height}, {self.width}, observed={self.observed})"

class Passport:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Passport({self.name})"
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(self, type):
        tok = self.current()
        if tok.type != type:
            raise Exception(f"Expected {type} but got {tok}")
        self.advance()
        return tok

    def parse_primary(self):
        tok = self.current()

        if tok.type == "NUMBER":
            self.advance()
            return Number(tok.value)

        if tok.type == "STRING":
            self.advance()
            return String(tok.value)

        if tok.type == "IDENT":
            self.advance()
            return Var(tok.value)

        if tok.type == "LPAREN":
            self.advance()
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        
        raise Exception(f"Unexpected token: {tok}")

    def parse_term(self):
        left = self.parse_primary()

        while self.current().type in ("STAR", "SLASH"):
            op = self.current().value
            self.advance()
            right = self.parse_primary()
            left = BinOp(left, op, right)

        return left

    def parse_arith(self):
        left = self.parse_term()

        while self.current().type in ("PLUS", "MINUS"):
            op = self.current().value
            self.advance()
            right = self.parse_term()
            left = BinOp(left, op, right)

        return left
    
    def parse_expression(self):
        first = self.parse_arith()

        if self.current().type != "PIPE":
            return first

        options = [first]
        while self.current().type == "PIPE":
            self.advance()
            options.append(self.parse_arith())

        return Superposition(options)

    def parse_statement(self):
        tok = self.current()

        if tok.type == "LET":
            self.advance()
            name = self.expect("IDENT").value
            self.expect("EQUALS")
            value = self.parse_expression()
            return Let(name, value)

        if tok.type == "SAY":
            self.advance()
            value = self.parse_expression()
            return Say(value)

        if tok.type == "TUNNEL":
            self.advance()
            energy = self.parse_arith()
            self.expect("THROUGH")
            height = self.parse_arith()
            self.expect("WIDE")
            width = self.parse_arith()
            return Tunnel(energy, height, width)

        if tok.type == "OBSERVE":
            self.advance()
            stmt = self.parse_statement()
            if not isinstance(stmt, Tunnel):
                raise Exception("observe can only used with tunnel")
            stmt.observed = True
            return stmt

        if tok.type == "PASSPORT":
            self.advance()
            name = self.expect("IDENT").value
            return Passport(name)
        
        raise Exception(f"Unexpected statement start: {tok}")

    def parse_program(self):
        statements = []
        while self.current().type != "EOF":
            statements.append(self.parse_statement())
        return statements

if __name__ == "__main__":
    tokens = Lexer("passport coin").tokenize()
    print(Parser(tokens).parse_program())