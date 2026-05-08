import os
from lexer import Lexer
from parser_ast import Parser
from semantic_analyzer import SemanticAnalyzer
from optimizer import Optimizer
from icg import ICG
from code_gen import CodeGen

def compile_code(input_data):
    # 1. Input Handling
    if os.path.exists(input_data) and input_data.endswith('.txt'):
        with open(input_data, "r") as f:
            source_code = f.read()
    else:
        source_code = input_data

    # --- 1. LEXICAL ANALYSIS ---
    lexer = Lexer(source_code)
    
    # --- 2. SYNTAX ANALYSIS (Parser) ---
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    
    # --- 3. SEMANTIC ANALYSIS ---
    semantic = SemanticAnalyzer()
    sem_errors = semantic.check(ast)
    
    # Error Collection (Stops compilation if errors are found)
    all_errors = lexer.errors + parser.errors + sem_errors
    if all_errors:
        print("\n[!] COMPILATION ERRORS:")
        for err in all_errors: 
            print(f" -> {err}")
        return

    # --- 4. BONUS: OPTIMIZATION ---
    # We show the original AST vs Optimized AST to prove it works
    optimizer = Optimizer()
    opt_ast = optimizer.optimize(ast)

    # --- 5. INTERMEDIATE CODE GENERATION (TAC) ---
    icg = ICG()
    tac = icg.generate(opt_ast)

    # --- 6. BONUS: TARGET CODE GENERATION (Assembly) ---
    codegen = CodeGen()
    asm = codegen.generate_asm(tac)

    # --- FINAL OUTPUT PRESENTATION ---
    print("\n" + "="*30)
    print(" COMPILATION SUCCESSFUL ")
    print("="*30)

    # Optional: Print AST for debugging/demo
    # print("\n--- ABSTRACT SYNTAX TREE ---")
    # print(opt_ast)

    if tac:
        print("\n--- THREE ADDRESS CODE (TAC) ---")
        for line in tac: 
            print(f"  {line}")
        
    if asm:
        print("\n--- TARGET ASSEMBLY (Simple ASM) ---")
        for line in asm: 
            print(f"  {line}")
    print("="*30 + "\n")

# To allow running main.py directly for testing
if __name__ == "__main__":
    test_code = "int x = 5 + 5; { print(x); }"
    compile_code(test_code)