KEYWORDS = {"let", "say", "tunnel", "through", "wide", "observe"}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

SYMBOLS = {
    "=": "EQUALS",
    "|": "PIPE",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "(": "LPAREN",
    ")": "RPAREN",
    ",": "COMMA",
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def current(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.current() is not None and self.current() in  " \t\r\n":
            self.advance()

    def read_number(self):
        digits = ""
        while self.current() is not None and self.current().isdigit():
            digits += self.current()
            self.advance()
        return int(digits)

    def read_word(self):
        word = ""
        while self.current() is not None and (self.current().isalnum() or self.current() == "_"):
            word += self.current()
            self.advance()
        return word

    def next_token(self):
        self.skip_whitespace()
        ch = self.current()

        if ch is None:
            return Token("EOF", None)

        if ch.isdigit():
            return Token("NUMBER", self.read_number())

        if ch.isalpha() or ch == "_":
            word = self.read_word()
            if word in KEYWORDS:
                return Token(word.upper(), word)
            return Token("IDENT", word)

        if ch == '"':
            return Token("STRING", self.read_string())

        if ch in SYMBOLS:
            self.advance()
            return Token(SYMBOLS[ch], ch)

        raise Exception(f"Unknown character: {ch!r}")

    def read_string(self):
        self.advance()
        text = ""
        while self.current() is not None and self.current() !='"':
            text += self.current()
            self.advance()
        self.advance()
        return text

    def tokenize(self):
        tokens = []
        tok = self.next_token()
        while tok.type != "EOF":
            tokens.append(tok)
            tok = self.next_token()
        tokens.append(tok)
        return tokens

if __name__  == "__main__":
    lx = LEXER('let coin = 0 | 1\nsay "hi"')
    print(lx.toxenize())

