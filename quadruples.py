from memory_manager import memory_manager
from semantic_cube import semantic_cube


class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
    
    def __str__(self):
        return f"({self.operator}, {self.left_operand}, {self.right_operand}, {self.result})"
    
    def __repr__(self):
        return self.__str__()

class QuadrupleManager:
    def __init__(self):
        self.quadruples = []
        self.operators_stack = []
        self.operands_stack = []
        self.types_stack = []
        self.jump_stack = []
        self.temp_counter = 0
        self.goto_main_index = None

    def next_quad(self):
        return len(self.quadruples)
    
    def new_temp(self, temp_type='entero'):
        self.temp_counter += 1
        return memory_manager.get_temp_address(temp_type)
    
    def push_operand(self, operand, type_):
        if isinstance(operand, int) or isinstance(operand, float):
            const_type = 'entero' if isinstance(operand, int) else 'flotante'
            address = memory_manager.get_constant_address(operand, const_type)
            self.push_address(address, const_type)
        else:
            raise Exception(f"Error: push_operand recibió '{operand}'. Usa push_address para variables.")
    
    def push_address(self, address, type_):
        self.operands_stack.append(address)
        self.types_stack.append(type_)

    def push_operator(self, operator):
        self.operators_stack.append(operator)
    
    def generate_quadruple(self):
        if len(self.operators_stack) == 0 or len(self.operands_stack) < 2:
            return
        
        operator = self.operators_stack.pop()
        right_operand = self.operands_stack.pop()
        right_type = self.types_stack.pop()
        left_operand = self.operands_stack.pop()
        left_type = self.types_stack.pop()
        
        result_type = self.get_result_type(left_type, right_type, operator)
        if result_type == 'error':
            raise Exception(f"Error Semántico: {left_type} {operator} {right_type}")

        result_address = self.new_temp(result_type)
        
        quad = Quadruple(operator, left_operand, right_operand, result_address)
        self.quadruples.append(quad)
        
        self.push_address(result_address, result_type)
    
    def get_result_type(self, left_type, right_type, operator):
        return semantic_cube.get_result_type(left_type, right_type, operator)
    
    def add_quadruple(self, operator, left_operand, right_operand, result):
        quad = Quadruple(operator, left_operand, right_operand, result)
        self.quadruples.append(quad)
        return len(self.quadruples) - 1

    def add_era(self, func_name):
        self.add_quadruple('ERA', func_name, '', '')

    def add_param(self, argument_address, destination_address):
        self.add_quadruple('PARAM', argument_address, '', destination_address)

    def add_gosub(self, func_name, start_quad):
        self.add_quadruple('GOSUB', func_name, '', start_quad)

    def add_endfunc(self):
        self.add_quadruple('ENDFUNC', '', '', '')
    
    def add_return(self, value_address):
        self.add_quadruple('RET', value_address, '', '')
    
    def push_jump(self, quad_index):
        self.jump_stack.append(quad_index)

    def patch(self, quad_index, new_result):
        if quad_index is not None and quad_index < len(self.quadruples):
            self.quadruples[quad_index].result = new_result
    
    def pop_jump(self):
        return self.jump_stack.pop() if self.jump_stack else None
    
    def complete_patching(self):
        for i, quad in enumerate(self.quadruples):
            if quad.operator in ['goto', 'gotof'] and quad.result == '':
                quad.result = str(len(self.quadruples))
    
    def print_quadruples(self):
        print("\n=== CUÁDRUPLOS (Direcciones Reales) ===")
        print("-" * 40)
        for i, quad in enumerate(self.quadruples):
            print(f"{i:<4} {str(quad.operator):<8} {str(quad.left_operand):<8} {str(quad.right_operand):<8} {str(quad.result):<8}")
    
    def clear(self):
        self.quadruples.clear()
        self.operators_stack.clear()
        self.operands_stack.clear()
        self.types_stack.clear()
        self.jump_stack.clear()
        self.temp_counter = 0
        self.goto_main_index = None

quadruple_manager = QuadrupleManager()