import unittest
from patito_parser import parser
from patito_lexer import lexer
from symbol_table import function_directory
from quadruples import quadruple_manager
from memory_manager import memory_manager

def reset_compiler():
    function_directory.functions = {}
    function_directory.current_function = 'global'
    function_directory.global_scope.variables = {}
    function_directory.add_function('global', 'nula', [])
    quadruple_manager.clear()
    memory_manager.reset()

class TestSemantic(unittest.TestCase):
    def setUp(self):
        reset_compiler()
        print(f"\n{'-'*60}")
        print(f"Running Semantic Test: {self._testMethodName}")
        print(f"{'-'*60}")

    def test_variable_redeclaration(self):
        print("[INFO] Probando redeclaración de variables...")
        code = '''
        programa test;
        vars
            x : entero;
            x : flotante; /* Error */
        inicio
            x = 10;
        fin
        '''
        with self.assertRaises(Exception) as cm:
            parser.parse(code, lexer=lexer)
        print(f"[SUCCESS] Error detectado correctamente: {cm.exception}")
        self.assertIn("ya declarada", str(cm.exception))

    def test_undeclared_variable(self):
        print("[INFO] Probando variable no declarada...")
        code = '''
        programa test;
        inicio
            y = 10; /* Error */
        fin
        '''
        with self.assertRaises(Exception) as cm:
            parser.parse(code, lexer=lexer)
        print(f"[SUCCESS] Error detectado correctamente: {cm.exception}")
        self.assertIn("no declarada", str(cm.exception))

    def test_type_compatibility(self):
        print("[INFO] Probando compatibilidad de tipos (asignación válida)...")
        code = '''
        programa test;
        vars
            x : entero;
            y : flotante;
        inicio
            x = 10;
            y = 3.14;
            x = y; /* Allowed with conversion */
        fin
        '''
        try:
            parser.parse(code, lexer=lexer)
            print("[SUCCESS] Asignación compatible analizada correctamente.")
        except Exception as e:
            self.fail(f"Semantic check failed unexpectedly: {e}")

    def test_function_argument_mismatch(self):
        print("[INFO] Probando error en argumentos de función (cantidad incorrecta)...")
        code = '''
        programa test;
        nula func(a : entero) { }
        inicio
            func(1, 2); /* Error: espera 1, recibe 2 */
        fin
        '''
        with self.assertRaises(Exception) as cm:
            parser.parse(code, lexer=lexer)
        print(f"[SUCCESS] Error detectado correctamente: {cm.exception}")

    def test_void_function_in_expression(self):
        print("[INFO] Probando uso inválido de función nula en expresión...")
        code = '''
        programa test;
        vars x : entero;
        nula func() { }
        inicio
            x = func() + 1; /* Error */
        fin
        '''
        with self.assertRaises(Exception) as cm:
            parser.parse(code, lexer=lexer)
        print(f"[SUCCESS] Error detectado correctamente: {cm.exception}")

if __name__ == '__main__':
    unittest.main()
