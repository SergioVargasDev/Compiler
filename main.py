import sys
from patito_parser import parser
from patito_lexer import lexer
from quadruples import quadruple_manager
from memory_manager import memory_manager
from virtual_machine import VirtualMachine

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
        # Limpiar estados
        quadruple_manager.clear()
        memory_manager.reset()
        
        print("1. Compilando...")
        result = parser.parse(data, lexer=lexer)
        
        print("\n2. Ejecutando...")
        vm = VirtualMachine(quadruple_manager.quadruples, memory_manager.constants_table)
        vm.run()
        
    except Exception as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()