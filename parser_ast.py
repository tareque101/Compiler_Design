class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def peek(self):
        # Safety check to prevent "list index out of range"
        if self.pos >= len(self.tokens):
            return ('EOF', None)
        return self.tokens[self.pos]

    def consume(self, expected_type=None):
        token = self.peek()
        if expected_type and token[0] != expected_type:
            self.errors.append(f"Syntax Error: Expected {expected_type} but got {token[0]}")
        
        # Move forward only if we haven't hit EOF
        if token[0] != 'EOF':
            self.pos += 1
        return token

    def parse(self):
        nodes = []
        while self.peek()[0] != 'EOF':
            stmt = self.statement()
            if stmt: 
                nodes.append(stmt)
        return nodes

    def statement(self):
        t_type, val = self.peek()
        
        # Bonus: Support for nested blocks { ... }
        if t_type == 'LBRACE':
            return self.block()
        
        # Declaration: int x; OR int x = 10;
        if t_type == 'KEYWORD' and val == 'int':
            return self.declaration()
        
        # Assignment: x = 20;
        if t_type == 'ID':
            return self.assignment()
        
        # Print: print(x);
        if t_type == 'KEYWORD' and val == 'print':
            return self.print_stmt()
        
        # Error recovery
        if t_type != 'EOF':
            self.errors.append(f"Syntax Error: Invalid statement start '{val}'")
            self.consume()
        return None

    def block(self):
        self.consume('LBRACE')
        statements = []
        # Parse until we hit a closing brace or end of file
        while self.peek()[0] != 'RBRACE' and self.peek()[0] != 'EOF':
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        self.consume('RBRACE')
        return ('BLOCK', statements)

    def declaration(self):
        self.consume('KEYWORD')  # Consume 'int'
        name = self.consume('ID')[1]  # Consume the variable name
        
        # Check if there's an immediate assignment (int x = 10;)
        if self.peek()[0] == 'ASSIGN':
            self.consume('ASSIGN')
            expr = self.expression()
            self.consume('SEMI')
            return ('DECL_ASSIGN', name, expr)
        
        # Just a plain declaration (int x;)
        self.consume('SEMI')
        return ('DECL', name)

    def assignment(self):
        name = self.consume('ID')[1]
        self.consume('ASSIGN')
        expr = self.expression()
        self.consume('SEMI')
        return ('ASSIGN', name, expr)

    def print_stmt(self):
        self.consume('KEYWORD') # Consume 'print'
        self.consume('LPAREN')  # Consume '('
        expr = self.expression()
        self.consume('RPAREN')  # Consume ')'
        self.consume('SEMI')
        return ('PRINT', expr)

    def expression(self):
        node = self.term()
        while self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.term()
            node = ('BINOP', op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek()[1] in ('*', '/'):
            op = self.consume()[1]
            right = self.factor()
            node = ('BINOP', op, node, right)
        return node

    def factor(self):
        token = self.peek()
        if token[0] == 'NUMBER' or token[0] == 'ID':
            return self.consume()[1]
        elif token[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.expression()
            self.consume('RPAREN')
            return node
        
        self.errors.append(f"Syntax Error: Expected Number or ID but got {token[0]}")
        self.consume()
        return None