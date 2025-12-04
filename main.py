import sys
from patito_parser import parser
from patito_lexer import lexer
from quadruples import quadruple_manager
from memory_manager import memory_manager
from virtual_machine import VirtualMachine
from symbol_table import function_directory

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
        quadruple_manager.clear()
        memory_manager.reset()
        
        print("\n=== 1. COMPILACIÓN ===")
        parser.parse(data, lexer=lexer)
        
        print("\n=== 2. DIRECTORIO DE FUNCIONES (TABLA DE SÍMBOLOS) ===")
        function_directory.print_directory()
        memory_manager.print_memory_distribution()
        
        print("\n=== 3. CÓDIGO INTERMEDIO (CUÁDRUPLOS) ===")
        quadruple_manager.print_quadruples()
        
        print("\n" + "="*50)
        print("🚀  INICIANDO MÁQUINA VIRTUAL...")
        print("="*50 + "\n")
        
        vm = VirtualMachine(quadruple_manager.quadruples, memory_manager.constants_table)
        vm.run()
        
        print("\n" + "="*50)
        print("EJECUCIÓN FINALIZADA")
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()