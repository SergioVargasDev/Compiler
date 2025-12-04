class SemanticCube:
    def __init__(self):
        self.types = {'entero': 0, 'flotante': 1, 'bool': 2}
        
        self.cube = {
            # OPERANDO IZQUIERDO: ENTERO (0)
            0: {
                # entero op entero
                0: {
                    '+': 0, '-': 0, '*': 0, '/': 0, '%': 0,
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,
                    '=': 0,
                    '&&': 3, '||': 3
                },
                # entero op flotante
                1: {
                    '+': 1, '-': 1, '*': 1, '/': 1, '%': 3,
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,
                    '=': 0,  # Asignación (int = float) -> Trunca a entero
                    '&&': 3, '||': 3
                },
                # entero op bool
                2: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,
                    '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3,
                    '=': 3,
                    '&&': 3, '||': 3
                }
            },
            # OPERANDO IZQUIERDO: FLOTANTE (1)
            1: {
                # flotante op entero
                0: {
                    '+': 1, '-': 1, '*': 1, '/': 1, '%': 3,
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,
                    # CORRECCIÓN APLICADA:
                    # Permitimos asignar entero a flotante. El resultado es flotante (1).
                    '=': 1,  
                    '&&': 3, '||': 3
                },
                # flotante op flotante
                1: {
                    '+': 1, '-': 1, '*': 1, '/': 1, '%': 3,
                    '>': 2, '<': 2, '==': 2, '!=': 2, '>=': 2, '<=': 2,
                    '=': 1,
                    '&&': 3, '||': 3
                },
                # flotante op bool
                2: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,
                    '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3,
                    '=': 3,
                    '&&': 3, '||': 3
                }
            },
            # OPERANDO IZQUIERDO: BOOL (2)
            2: {
                # bool op entero
                0: { '+': 3, '-': 3, '*': 3, '/': 3, '%': 3, '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3, '=': 3, '&&': 3, '||': 3 },
                # bool op flotante
                1: { '+': 3, '-': 3, '*': 3, '/': 3, '%': 3, '>': 3, '<': 3, '==': 3, '!=': 3, '>=': 3, '<=': 3, '=': 3, '&&': 3, '||': 3 },
                # bool op bool
                2: {
                    '+': 3, '-': 3, '*': 3, '/': 3, '%': 3,
                    '>': 3, '<': 3, '==': 2, '!=': 2, '>=': 3, '<=': 3,
                    '=': 2,
                    '&&': 2, '||': 2
                }
            }
        }
        
        self.unary_operations = {
            2: {'!': 2}
        }
    
    def get_result_type(self, left_type, right_type, operator):
        left_code = self.types.get(left_type, 3)
        right_code = self.types.get(right_type, 3)
        
        if left_code == 3 or right_code == 3:
            return 'error'
        
        try:
            result_code = self.cube[left_code][right_code][operator]
            if result_code == 3:
                return 'error'
            for name, code in self.types.items():
                if code == result_code:
                    return name
            return 'error'
        except KeyError:
            return 'error'
    
    def get_unary_result_type(self, operand_type, operator):
        operand_code = self.types.get(operand_type, 3)
        if operand_code == 3: return 'error'
        try:
            result_code = self.unary_operations[operand_code][operator]
            for name, code in self.types.items():
                if code == result_code: 
                    return name
            return 'error'
        except KeyError:
            return 'error'

semantic_cube = SemanticCube()

if __name__ == "__main__":
    print("=== TESTEANDO CUBO SEMÁNTICO ===")
    
    def probar(desc, izq, der, op, esperado):
        resultado = semantic_cube.get_result_type(izq, der, op)
        status = "OK" if resultado == esperado else f"FALLÓ (Obtuve: {resultado})"
        print(f"{desc:<35} | {izq} {op} {der} -> {resultado} \t{status}")

    def probar_unario(desc, op, tipo, esperado):
        resultado = semantic_cube.get_unary_result_type(tipo, op)
        status = "OK" if resultado == esperado else f"FALLÓ (Obtuve: {resultado})"
        print(f"{desc:<35} | {op}{tipo} -> {resultado} \t{status}")

    print("\n--- 1. Aritmética Básica ---")
    probar("Suma Enteros", "entero", "entero", "+", "entero")
    probar("Resta Flotantes", "flotante", "flotante", "-", "flotante")
    probar("Mult Mixta (Promoción)", "entero", "flotante", "*", "flotante")

    print("\n--- 2. Comparaciones (Relacionales) ---")
    probar("Mayor que", "entero", "entero", ">", "bool")
    probar("Igualdad mixta", "entero", "flotante", "==", "bool")
    probar("Comparar Bool (Válido)", "bool", "bool", "==", "bool")

    print("\n--- 3. Asignación (Tus Reglas Especiales) ---")
    probar("Asignar Int a Float", "flotante", "entero", "=", "flotante")
    
    probar("Asignar Float a Int", "entero", "flotante", "=", "entero")

    print("\n--- 4. Casos de Error (Lo que debe fallar) ---")
    probar("Sumar Entero + Bool", "entero", "bool", "+", "error")
    probar("Comparar Bool > Entero", "bool", "entero", ">", "error")
    probar("Operador Inexistente", "entero", "entero", "@", "error")
    probar("Tipo Desconocido", "entero", "marciano", "+", "error")
    
    probar("Operar con Letrero", "entero", "letrero", "+", "error") 

    print("\n--- 5. Operaciones Unarias ---")
    probar_unario("Not Booleano", "!", "bool", "bool")
    probar_unario("Not Entero (Debe fallar)", "!", "entero", "error")