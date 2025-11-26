import unittest
from patito_lexer import lexer

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer
        print(f"\n{'-'*60}")
        print(f"Running Lexer Test: {self._testMethodName}")
        print(f"{'-'*60}")

    def test_tokens_basic(self):
        print("[INFO] Probando tokens básicos...")
        data = '''
        programa test;
        vars
        i : entero;
        f : flotante;
        inicio
        i = 10;
        f = 3.14;
        si (i > 0) haz {
            escribe("hola");
        };
        fin
        '''
        self.lexer.input(data)
        
        expected_tokens = [
            'PROGRAMA', 'ID', 'PUNTOCOMA',
            'VARS',
            'ID', 'DOSPUNTOS', 'ENTERO', 'PUNTOCOMA',
            'ID', 'DOSPUNTOS', 'FLOTANTE', 'PUNTOCOMA',
            'INICIO',
            'ID', 'ASIGNACION', 'CTE_ENT', 'PUNTOCOMA',
            'ID', 'ASIGNACION', 'CTE_FLOAT', 'PUNTOCOMA',
            'SI', 'PARIZQ', 'ID', 'MAYOR', 'CTE_ENT', 'PARDER', 'HAZ', 'LLAVEIZQ',
            'ESCRIBE', 'PARIZQ', 'LETRERO', 'PARDER', 'PUNTOCOMA',
            'LLAVEDER', 'PUNTOCOMA',
            'FIN'
        ]
        
        tokens_found = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens_found.append(tok.type)
            # print(f"  Token encontrado: {tok.type} -> {tok.value}")
            
        self.assertEqual(tokens_found, expected_tokens)
        print("[SUCCESS] Tokens básicos reconocidos correctamente.")

    def test_tokens_complex(self):
        print("[INFO] Probando tokens complejos (comentarios, strings, operadores)...")
        data = '''
        /* Comentario de bloque */
        var_1 = "Texto con espacios";
        val = 1.5 + 2 * 3;
        comp = a >= b;
        '''
        self.lexer.input(data)
        
        # Solo verificamos que no lance error y reconozca tipos clave
        tokens_found = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens_found.append(tok.type)
            print(f"  Token: {tok.type:15} | Valor: {tok.value}")
            
        self.assertIn('LETRERO', tokens_found)
        self.assertIn('MAYOR_IGUAL', tokens_found)
        self.assertIn('CTE_FLOAT', tokens_found)
        print("[SUCCESS] Tokens complejos reconocidos correctamente.")

if __name__ == '__main__':
    unittest.main()
