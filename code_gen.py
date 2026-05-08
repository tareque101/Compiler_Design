class CodeGen:
    def generate_asm(self, tac_list):
        asm = []
        for line in tac_list:
            parts = line.split() # Using split() without ' ' handles multiple spaces better
            
            # Handle PRINT: "PRINT t1"
            if parts[0] == 'PRINT':
                asm.append(f"LOAD {parts[1]}")
                asm.append("OUT") # 'OUT' is common for printing the accumulator value
            
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
                
                # Map TAC operators to Assembly Mnemonics
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
                
        return asm