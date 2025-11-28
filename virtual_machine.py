# virtual_machine.py
from memory_manager import memory_manager
import sys

class MemoryMap:
    def __init__(self):
        self.global_memory = {}
        self.constant_memory = {}
        self.local_memory_stack = [] # Stack of local memories (for function calls)
        self.temp_memory_stack = []  # Stack of temp memories (if temps are local)
        
        # Initialize global memory (could be pre-allocated or dynamic)
        self.global_memory = {}
        
        # Current local memory (top of stack)
        self.local_memory = {}
        self.temp_memory = {}
        
    def get_value(self, address):
        # Determine memory segment based on address ranges from memory_manager
        if address >= memory_manager.CONST_INT_START:
            return self.constant_memory.get(address)
        elif address >= memory_manager.TEMP_INT_START:
            # Check if we are in a function (stack not empty)
            if self.temp_memory_stack:
                return self.temp_memory_stack[-1].get(address)
            return self.temp_memory.get(address) # Fallback or global temps?
        elif address >= memory_manager.LOCAL_INT_START:
            if self.local_memory_stack:
                return self.local_memory_stack[-1].get(address)
            return self.local_memory.get(address)
        elif address >= memory_manager.GLOBAL_INT_START:
            val = self.global_memory.get(address)
            # if val is None: print(f"[DEBUG] Read Global {address}: None")
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
            # print(f"[DEBUG] Write Global {address} = {value}")
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
            # key is "value_type", e.g. "10_entero"
            value_str = key.rsplit('_', 1)[0]
            type_str = key.rsplit('_', 1)[1]
            
            if type_str in ['entero', 'int']:
                value = int(value_str)
            elif type_str in ['flotante', 'float']:
                value = float(value_str)
            else:
                value = value_str.strip('"') # Remove quotes for strings
                
            self.constant_memory[address] = value

class VirtualMachine:
    def __init__(self, quadruples, constants_table):
        self.quadruples = quadruples
        self.memory = MemoryMap()
        self.memory.load_constants(constants_table)
        self.instruction_pointer = 0
        self.call_stack = [] # To store return IPs
        self.pending_stack = [] # Stack of pending activation records for nested calls

    def run(self, debug=False):
        # print("=== INICIANDO EJECUCIÓN VM ===")
        while self.instruction_pointer < len(self.quadruples):
            quad = self.quadruples[self.instruction_pointer]
            
            if debug:
                print(f"[VM-STEP] IP={self.instruction_pointer} | {quad}")
                # Opcional: Imprimir memoria relevante si se desea
            
            op = quad.operator
            left = quad.left_operand
            right = quad.right_operand
            res = quad.result
            
            # print(f"Exec: {self.instruction_pointer}: {quad}") # Debug
            # print(f"Exec: {self.instruction_pointer}: {op} {left} {right} {res}")
            
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
                # Crear nueva memoria local y ponerla en pila de pendientes
                self.pending_stack.append({})
                self.instruction_pointer += 1
                
            elif op == 'PARAM':
                value = self.memory.get_value(left)
                dest_addr = int(res)
                # Escribir en la memoria pendiente más reciente (tope de pila)
                if not self.pending_stack:
                    raise Exception("PARAM without ERA")
                self.pending_stack[-1][dest_addr] = value
                self.instruction_pointer += 1
                
            elif op == 'GOSUB':
                self.call_stack.append(self.instruction_pointer + 1)
                self.instruction_pointer = int(res)
                
                # Mover memoria pendiente a memoria activa
                if not self.pending_stack:
                    raise Exception("GOSUB without ERA")
                new_local_memory = self.pending_stack.pop()
                
                # Empujar a la pila de memoria de ejecución
                self.memory.local_memory_stack.append(new_local_memory)
                self.memory.temp_memory_stack.append({}) # Nueva memoria temporal para la función
                
            elif op == 'ENDFUNC':
                self.memory.pop_local_memory()
                self.instruction_pointer = self.call_stack.pop()
                
            elif op == 'RET':
                # RET no hace nada en esta implementación porque el valor ya se asignó
                # a la variable global de retorno antes de generar RET (si hubiera)
                # O si RET tiene operando, se asignaría aquí.
                # En mi parser, la asignación se hace antes.
                self.instruction_pointer += 1
                
            else:
                raise Exception(f"Unknown opcode: {op}")

