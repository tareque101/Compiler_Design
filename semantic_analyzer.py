class SemanticAnalyzer:
    def __init__(self):
        # Stack of dictionaries for nested scopes
        # Each dictionary represents one scope level
        self.scopes = [{}] 
        self.errors = []

    def current_scope(self):
        return self.scopes[-1]

    def is_declared(self, name):
        # Search from the innermost scope outward to the global scope
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False

    def check(self, ast):
        for node in ast:
            node_type = node[0]

            if node_type == 'DECL':
                name = node[1]
                if name in self.current_scope():
                    self.errors.append(f"Semantic Error: Variable '{name}' already declared in this scope")
                else:
                    self.current_scope()[name] = 'int' # Assuming 'int' for now

            elif node_type == 'DECL_ASSIGN':
                name = node[1]
                expr = node[2]
                if name in self.current_scope():
                    self.errors.append(f"Semantic Error: Variable '{name}' already declared in this scope")
                else:
                    self.current_scope()[name] = 'int'
                self.check_expr(expr)

            elif node_type == 'ASSIGN':
                name = node[1]
                expr = node[2]
                if not self.is_declared(name):
                    self.errors.append(f"Semantic Error: Variable '{name}' not declared")
                self.check_expr(expr)

            elif node_type == 'PRINT':
                self.check_expr(node[1])

            elif node_type == 'BLOCK':
                # Enter new scope
                self.scopes.append({})
                self.check(node[1]) # Recursively check statements inside block
                self.scopes.pop() # Exit scope

        return self.errors

    def check_expr(self, expr):
        # If expression is a binary operation (tuple)
        if isinstance(expr, tuple) and expr[0] == 'BINOP':
            self.check_expr(expr[2]) # Left side
            self.check_expr(expr[3]) # Right side
        
        # If expression is a variable (string and not a digit)
        elif isinstance(expr, str) and not expr.isdigit():
            if not self.is_declared(expr):
                self.errors.append(f"Semantic Error: Variable '{expr}' not declared")