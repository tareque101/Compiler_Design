from main import compile_code

print("=== Mini Compiler REPL ===")
print("Type 'exit' to quit. Type 'RUN' on a new line to compile multi-line blocks.")
print("---------------------------")

buffer = []

while True:
    try:
        # Prompt changes if we are inside a multi-line block
        prompt = ".. " if buffer else ">> "
        line = input(prompt)

        if line.lower() == 'exit':
            break
        
        # If user types 'RUN', we compile everything in the buffer
        if line.strip().upper() == 'RUN':
            if buffer:
                full_code = "\n".join(buffer)
                print("\n--- Compiling ---")
                compile_code(full_code)
                print("-----------------\n")
                buffer = [] # Clear buffer after run
            continue

        # Basic single-line execution for simple commands
        if not buffer and not line.strip().endswith('{'):
            if line.strip():
                compile_code(line)
            continue
        
        # Otherwise, add to buffer (for blocks or multi-line logic)
        buffer.append(line)
        
        # Auto-run if braces are balanced and not empty (optional quality of life)
        if line.strip() == '}':
            # Check if braces are balanced
            full_code = "\n".join(buffer)
            if full_code.count('{') == full_code.count('}'):
                print("\n--- Compiling Block ---")
                compile_code(full_code)
                print("-----------------------\n")
                buffer = []

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"REPL Error: {e}")
        buffer = [] # Clear buffer on error to reset state