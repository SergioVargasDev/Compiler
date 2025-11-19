from patito_parser import parser
from patito_lexer import lexer
from symbol_table import function_directory
from quadruples import quadruple_manager

def test_codigo_complejo():
    codigo = """
programa CodigoComplejo;
vars
    A, B, C, D, E, F, G, H, J, K : entero;
inicio
    A = B + C * (D - E / F) * H;
    B = E - F;
    
    mientras (A * B - C >= D * E / (G + H)) haz {
        H = J * K + B;
        
        si (B < H) {
            B = H + J;
            
            mientras (B > A + C) haz {
                escribe(A + B * C, D - E);
                B = B - J;
            };
        } sino {
            A = A + B;
            escribe(B - D);
        };
    };
    
    F = A + B;
fin
"""

    print("=" * 80)
    print("PRUEBA: CÓDIGO COMPLEJO CON EXPRESIONES ANIDADAS")
    print("=" * 80)
    print("Código a analizar:")
    print(codigo)
    print("\n" + "=" * 80)
    
    try:
        # Reiniciar estructuras
        function_directory.functions = {}
        function_directory.current_function = 'global'
        function_directory.global_scope.variables = {}
        function_directory.add_function('global', 'nula', [])
        quadruple_manager.clear()
        
        print("Iniciando análisis...")
        result = parser.parse(codigo, lexer=lexer)
        
        if result:
            print("✓ Análisis completado exitosamente")
            print("\n✓ AST generado correctamente")
        return True
        
    except Exception as e:
        print(f"✗ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_codigo_complejo()