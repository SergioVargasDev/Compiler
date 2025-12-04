from memory_manager import memory_manager
import sys

class MemoryMap:
    def __init__(self):
        self.global_memory = {}
        self.constant_memory = {}
        self.local_memory_stack = [] 
        self.temp_memory_stack = [] 
        
        self.global_memory = {}
        
        self.local_memory = {}
        self.temp_memory = {}
        
    def get_value(self, address):
        if address >= memory_manager.CONST_INT_START:
            return self.constant_memory.get(address)
        elif address >= memory_manager.TEMP_INT_START:
            if self.temp_memory_stack:
                return self.temp_memory_stack[-1].get(address)
            return self.temp_memory.get(address) 
        elif address >= memory_manager.LOCAL_INT_START:
            if self.local_memory_stack:
                return self.local_memory_stack[-1].get(address)
            return self.local_memory.get(address)
        elif address >= memory_manager.GLOBAL_INT_START:
            val = self.global_memory.get(address)
            return val
        else:
            raise Exception(f"Segmentation Fault: Address {address} out of bounds")

    def set_value(self, address, value):
        if address >= memory_manager.CONST_INT_START:
            raise Exception("Segmentation Fault: Cannot write to Read-Only Memory (Constants)")
        elif address >= memory_manager.TEMP_INT_START:
            if self.temp_memory_stack:
                self.temp_memory_stack[-1][address] = value
            else:
                self.temp_memory[address] = value
        elif address >= memory_manager.LOCAL_INT_START:
            if self.local_memory_stack:
                self.local_memory_stack[-1][address] = value
            else:
                self.local_memory[address] = value
        elif address >= memory_manager.GLOBAL_INT_START:
            self.global_memory[address] = value
        else:
            raise Exception(f"Segmentation Fault: Address {address} out of bounds")

    def push_local_memory(self):
        self.local_memory_stack.append({})
        self.temp_memory_stack.append({})

    def pop_local_memory(self):
        if self.local_memory_stack:
            self.local_memory_stack.pop()
            self.temp_memory_stack.pop()

    def load_constants(self, constants_table):
        for key, address in constants_table.items():
            value_str = key.rsplit('_', 1)[0]
            type_str = key.rsplit('_', 1)[1]
            
            if type_str in ['entero', 'int']:
                value = int(value_str)
            elif type_str in ['flotante', 'float']:
                value = float(value_str)
            else:
                value = value_str.strip('"') 
                
            self.constant_memory[address] = value

class VirtualMachine:
    def __init__(self, quadruples, constants_table):
        self.quadruples = quadruples
        self.memory = MemoryMap()
        self.memory.load_constants(constants_table)
        self.instruction_pointer = 0
        self.call_stack = [] 
        self.pending_stack = []
    def run(self, debug=False):
        while self.instruction_pointer < len(self.quadruples):
            quad = self.quadruples[self.instruction_pointer]
            
            if debug:
                print(f"[VM-STEP] IP={self.instruction_pointer} | {quad}")
            
            op = quad.operator
            left = quad.left_operand
            right = quad.right_operand
            res = quad.result
            
           
            
            if op == '=':
                value = self.memory.get_value(left)
                if value is None: print(f"WARNING: Get value {left} returned None")
                self.memory.set_value(res, value)
                self.instruction_pointer += 1
                
            elif op == '+':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                if left_val is None: print(f"WARNING: Left {left} is None")
                if right_val is None: print(f"WARNING: Right {right} is None")
                self.memory.set_value(res, left_val + right_val)
                self.instruction_pointer += 1
                
            elif op == '-':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val - right_val)
                self.instruction_pointer += 1
                
            elif op == '*':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val * right_val)
                self.instruction_pointer += 1
                
            elif op == '/':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                if right_val == 0:
                    raise Exception("Division by Zero")
                self.memory.set_value(res, left_val / right_val)
                self.instruction_pointer += 1
                
            elif op == '<':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val < right_val)
                self.instruction_pointer += 1
                
            elif op == '>':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val > right_val)
                self.instruction_pointer += 1

            elif op == '==':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val == right_val)
                self.instruction_pointer += 1

            elif op == '!=':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val != right_val)
                self.instruction_pointer += 1

            elif op == '<=':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val <= right_val)
                self.instruction_pointer += 1

            elif op == '>=':
                left_val = self.memory.get_value(left)
                right_val = self.memory.get_value(right)
                self.memory.set_value(res, left_val >= right_val)
                self.instruction_pointer += 1
                self.memory.set_value(res, left_val > right_val)
                self.instruction_pointer += 1
                
            elif op == 'print':
                if isinstance(left, str) and left.startswith('"'):
                    print(left.strip('"'))
                else:
                    value = self.memory.get_value(left)
                    print(value)
                self.instruction_pointer += 1
                
            elif op == 'goto':
                self.instruction_pointer = int(res)
                
            elif op == 'gotof':
                condition = self.memory.get_value(left)
                if not condition:
                    self.instruction_pointer = int(res)
                else:
                    self.instruction_pointer += 1
                    
            elif op == 'ERA':
                self.pending_stack.append({})
                self.instruction_pointer += 1
                
            elif op == 'PARAM':
                value = self.memory.get_value(left)
                dest_addr = int(res)
                if not self.pending_stack:
                    raise Exception("PARAM without ERA")
                self.pending_stack[-1][dest_addr] = value
                self.instruction_pointer += 1
                
            elif op == 'GOSUB':
                self.call_stack.append(self.instruction_pointer + 1)
                self.instruction_pointer = int(res)
                
                if not self.pending_stack:
                    raise Exception("GOSUB without ERA")
                new_local_memory = self.pending_stack.pop()
                
                self.memory.local_memory_stack.append(new_local_memory)
                self.memory.temp_memory_stack.append({}) 
                
            elif op == 'ENDFUNC':
                self.memory.pop_local_memory()
                self.instruction_pointer = self.call_stack.pop()
                
            elif op == 'RET':
                self.instruction_pointer += 1
                
            else:
                raise Exception(f"Unknown opcode: {op}")

