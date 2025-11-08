# semantic_cube.py

class SemanticCube:
    def __init__(self):
        # Tipos: 0 = entero, 1 = flotante, 2 = error
        self.types = {'entero': 0, 'flotante': 1}
        self.operations = {
            '+': 'arithmetic', '-': 'arithmetic', '*': 'arithmetic', '/': 'arithmetic',
            '<': 'relational', '>': 'relational', '==': 'relational', '!=': 'relational',
            '=': 'assignment'
        }
        
        # Cubo semántico: [operando1][operando2][operador] = tipo_resultado
        self.cube = {
            # Operaciones aritméticas
            0: {  # entero
                0: {'+': 0, '-': 0, '*': 0, '/': 0},  # entero op entero = entero
                1: {'+': 1, '-': 1, '*': 1, '/': 1},  # entero op flotante = flotante
            },
            1: {  # flotante
                0: {'+': 1, '-': 1, '*': 1, '/': 1},  # flotante op entero = flotante
                1: {'+': 1, '-': 1, '*': 1, '/': 1},  # flotante op flotante = flotante
            },
        }
        
        # Cubo para operaciones relacionales (siempre retornan entero como booleano)
        relational_cube = {0: 0, 1: 0}  # entero = 0, flotante = 0 (resultado)
        for op in ['<', '>', '==', '!=']:
            for t1 in [0, 1]:
                self.cube[t1] = self.cube.get(t1, {})
                for t2 in [0, 1]:
                    self.cube[t1][t2] = self.cube[t1].get(t2, {})
                    self.cube[t1][t2][op] = 0  # resultado entero (booleano)
        
        # Cubo para asignación
        for t1 in [0, 1]:
            self.cube[t1] = self.cube.get(t1, {})
            for t2 in [0, 1]:
                self.cube[t1][t2] = self.cube[t1].get(t2, {})
                if t1 == t2:  # misma tipo
                    self.cube[t1][t2]['='] = t1
                elif t1 == 0 and t2 == 1:  # entero = flotante (permitido con conversión)
                    self.cube[t1][t2]['='] = 0
                else:  # flotante = entero (no permitido sin conversión explícita)
                    self.cube[t1][t2]['='] = 2  # error
    
    def get_result_type(self, left_type, right_type, operator):
        """Obtiene el tipo resultante de una operación"""
        left_code = self.types.get(left_type, 2)  # 2 = error
        right_code = self.types.get(right_type, 2)
        
        if left_code == 2 or right_code == 2:
            return 'error'
        
        try:
            result_code = self.cube[left_code][right_code][operator]
            if result_code == 2:
                return 'error'
            # Convertir código a nombre de tipo
            for name, code in self.types.items():
                if code == result_code:
                    return name
        except KeyError:
            return 'error'
    
    def is_operation_valid(self, left_type, right_type, operator):
        """Verifica si una operación es válida"""
        return self.get_result_type(left_type, right_type, operator) != 'error'

semantic_cube = SemanticCube()