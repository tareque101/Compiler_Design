import os
from lexer import Lexer
from parser_ast import Parser
from semantic_analyzer import SemanticAnalyzer
from optimizer import Optimizer
from icg import ICG
from code_gen import CodeGen

class AssemblyVM:
    def __init__(self):
        self.memory = {}
        self.accumulator = 0

    def _get_val(self, target):
        try:
            if '.' in target: return float(target)
            return int(target)
        except ValueError:
            return self.memory.get(target, 0)

    def execute(self, asm_instructions):
        print("\n--- RUNTIME LIVE EXECUTION OUTPUT ---")
        for line in asm_instructions:
            parts = line.split()
            if not parts: continue
            cmd = parts[0]
            
            if cmd == "LOAD":
                self.accumulator = self._get_val(parts[1])
            elif cmd == "STORE":
                self.memory[parts[1]] = self.accumulator
            elif cmd == "ADD":
                self.accumulator += self._get_val(parts[1])
            elif cmd == "SUB":
                self.accumulator -= self._get_val(parts[1])
            elif cmd == "MUL":
                self.accumulator *= self._get_val(parts[1])
            elif cmd == "DIV":
                divisor = self._get_val(parts[1])
                self.accumulator = (self.accumulator // divisor) if divisor != 0 else 0
            elif cmd == "OUT":
                print(f"[ASM OUT]: {self.accumulator}")
        print("-" * 37)

# --- NEW HELPER: Scans the AST for any PRINT nodes ---
def contains_print(ast_nodes):
    for node in ast_nodes:
        if node[0] == 'PRINT':
            return True
        if node[0] == 'BLOCK' and contains_print(node[1]):
            return True
    return False

def compile_code(input_data):
    if os.path.exists(input_data) and input_data.endswith('.txt'):
        with open(input_data, "r") as f:
            source_code = f.read()
    else:
        source_code = input_data

    lexer = Lexer(source_code)
    parser = Parser(lexer.tokens)
    ast = parser.parse()
     
    semantic = SemanticAnalyzer()
    sem_errors = semantic.check(ast)
    
    all_errors = lexer.errors + parser.errors + sem_errors
    if all_errors:
        print("\n[!] COMPILATION ERRORS:")
        for err in all_errors: 
            print(f" -> {err}")
        return
 
    optimizer = Optimizer()
    opt_ast = optimizer.optimize(ast)

    icg = ICG()
    tac = icg.generate(opt_ast)

    codegen = CodeGen()
    asm = codegen.generate_asm(tac)

    # --- FIXED: Only print output if a PRINT function exists in the code ---
    if contains_print(ast):
        print("\n" + "="*30)
        print(" COMPILATION SUCCESSFUL ")
        print("="*30)

        if tac:
            print("\n--- THREE ADDRESS CODE (TAC) ---")
            for line in tac: 
                print(f"  {line}")
            
        if asm:
            print("\n--- TARGET ASSEMBLY (Simple ASM) ---")
            for line in asm: 
                print(f"  {line}")
        print("="*30 + "\n")

        if asm:
            vm = AssemblyVM()
            vm.execute(asm)
    else:
        # No print function found -> Remain completely silent
        pass

if __name__ == "__main__":
    # Test code with print
    test_code = "int x = 5 + 5; { print(x); }"
    compile_code(test_code)