# quadruples.py
from memory_manager import memory_manager

class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand  # Ahora será dirección virtual
        self.right_operand = right_operand  # Ahora será dirección virtual
        self.result = result  # Ahora será dirección virtual
    
    def __str__(self):
        return f"({self.operator}, {self.left_operand}, {self.right_operand}, {self.result})"
    
    def __repr__(self):
        return self.__str__()

class QuadrupleManager:
    def __init__(self):
        self.quadruples = []  # Fila de cuádruplos
        self.operators_stack = []  # Pila de operadores
        self.operands_stack = []   # Pila de operandos (ahora con direcciones)
        self.types_stack = []      # Pila de tipos
        self.jump_stack = []       # Pila para saltos (para condicionales y ciclos)
        self.temp_counter = 0      # Contador para variables temporales
        
        # Tabla de direcciones para variables, constantes y temporales
        self.address_table = {}
        # Tabla inversa para debugging
        self.address_to_name = {}

    def next_quad(self):
        """Devuelve el número del siguiente cuádruplo"""
        return len(self.quadruples)
        
    def get_variable_address(self, var_name, var_type, scope='global'):
        """Obtiene o crea dirección para variable"""
        if var_name in self.address_table:
            return self.address_table[var_name]
        
        if scope == 'global':
            address = memory_manager.get_global_address(var_type)
        else:
            address = memory_manager.get_local_address(var_type)
        
        self.address_table[var_name] = address
        self.address_to_name[address] = var_name
        return address
    
    def get_constant_address(self, value, const_type):
        """Obtiene dirección para constante"""
        address = memory_manager.get_constant_address(value, const_type)
        # Registrar en tabla de direcciones
        const_name = f"const_{value}"
        self.address_table[const_name] = address
        self.address_to_name[address] = const_name
        return address
    
    def get_temp_address(self, temp_type):
        """Obtiene dirección para temporal"""
        return memory_manager.get_temp_address(temp_type)
    
    def new_temp(self, temp_type='entero'):
        """Genera nueva variable temporal con dirección"""
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        temp_address = self.get_temp_address(temp_type)
        self.address_table[temp_name] = temp_address
        self.address_to_name[temp_address] = temp_name
        return temp_name, temp_address
    
    def push_operand(self, operand, type_):
        """Agrega operando (ahora con dirección) a las pilas"""
        # Si es constante numérica, obtener su dirección
        if isinstance(operand, int) or isinstance(operand, float):
            const_type = 'entero' if isinstance(operand, int) else 'flotante'
            address = self.get_constant_address(str(operand), const_type)
            self.operands_stack.append(address)
            self.types_stack.append(type_)
        # Si es string que representa número
        elif isinstance(operand, str) and (operand.isdigit() or (operand.replace('.', '').isdigit() and operand.count('.') == 1)):
            const_type = 'entero' if operand.isdigit() else 'flotante'
            address = self.get_constant_address(operand, const_type)
            self.operands_stack.append(address)
            self.types_stack.append(type_)
        # Si es variable o temporal, obtener su dirección de la tabla
        elif operand in self.address_table:
            self.operands_stack.append(self.address_table[operand])
            self.types_stack.append(type_)
        else:
            # Es un identificador nuevo - asumir que es variable y crear dirección
            address = self.get_variable_address(operand, type_)
            self.operands_stack.append(address)
            self.types_stack.append(type_)
    
    def push_operator(self, operator):
        """Agrega un operador a la pila"""
        self.operators_stack.append(operator)
    
    def generate_quadruple(self):
        """Genera un cuádruplo a partir de las pilas con direcciones virtuales"""
        if len(self.operators_stack) == 0 or len(self.operands_stack) < 2:
            return
        
        operator = self.operators_stack.pop()
        right_operand = self.operands_stack.pop()
        right_type = self.types_stack.pop()
        left_operand = self.operands_stack.pop()
        left_type = self.types_stack.pop()
        
        # Determinar tipo resultante
        result_type = self.get_result_type(left_type, right_type, operator)
        
        # Generar resultado temporal con dirección
        result_temp, result_address = self.new_temp(result_type)
        
        # Crear y agregar cuádruplo con direcciones virtuales
        quadruple = Quadruple(operator, left_operand, right_operand, result_address)
        self.quadruples.append(quadruple)
        
        # El resultado se convierte en nuevo operando
        self.push_operand(result_temp, result_type)
    
    def get_result_type(self, left_type, right_type, operator):
        """Determina el tipo resultante de una operación"""
        from semantic_cube import semantic_cube
        return semantic_cube.get_result_type(left_type, right_type, operator)
    
    def add_quadruple(self, operator, left_operand, right_operand, result):
        """Agrega un cuádruplo directamente con direcciones virtuales"""
        # Convertir operandos a direcciones si es necesario
        if isinstance(left_operand, str) and left_operand in self.address_table:
            left_operand = self.address_table[left_operand]
        if isinstance(right_operand, str) and right_operand in self.address_table:
            right_operand = self.address_table[right_operand]
        if isinstance(result, str) and result in self.address_table:
            result = self.address_table[result]
        
        quadruple = Quadruple(operator, left_operand, right_operand, result)
        self.quadruples.append(quadruple)
        return len(self.quadruples) - 1  # Retorna el índice del cuádruplo
    
    def patch(self, quad_index, new_result):
        """Parchea un cuádruplo con un nuevo resultado"""
        if quad_index is not None and quad_index < len(self.quadruples):
            self.quadruples[quad_index].result = new_result
    
    def push_jump(self, quad_index):
        """Empuja un salto a la pila"""
        self.jump_stack.append(quad_index)
    
    def pop_jump(self):
        """Saca un salto de la pila"""
        return self.jump_stack.pop() if self.jump_stack else None
    
    def complete_patching(self):
        """Completa el parcheo de todos los GOTOs pendientes"""
        for i, quad in enumerate(self.quadruples):
            if quad.operator in ['goto', 'gotof'] and quad.result == '':
                # Parchear con el final del programa
                quad.result = str(len(self.quadruples))
    
    def print_quadruples(self):
        """Imprime todos los cuádruplos generados con nombres legibles"""
        print("\n=== CUÁDRUPLOS GENERADOS (con direcciones virtuales) ===")
        for i, quad in enumerate(self.quadruples):
            # Convertir direcciones a nombres legibles para display
            left_display = self.address_to_name.get(quad.left_operand, quad.left_operand)
            right_display = self.address_to_name.get(quad.right_operand, quad.right_operand)
            result_display = self.address_to_name.get(quad.result, quad.result)
            
            print(f"{i}: ({quad.operator}, {left_display}, {right_display}, {result_display})")
    
    def print_quadruples_raw(self):
        """Imprime cuádruplos con direcciones numéricas reales"""
        print("\n=== CUÁDRUPLOS GENERADOS (direcciones virtuales crudas) ===")
        for i, quad in enumerate(self.quadruples):
            print(f"{i}: {quad}")
    
    def print_address_table(self):
        """Imprime la tabla de direcciones para debugging"""
        print("\n=== TABLA DE DIRECCIONES VIRTUALES ===")
        for name, address in self.address_table.items():
            print(f"{name}: {address}")
    
    def clear(self):
        """Limpia todas las estructuras"""
        self.quadruples.clear()
        self.operators_stack.clear()
        self.operands_stack.clear()
        self.types_stack.clear()
        self.jump_stack.clear()
        self.temp_counter = 0
        self.address_table.clear()
        self.address_to_name.clear()

# Instancia global del manejador de cuádruplos
quadruple_manager = QuadrupleManager()