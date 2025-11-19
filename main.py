from patito_parser import parser
from patito_lexer import lexer
from quadruples import quadruple_manager
import sys

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: Archivo {sys.argv[1]} no encontrado")
            return
    else:
        print("Compilador Patito - Escribe código (Ctrl+D para terminar):")
        data = sys.stdin.read()

    try:
        # Limpiar cuádruplos anteriores
        quadruple_manager.clear()
        
        result = parser.parse(data, lexer=lexer)
        if result:
            print("✓ Análisis exitoso")
            print("AST:", result)
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()