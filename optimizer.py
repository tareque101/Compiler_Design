class Optimizer:
    def fold_constants(self, expr):
        # Base case: if it's not a BINOP tuple, try to return it as an int if possible
        if not isinstance(expr, tuple) or expr[0] != 'BINOP':
            try:
                # If the string is a pure number, convert it to int for calculation
                if isinstance(expr, str) and expr.isdigit():
                    return int(expr)
                return expr
            except:
                return expr
        
        op = expr[1]
        left = self.fold_constants(expr[2])
        right = self.fold_constants(expr[3])
        
        # If both sides are now integers, fold them!
        if isinstance(left, int) and isinstance(right, int):
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left // right if right != 0 else 0
            
        return ('BINOP', op, left, right)

    def optimize(self, ast):
        optimized_ast = []
        for node in ast:
            node_type = node[0]

            if node_type == 'ASSIGN':
                # a = 2 + 3 -> a = 5
                optimized_ast.append(('ASSIGN', node[1], self.fold_constants(node[2])))

            elif node_type == 'DECL_ASSIGN':
                # int a = 2 + 3 -> int a = 5
                optimized_ast.append(('DECL_ASSIGN', node[1], self.fold_constants(node[2])))

            elif node_type == 'PRINT':
                # print(2 + 3) -> print(5)
                optimized_ast.append(('PRINT', self.fold_constants(node[1])))

            elif node_type == 'BLOCK':
                # Recursively optimize statements inside { ... }
                optimized_ast.append(('BLOCK', self.optimize(node[1])))

            else:
                # Keep 'DECL' or other nodes as they are
                optimized_ast.append(node)
                
        return optimized_ast