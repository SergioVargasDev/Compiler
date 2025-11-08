from patito_parser import parser
from patito_lexer import lexer
from symbol_table import function_directory  # Importar el directorio

def run_test(test_name, code):
    print(f"\n{'='*50}")
    print(f"TEST: {test_name}")
    print(f"{'='*50}")
    print(f"Código:\n{code}")
    print(f"\nResultado:")
    
    try:
        # 🔥 RESETEAR el directorio de funciones entre tests
        function_directory.functions = {}
        function_directory.current_function = 'global'
        function_directory.global_scope.variables = {}
        function_directory.add_function('global', 'nula', [])
        
        result = parser.parse(code, lexer=lexer)
        if result:
            print("✓ Análisis completado exitosamente")
            print("Estructura del programa:")
            print(result)
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Casos de prueba (se mantienen igual)
test_cases = [
    ("Programa básico con variables", """
programa HolaMundo;
vars
    x, y : entero;
    z : flotante;
inicio
    x = 10;
    y = 20;
    z = 3.14;
fin
    """),
    
    ("Programa con condicionales", """
programa Condicionales;
vars
    a, b : entero;
inicio
    a = 5;
    b = 10;
    si (a < b) {
        escribe("a es menor que b");
    } sino {
        escribe("a es mayor o igual que b");
    };
fin
    """),
    
    ("Programa con ciclo mientras", """
programa CicloMientras;
vars
    i : entero;
inicio
    i = 0;
    mientras (i < 5) haz {
        escribe(i);
        i = i + 1;
    };
fin
    """),
    
    ("Programa con funciones", """
programa Funciones;
vars
    resultado : entero;

nula saludar() {
    escribe("Hola mundo");
}

inicio
    saludar();
    resultado = 42;
    escribe("Resultado:", resultado);
fin
    """),
    
    ("Expresiones aritméticas complejas", """
programa Expresiones;
vars
    a, b, c : entero;
inicio
    a = 10;
    b = 20;
    c = (a + b) * 2;
    si (c > 25) {
        escribe("c es mayor que 25");
    };
fin
    """),
    
    ("Programa simple para debug", """
programa Simple;
vars
    x : entero;
inicio
    x = 10;
    escribe(x);
fin
    """)
]

def run_all_tests():
    print("INICIANDO PRUEBAS DEL COMPILADOR PATITO")
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