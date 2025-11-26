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

class TestQuadruples(unittest.TestCase):
    def setUp(self):
        reset_compiler()
        print(f"\n{'-'*60}")
        print(f"Running Quadruples Test: {self._testMethodName}")
        print(f"{'-'*60}")

    def test_expression_quadruples(self):
        print("[INFO] Probando cuádruplos de expresiones aritméticas...")
        code = '''
        programa test;
        vars
            x, y, z : entero;
        inicio
            x = 1 + 2 * 3;
        fin
        '''
        parser.parse(code, lexer=lexer)
        quads = quadruple_manager.quadruples
        
        print("[INFO] Cuádruplos generados:")
        for i, q in enumerate(quads):
            print(f"  {i}: {q}")
        
        has_mult = any(q.operator == '*' for q in quads)
        self.assertTrue(has_mult, "Debe haber una multiplicación")
        
        has_add = any(q.operator == '+' for q in quads)
        self.assertTrue(has_add, "Debe haber una suma")
        
        has_assign = any(q.operator == '=' for q in quads)
        self.assertTrue(has_assign, "Debe haber una asignación")
        print("[SUCCESS] Cuádruplos de expresión verificados.")

    def test_control_flow_quadruples(self):
        print("[INFO] Probando cuádruplos de control de flujo (si/sino, mientras)...")
        code = '''
        programa test;
        vars x : entero;
        inicio
            si (x > 0) {
                x = 1;
            } sino {
                x = 0;
            };
            
            mientras (x < 10) haz {
                x = x + 1;
            };
        fin
        '''
        parser.parse(code, lexer=lexer)
        quads = quadruple_manager.quadruples
        
        print("[INFO] Cuádruplos generados:")
        for i, q in enumerate(quads):
            print(f"  {i}: {q}")
        
        has_gotof = any(q.operator == 'gotof' for q in quads)
        has_goto = any(q.operator == 'goto' for q in quads)
        
        self.assertTrue(has_gotof, "Debe haber GOTOF")
        self.assertTrue(has_goto, "Debe haber GOTO")
        print("[SUCCESS] Cuádruplos de control de flujo verificados.")

    def test_function_call_quadruples(self):
        print("[INFO] Probando cuádruplos de llamada a función...")
        code = '''
        programa test;
        nula func(a : entero) { }
        inicio
            func(10);
        fin
        '''
        parser.parse(code, lexer=lexer)
        quads = quadruple_manager.quadruples
        
        print("[INFO] Cuádruplos generados:")
        for i, q in enumerate(quads):
            print(f"  {i}: {q}")
            
        has_era = any(q.operator == 'ERA' for q in quads)
        has_param = any(q.operator == 'PARAM' for q in quads)
        has_gosub = any(q.operator == 'GOSUB' for q in quads)
        
        self.assertTrue(has_era, "Debe haber ERA")
        self.assertTrue(has_param, "Debe haber PARAM")
        self.assertTrue(has_gosub, "Debe haber GOSUB")
        print("[SUCCESS] Cuádruplos de función verificados.")

if __name__ == '__main__':
    unittest.main()
