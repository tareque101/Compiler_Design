class ICG:
    def __init__(self):
        self.tac = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast):
        for node in ast:
            node_type = node[0]

            if node_type == 'ASSIGN':
                # x = expression
                res = self.gen_expr(node[2])
                self.tac.append(f"{node[1]} = {res}")

            elif node_type == 'DECL_ASSIGN':
                # int x = expression
                res = self.gen_expr(node[2])
                self.tac.append(f"{node[1]} = {res}")

            elif node_type == 'PRINT':
                # print(expression)
                res = self.gen_expr(node[1])
                self.tac.append(f"PRINT {res}")

            elif node_type == 'BLOCK':
                # Recursively generate TAC for statements inside { ... }
                self.generate(node[1])

            elif node_type == 'DECL':
                # For basic 'int x;', TAC often ignores it or uses 'alloc'
                pass 

        return self.tac

    def gen_expr(self, expr):
        # If it's a constant or variable (not a tuple)
        if not isinstance(expr, tuple):
            return expr
        
        # If it's a BINOP (t1 = a + b)
        if expr[0] == 'BINOP':
            op = expr[1]
            left = self.gen_expr(expr[2])
            right = self.gen_expr(expr[3])
            temp = self.new_temp()
            self.tac.append(f"{temp} = {left} {op} {right}")
            return temp
            
        return expr