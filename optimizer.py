class Optimizer:
    def fold_constants(self, expr):
        # --- PRESERVED: Your original base case fallback logic ---
        if not isinstance(expr, tuple) or expr[0] != 'BINOP':
            try:
                if isinstance(expr, str) and expr.isdigit():
                    return int(expr)
                return expr
            except:
                return expr
        
        op = expr[1]
        left = self.fold_constants(expr[2])
        right = self.fold_constants(expr[3])
        
        # --- ENHANCEMENT: Handle actual numeric objects from the lexer ---
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left // right if right != 0 else 0
            
        # --- HIGH-FI ADDITION: Algebraic Simplifications ---
        if op == '+':
            if left == 0: return right
            if right == 0: return left
        elif op == '-':
            if right == 0: return left
            if left == right: return 0
        elif op == '*':
            if left == 0 or right == 0: return 0
            if left == 1: return right
            if right == 1: return left
            
        return ('BINOP', op, left, right)

    def optimize(self, ast):
        optimized_ast = []
        for node in ast:
            node_type = node[0]

            if node_type == 'ASSIGN':
                optimized_ast.append(('ASSIGN', node[1], self.fold_constants(node[2])))

            elif node_type == 'DECL_ASSIGN':
                optimized_ast.append(('DECL_ASSIGN', node[1], self.fold_constants(node[2])))

            elif node_type == 'PRINT':
                optimized_ast.append(('PRINT', self.fold_constants(node[1])))

            elif node_type == 'BLOCK':
                optimized_ast.append(('BLOCK', self.optimize(node[1])))

            else:
                optimized_ast.append(node)
                
        return optimized_ast