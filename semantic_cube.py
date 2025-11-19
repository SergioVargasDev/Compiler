# semantic_cube.py

class SemanticCube:
    def __init__(self):
        # Tipos: 0 = entero, 1 = flotante, 2 = bool, 3 = error
        self.types = {'entero': 0, 'flotante': 1, 'bool': 2}
        
        # Cubo semántico: [operando1][operando2][operador] = tipo_resultado
        self.cube = {
            # entero
            0: {
                # entero op entero
                0: {
                    '+': 0, '-': 0, '*': 0, '/': 0, '%': 0,  # aritméticas
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,  # relacionales
                    '=': 0,  # asignación
                    '&&': 3, '||': 3  # error para booleanas
                },
                # entero op flotante
                1: {
                    '+': 1, '-': 1, '*': 1, '/': 1, '%': 3,  # aritméticas
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,  # relacionales
                    '=': 0,  # asignación con conversión
                    '&&': 3, '||': 3  # error para booleanas
                },
                # entero op bool
                2: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,  # error aritméticas
                    '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3,  # error relacionales
                    '=': 3,  # error asignación
                    '&&': 3, '||': 3  # error para booleanas
                }
            },
            # flotante
            1: {
                # flotante op entero
                0: {
                    '+': 1, '-': 1, '*': 1, '/': 1, '%': 3,  # aritméticas
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,  # relacionales
                    '=': 3,  # error asignación
                    '&&': 3, '||': 3  # error para booleanas
                },
                # flotante op flotante
                1: {
                    '+': 1, '-': 1, '*': 1, '/': 1, '%': 3,  # aritméticas
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,  # relacionales
                    '=': 1,  # asignación
                    '&&': 3, '||': 3  # error para booleanas
                },
                # flotante op bool
                2: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,  # error aritméticas
                    '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3,  # error relacionales
                    '=': 3,  # error asignación
                    '&&': 3, '||': 3  # error para booleanas
                }
            },
            # bool
            2: {
                # bool op entero
                0: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,  # error aritméticas
                    '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3,  # error relacionales
                    '=': 3,  # error asignación
                    '&&': 3, '||': 3  # error para booleanas
                },
                # bool op flotante
                1: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,  # error aritméticas
                    '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3,  # error relacionales
                    '=': 3,  # error asignación
                    '&&': 3, '||': 3  # error para booleanas
                },
                # bool op bool
                2: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,  # error aritméticas
                    '>': 3, '<': 3, '==': 2, '!=': 2, '>=': 3, '<=': 3,  # relacionales
                    '=': 2,  # asignación
                    '&&': 2, '||': 2  # booleanas
                }
            }
        }
        
        # Operador unario !
        self.unary_operations = {
            2: {'!': 2}  # bool -> bool
        }
    
    def get_result_type(self, left_type, right_type, operator):
        """Obtiene el tipo resultante de una operación"""
        left_code = self.types.get(left_type, 3)  # 3 = error
        right_code = self.types.get(right_type, 3)
        
        if left_code == 3 or right_code == 3:
            return 'error'
        
        try:
            result_code = self.cube[left_code][right_code][operator]
            if result_code == 3:
                return 'error'
            # Convertir código a nombre de tipo
            for name, code in self.types.items():
                if code == result_code:
                    return name
            return 'error'
        except KeyError:
            return 'error'
    
    def get_unary_result_type(self, operand_type, operator):
        """Obtiene el tipo resultante de una operación unaria"""
        operand_code = self.types.get(operand_type, 3)
        
        if operand_code == 3:
            return 'error'
        
        try:
            result_code = self.unary_operations[operand_code][operator]
            for name, code in self.types.items():
                if code == result_code:
                    return name
            return 'error'
        except KeyError:
            return 'error'
    
    def is_operation_valid(self, left_type, right_type, operator):
        """Verifica si una operación binaria es válida"""
        return self.get_result_type(left_type, right_type, operator) != 'error'
    
    def is_unary_operation_valid(self, operand_type, operator):
        """Verifica si una operación unaria es válida"""
        return self.get_unary_result_type(operand_type, operator) != 'error'

semantic_cube = SemanticCube()