from patito_parser import parser
from patito_lexer import lexer

def test_semantic():
    test_cases = [
        # Test 1: Programa válido
        ("""
programa Test;
vars
    x, y : entero;
    z : flotante;
inicio
    x = 10;
    y = x + 5;
    z = 3.14;
fin
        """, "VÁLIDO"),
        
        # Test 2: Variable no declarada
        ("""
programa Test;
vars
    x : entero;
inicio
    y = 10;
fin
        """, "ERROR - Variable no declarada"),
        
        # Test 3: Tipos compatibles
        ("""
programa Test;
vars
    x : entero;
    y : flotante;
inicio
    x = 5;
    y = 3.14;
    x = y;  // entero = flotante (válido con conversión)
fin
        """, "VÁLIDO"),
        
        # Test 4: Función simple
        ("""
programa Test;
vars
    resultado : entero;

nula saludar() {
    escribe("Hola mundo");
}

inicio
    saludar();
    resultado = 42;
fin
        """, "VÁLIDO"),
    ]
    
    for i, (code, expected) in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"TEST {i}: {expected}")
        print(f"{'='*50}")
        print("Código:")
        print(code.strip())
        print("\nResultado:")
        
        try:
            result = parser.parse(code, lexer=lexer)
            if result:
                print("✓ ANÁLISIS SEMÁNTICO EXITOSO")
            else:
                print("✗ Error en el análisis")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_semantic()