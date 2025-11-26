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

class TestParser(unittest.TestCase):
    def setUp(self):
        reset_compiler()
        print(f"\n{'-'*60}")
        print(f"Running Parser Test: {self._testMethodName}")
        print(f"{'-'*60}")

    def test_valid_program(self):
        print("[INFO] Probando programa válido básico...")
        code = '''
        programa valid;
        vars
            x : entero;
        inicio
            x = 10;
        fin
        '''
        try:
            parser.parse(code, lexer=lexer)
            print("[SUCCESS] Programa válido analizado correctamente.")
        except Exception as e:
            self.fail(f"Parser raised Exception unexpectedly: {e}")

    def test_nested_structures(self):
        print("[INFO] Probando estructuras anidadas (if dentro de while)...")
        code = '''
        programa nested;
        vars i : entero;
        inicio
            mientras (i > 0) haz {
                si (i == 5) {
                    i = 0;
                } sino {
                    i = i - 1;
                };
            };
        fin
        '''
        try:
            parser.parse(code, lexer=lexer)
            print("[SUCCESS] Estructuras anidadas analizadas correctamente.")
        except Exception as e:
            self.fail(f"Parser failed on nested structures: {e}")

    def test_invalid_syntax_missing_semicolon(self):
        print("[INFO] Probando error de sintaxis (falta punto y coma)...")
        code = '''
        programa invalid;
        vars x : entero
        inicio
            x = 10;
        fin
        '''
        with self.assertRaises(Exception) as cm:
            parser.parse(code, lexer=lexer)
        print(f"[SUCCESS] Error detectado correctamente: {cm.exception}")

    def test_invalid_syntax_bad_expression(self):
        print("[INFO] Probando error de sintaxis (expresión mal formada)...")
        code = '''
        programa invalid;
        inicio
            x = 10 + ; 
        fin
        '''
        with self.assertRaises(Exception) as cm:
            parser.parse(code, lexer=lexer)
        print(f"[SUCCESS] Error detectado correctamente: {cm.exception}")

if __name__ == '__main__':
    unittest.main()
