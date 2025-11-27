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
    # 1. Código de prueba
    code = '''
    programa patito;
    vars
        i, j, k : entero;
        f : flotante;

    nula uno(a : entero, b : entero)
    {
        si (a > 0)
        {
            i = a + b * j + i;
            escribe (i + j);
            uno (a - i, i);
        }
        sino
        {
            escribe (a + b);
        };
    }

    entero dos(a : entero, g : flotante)
    {
        vars i : entero;
        {
            i = a;
            mientras (a > 0) haz
            {
                a = a - k * j;
                uno(a * 2, a + k);
                g = g * j - k;
            };
            dos = i + k * j;
        }
    }

    inicio
        i = 2;
        j = 3;
        k = i + 1;
        f = 3.14;

        mientras (i > 0) haz
        {
            escribe( dos ( i + k, f * 3) + 3);
            escribe( i , j * 2, f * 2 + 1.5);
            i = i - k;
        };
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
    
    print(f"{BOLD}=== TABLA DE VARIABLES GLOBALES ==={RESET}")
    if function_directory.global_scope.variables:
        print(f"{'Nombre':<15} {'Tipo':<10} {'Dirección':<10}")
        print("-" * 40)
        for name, var_data in function_directory.global_scope.variables.items():
            print(f"{name:<15} {var_data['type']:<10} {var_data['address']:<10}")
    else:
        print("  (No hay variables globales)")
    print("-" * 60)

    print(f"\n{BOLD}=== DIRECTORIO DE FUNCIONES Y VARIABLES LOCALES ==={RESET}")
    for func_name, func_data in function_directory.functions.items():
        print(f"\nFunción: {BLUE}{func_name}{RESET}")
        print(f"  Tipo Retorno: {func_data['return_type']}")
        print(f"  Inicio Cuádruplos: {func_data['start_quad']}")
        
        # Parámetros
        params = func_data['parameters']
        print(f"  Parámetros ({len(params)}):")
        if params:
            for param in params:
                print(f"    - {param['name']} ({param['type']}) -> Dir: {param['address']}")
        else:
            print("    (Ninguno)")
            
        # Variables Locales (incluye parámetros en la tabla de variables)
        local_vars = func_data['local_scope'].variables
        print(f"  Variables en Scope ({len(local_vars)} total):")
        # Identificar cuáles son locales puras (no parámetros)
        param_names = [p['name'] for p in params]
        
        for name, var_data in local_vars.items():
            kind = "Parámetro" if name in param_names else "Local"
            print(f"    - {name:<10} ({var_data['type']:<8}) -> Dir: {var_data['address']:<6} [{kind}]")
            
        print("-" * 30)

    print(f"\n{BOLD}=== TABLA DE CONSTANTES (MEMORIA) ==={RESET}")
    if memory_manager.constants_table:
        print(f"{'Valor_Tipo':<20} {'Dirección':<10}")
        print("-" * 40)
        # Ordenar por dirección para mayor claridad
        sorted_consts = sorted(memory_manager.constants_table.items(), key=lambda item: item[1])
        for key, addr in sorted_consts:
            print(f"{key:<20} {addr:<10}")
    else:
        print("  (No hay constantes)")

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
