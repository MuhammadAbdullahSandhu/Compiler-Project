from Token import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_pos = 0

    def current_token(self):
        if self.current_token_pos < len(self.tokens):
            return self.tokens[self.current_token_pos]
        return None

    def consume_token(self, token_type, value=None):
        token = self.current_token()
        if token and token.t_type == token_type and (value is None or token.t_vale == value):
            print(f"Consuming token: {token}")
            self.current_token_pos += 1
        else:
            expected = token_type if value is None else f"{token_type} with value '{value}'"
            raise SyntaxError(f"Unexpected token: {token}. Expected {expected}.")

    
    def parse_Expression(self):
        print("Parsing E -> T E'")
        self.parse_Term()
        self.parse_Expression_E()

    # Expression -> + Term followed by Expression | E
    def parse_Expression_E(self):
        token = self.current_token()
        
        # only for + and - 
        if token and token.t_type == TokenType.OPERATOR and token.t_vale in ('+', '-'):
            if token.t_vale == '+':
                print("Parsing E' -> + T E'")
                self.consume_token(TokenType.OPERATOR, '+')
            elif token.t_vale == '-':
                print("Parsing E' -> - T E'")
                self.consume_token(TokenType.OPERATOR, '-')
            
            # Parse the next term after the operator
            self.parse_Term()
            
            # look for more '+' or '-' operators
            self.parse_Expression_E()
        else:
            # No more '+' or '-' operators
            print("Parsing E' -> done")


    # Grammar: T -> F T'
    def parse_Term(self):
        print("Parsing T -> F T'")
        self.parse_Factor()
        self.parse_Term_T()

    # Grammar: T' -> * F T' | Em
    def parse_Term_T(self):
        token = self.current_token()

        # Check if the token is an operator and is either '*' or '/'
        if token and token.t_type == TokenType.OPERATOR and token.t_vale in ('*', '/'):
            if token.t_vale == '*':
                print("Parsing T' -> * F T'")
                self.consume_token(TokenType.OPERATOR, '*')
            elif token.t_vale == '/':
                print("Parsing T' -> / F T'")
                self.consume_token(TokenType.OPERATOR, '/')
            
            # Parse the next factor after the operator
            self.parse_Factor()

            # look for more '*' or '/' operators
            self.parse_Term_T()
        else:
            # No more '*' or '/' operators
            print("Parsing T' -> done")


    # Grammar: F -> ( E ) | id | number
    def parse_Factor(self):
        token = self.current_token()
        if token.t_type == TokenType.PUNCTUATION and token.t_vale == '(':
            print("Parsing F -> ( E )")
            self.consume_token(TokenType.PUNCTUATION, '(')
            self.parse_Expression()
            self.consume_token(TokenType.PUNCTUATION, ')')
        elif token.t_type == TokenType.IDENTIFIER:
            print("Parsing F -> ID")
            self.consume_token(TokenType.IDENTIFIER)
        elif token.t_type == TokenType.NUMBER:
            print("Parsing F -> Number")
            self.consume_token(TokenType.NUMBER)
        else:
            raise SyntaxError(f"Unexpected token in Factor: {token}")

    def parse(self):
        self.parse_Expression()
        # check for remaining tokens
        if self.current_token() is not None:
            raise SyntaxError(f"Unexpected token {self.current_token()}")

