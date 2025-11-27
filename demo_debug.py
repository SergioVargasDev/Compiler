import sys
import time
from patito_lexer import lexer
from patito_parser import parser
from symbol_table import function_directory
from quadruples import quadruple_manager
from memory_manager import memory_manager
from virtual_machine import VirtualMachine

# Códigos de color para la terminal
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(title):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{title.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def pause():
    input(f"\n{YELLOW}Presiona ENTER para continuar al siguiente paso...{RESET}")

def demo_compiler():
    # 1. Código de prueba (Factorial Iterativo para que sea interesante pero no eterno)
    code = '''
    programa DemoFactorial;
    vars
        n, res : entero;

    entero factorial(num : entero) {
        vars
            acum : entero;
            i : entero;
        {
            acum = 1;
            i = 1;
            mientras (i < num) haz {
                i = i + 1;
                acum = acum * i;
            };
            factorial = acum;
        }
    }

    inicio
        n = 5;
        res = factorial(n);
        escribe("El factorial de 5 es:", res);
    fin
    '''

    print_header("DEMOSTRACIÓN COMPILADOR PATITO")
    print(f"Código Fuente a Compilar:\n{GREEN}{code}{RESET}")
    pause()

    # ---------------------------------------------------------
    # PASO 1: ESCÁNER (LEXER)
    # ---------------------------------------------------------
    print_header("PASO 1: ANÁLISIS LÉXICO (SCANNER)")
    print("Identificando tokens en el código fuente...")
    
    lexer.input(code)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"  Token: {GREEN}{tok.type:15}{RESET} | Valor: {tok.value}")
        time.sleep(0.01) # Pequeña pausa para efecto visual
    
    print(f"\n{BOLD}✓ Análisis Léxico completado.{RESET}")
    pause()

    # ---------------------------------------------------------
    # PASO 2: PARSER Y SEMÁNTICA
    # ---------------------------------------------------------
    print_header("PASO 2: ANÁLISIS SINTÁCTICO Y SEMÁNTICO")
    print("Construyendo tablas de símbolos y verificando tipos...")
    
    # Resetear estado
    function_directory.functions = {}
    function_directory.current_function = 'global'
    function_directory.global_scope.variables = {}
    function_directory.add_function('global', 'nula', [])
    quadruple_manager.clear()
    memory_manager.reset()

    try:
        parser.parse(code, lexer=lexer)
        print(f"\n{BOLD}✓ Análisis Sintáctico y Semántico completado sin errores.{RESET}")
    except Exception as e:
        print(f"{BOLD}✗ Error durante el análisis:{RESET} {e}")
        return

    pause()

    # ---------------------------------------------------------
    # PASO 3: TABLAS DE SÍMBOLOS Y DIRECTORIO DE FUNCIONES
    # ---------------------------------------------------------
    print_header("PASO 3: ESTRUCTURAS DE DATOS GENERADAS")
    
    print(f"{BOLD}Directorio de Funciones:{RESET}")
    for func_name, func_data in function_directory.functions.items():
        print(f"  Función: {BLUE}{func_name}{RESET} (Tipo: {func_data['return_type']})")
        print(f"    Inicio Cuádruplos: {func_data['start_quad']}")
        print(f"    Variables Locales: {len(func_data['local_scope'].variables)}")
        print(f"    Parámetros: {len(func_data['parameters'])}")
        print("-" * 30)

    print(f"\n{BOLD}Tabla de Constantes (Memoria):{RESET}")
    for key, addr in memory_manager.constants_table.items():
        print(f"  {key:15} -> Dirección: {addr}")

    pause()

    # ---------------------------------------------------------
    # PASO 4: GENERACIÓN DE CÓDIGO INTERMEDIO (CUÁDRUPLOS)
    # ---------------------------------------------------------
    print_header("PASO 4: CUÁDRUPLOS (CÓDIGO INTERMEDIO)")
    print("Instrucciones de bajo nivel generadas para la VM:")
    
    # Usamos print_quadruples_raw para ver direcciones reales
    print(f"\n{BOLD}Lista de Cuádruplos (Direcciones Reales):{RESET}")
    for i, quad in enumerate(quadruple_manager.quadruples):
        print(f"  {i}:\t({quad.operator}, {quad.left_operand}, {quad.right_operand}, {quad.result})")
    
    pause()

    # ---------------------------------------------------------
    # PASO 5: MÁQUINA VIRTUAL
    # ---------------------------------------------------------
    print_header("PASO 5: EJECUCIÓN EN MÁQUINA VIRTUAL")
    print("Ejecutando instrucción por instrucción...")
    print("-" * 60)
    
    vm = VirtualMachine(quadruple_manager.quadruples, memory_manager.constants_table)
    vm.run(debug=True)
    
    print("-" * 60)
    print(f"\n{BOLD}✓ Ejecución finalizada con éxito.{RESET}")

if __name__ == "__main__":
    demo_compiler()
