import re

TOKEN_SPEC = [
    # Updated: Supports integers (10) and floats (10.5)
    ('NUMBER',   r'\d+(\.\d+)?'), 
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN',   r'='),
    ('OP',       r'[+\-*/]'),
    ('SEMI',     r';'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('COMMENT',  r'#.*'),
    ('SKIP',     r'[ \t\n\r]+'),
    ('MISMATCH', r'.'),
]

class Lexer:
    # --- UPDATED KEYWORD LIST ---
    # Added common types and control structures
    KEYWORDS = {
        'int', 'float', 'char', 'bool', 
        'if', 'else', 'while', 'for', 
        'print', 'true', 'false', 'return'
    }

    def __init__(self, code):
        self.tokens = []
        self.errors = []
        self.tokenize(code)

    def tokenize(self, code):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
        
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            
            if kind == 'NUMBER':
                # Convert to float if '.' exists, otherwise int
                num_value = float(value) if '.' in value else int(value)
                self.tokens.append(('NUMBER', num_value))
                
            elif kind == 'ID':
                # Check against the expanded KEYWORD set
                if value in self.KEYWORDS:
                    self.tokens.append(('KEYWORD', value))
                else:
                    self.tokens.append(('ID', value))
                    
            elif kind == 'COMMENT' or kind == 'SKIP':
                continue
                
            elif kind == 'MISMATCH':
                self.errors.append(f"Lexical Error: Unexpected character '{value}'")
                
            else:
                self.tokens.append((kind, value))
        
        self.tokens.append(('EOF', None))
        return self.tokens