class CodeGen:
    def generate_asm(self, tac_list):
        asm = []
        for line in tac_list:
            parts = line.split() 
            if not parts:
                continue
            
            # Handle PRINT: "PRINT t1"
            if parts[0] == 'PRINT':
                asm.append(f"LOAD {parts[1]}")
                asm.append("OUT")
            
            # Handle Simple Assignment: "a = 5" or "a = t1"
            elif len(parts) == 3 and parts[1] == '=':
                asm.append(f"LOAD {parts[2]}")
                asm.append(f"STORE {parts[0]}")
            
            # Handle Binary Operations: "t1 = a + b"
            elif len(parts) == 5 and parts[1] == '=':
                target = parts[0]
                left = parts[2]
                op_char = parts[3]
                right = parts[4]
                
                op_map = {
                    '+': 'ADD',
                    '-': 'SUB',
                    '*': 'MUL',
                    '/': 'DIV'
                }
                
                op_code = op_map.get(op_char, 'UNK')
                
                asm.append(f"LOAD {left}")
                asm.append(f"{op_code} {right}")
                asm.append(f"STORE {target}")
                
        # --- HIGH-FI ADDITION: Low-Level Peephole Optimizer Pass ---
        # Seamlessly filters out redundant instructions without touching your loop
        optimized_asm = []
        for inst in asm:
            if inst.startswith("LOAD ") and optimized_asm:
                prev_inst = optimized_asm[-1]
                var_name = inst[5:] 
                if prev_inst == f"STORE {var_name}":
                    continue # Drops unneeded RAM reload cycle since it's already in CPU
            optimized_asm.append(inst)
                
        return optimized_asm