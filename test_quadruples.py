from patito_parser import parser
from patito_lexer import lexer
from symbol_table import function_directory
from quadruples import quadruple_manager

def run_test(test_name, code):
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Código:\n{code}")
    print(f"\nResultado:")
    
    try:
        # Reiniciar estructuras
        function_directory.functions = {}
        function_directory.current_function = 'global'
        function_directory.global_scope.variables = {}
        function_directory.add_function('global', 'nula', [])
        quadruple_manager.clear()
        
        result = parser.parse(code, lexer=lexer)
        if result:
            print("✓ Análisis completado exitosamente")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Casos de prueba específicos para cuádruplos
test_cases = [
    ("Expresiones aritméticas simples", """
programa TestAritmetica;
vars
    a, b, c : entero;
inicio
    a = 5;
    b = 10;
    c = a + b * 2;
fin
    """),
    
    ("Expresiones con paréntesis", """
programa TestParentesis;
vars
    x, y, z : entero;
inicio
    x = 10;
    y = 20;
    z = (x + y) * 2;
fin
    """),
    
    ("Operaciones mixtas", """
programa TestMixto;
vars
    a : entero;
    b : flotante;
    c : flotante;
inicio
    a = 5;
    b = 3.14;
    c = a + b;
fin
    """),
    
    ("Expresiones relacionales", """
programa TestRelacional;
vars
    x, y : entero;
    resultado : entero;
inicio
    x = 10;
    y = 20;
    resultado = x < y;
fin
    """),
    
    ("Múltiples asignaciones", """
programa TestMultiples;
vars
    a, b, c, d : entero;
inicio
    a = 1;
    b = 2;
    c = 3;
    d = a + b + c;
fin
    """)
]

def run_all_tests():
    print("INICIANDO PRUEBAS DE GENERACIÓN DE CUÁDRUPLOS")
    print("=" * 60)
    
    passed = 0
    total = len(test_cases)
    
    for test_name, code in test_cases:
        if run_test(test_name, code):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"RESUMEN DE PRUEBAS: {passed}/{total} pasaron")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_all_tests()