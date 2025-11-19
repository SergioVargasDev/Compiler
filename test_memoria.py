from patito_parser import parser
from patito_lexer import lexer
from symbol_table import function_directory
from quadruples import quadruple_manager
from memory_manager import memory_manager

def test_codigo_complejo_mejorado():
    codigo = """
programa CodigoComplejo;
vars
    A, B, C, D, E, F, G, H, J, K : entero;
inicio
    A = 5;
    B = 10;
    C = 15;
    D = 20;
    E = 25;
    F = 30;
    G = 35;
    H = 40;
    J = 45;
    K = 50;
    
    A = B + C * (D - E / F) * H;
    B = E - F;
    
    mientras (A * B - C >= D * E / (G + H)) haz {
        H = J * K + B;
        
        si (B < H) {
            B = H + J;
            
            mientras (B > A + C) haz {
                escribe("Valor A+B*C:", A + B * C);
                escribe("Valor D-E:", D - E);
                B = B - J;
            };
        } sino {
            A = A + B;
            escribe("Valor B-D:", B - D);
        };
    };
    
    F = A + B;
    escribe("Resultado final F:", F);
fin
"""

    print("=" * 80)
    print("PRUEBA MEJORADA: CÓDIGO COMPLEJO CON VALORES REALES")
    print("=" * 80)
    
    try:
        # Reiniciar todo
        function_directory.functions = {}
        function_directory.current_function = 'global'
        function_directory.global_scope.variables = {}
        function_directory.add_function('global', 'nula', [])
        quadruple_manager.clear()
        
        print("Analizando código complejo mejorado...")
        result = parser.parse(codigo, lexer=lexer)
        
        if result:
            print("✓ Análisis completado exitosamente")
            
            # Mostrar distribución de memoria
            memory_manager.print_memory_distribution()
            
            # Mostrar tabla de direcciones
            print("\n=== TABLA DE DIRECCIONES VIRTUALES ===")
            quadruple_manager.print_address_table()
            
            # Mostrar cuádruplos
            quadruple_manager.print_quadruples()
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_codigo_complejo_mejorado()