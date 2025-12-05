import ply.yacc as yacc
from patito_lexer import tokens, lexer
from semantic_cube import semantic_cube
from symbol_table import function_directory
from quadruples import quadruple_manager
from memory_manager import memory_manager

precedence = (
    ('nonassoc', 'MENOR', 'MAYOR', 'IGUAL', 'DIFERENTE', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
)

# Regla principal del programa
def p_programa(p):
    # Regla principal del programa
    'programa : PROGRAMA ID PUNTOCOMA start_goto vars funcs fill_goto_main INICIO start_main cuerpo FIN'
    print("\n✓ COMPILACIÓN EXITOSA - Programa válido")
    # Completa los saltos pendientes
    quadruple_manager.complete_patching()

# Regla neurálgica para iniciar el salto al main
def p_start_goto(p):
    #La palabra empty le dice al parser que no espere ningún token
    'start_goto : empty'
    # Si el siguiente cuadruplo es el cuadruplo 0, significa que no hay cuadruplos anteriores
    if quadruple_manager.next_quad() == 0:
        # Agrega un cuadruplo goto al final
        goto_main = quadruple_manager.add_quadruple('goto', '', '', '')
        # Guarda el índice del cuadruplo goto
        quadruple_manager.goto_main_index = goto_main

# Regla para completar el salto al main
def p_fill_goto_main(p):
    'fill_goto_main : empty'
    pass

# Regla para iniciar la función main
def p_start_main(p):
    'start_main : empty'
    if quadruple_manager.goto_main_index is not None:
        quadruple_manager.patch(quadruple_manager.goto_main_index, quadruple_manager.next_quad())

# Regla para declaraciones
def p_vars(p):
    # El parser busca que haya variables declaradas, si no serán omitidas gracias al |empty|
    '''vars : VARS declaraciones
            | empty'''

# Regla para declaraciones
def p_declaraciones(p):
    '''declaraciones : declaracion declaraciones
                     | declaracion'''
    """
    a : entero;
    b : flotante;  <-- El parser vuelve a llamar a 'declaracion'
    c : entero;    <-- Y otra vez
    |
     a : entero;
    """

def p_declaracion(p):
    'declaracion : lista_ids DOSPUNTOS tipo PUNTOCOMA'
    var_type = p[3]
    var_names = p[1]

    for var_name in var_names:
        try:
            current_scope, scope_type = function_directory.get_current_scope_info()
            address = current_scope.add_variable(var_name, var_type, scope_type)
            
            print(f"✓ Variable declarada: {var_name} ({var_type}) -> Dir: {address}")
        except Exception as e:
            print(f"✗ Error semántico: {e}")
            raise
    
def p_lista_ids(p):
    '''lista_ids : ID
                 | ID COMA lista_ids'''
    
    # lista_ids : ID
    # p tiene índices [0, 1]. Longitud = 2
    if len(p) == 2:
        p[0] = [p[1]]
        
    # lista_ids : ID COMA lista_ids
    # p tiene índices [0, 1, 2, 3]. Longitud = 4
    else:
        # Ignoramos p[2] (la coma)
        p[0] = [p[1]] + p[3]

def p_tipo(p):
    '''tipo : ENTERO
            | FLOTANTE'''
    p[0] = p[1]


def p_funcs(p):
    '''funcs : func funcs
             | empty'''
    p[0] = []

def p_func(p):
    'func : func_header LLAVEIZQ vars cuerpo LLAVEDER'
    quadruple_manager.add_endfunc()
    function_directory.set_current_function('global')

def p_func_header(p):
    'func_header : func_tipo ID PARIZQ params PARDER'
    return_type = p[1]
    func_name = p[2]
    parameters = p[4]
    
    try:
        function_directory.add_function(func_name, return_type, [])
        function_directory.set_current_function(func_name)
        
        start_quad = quadruple_manager.next_quad()
        function_directory.set_start_quad(func_name, start_quad)
        
        for param_name, param_type in parameters:
            function_directory.add_parameter(func_name, param_name, param_type)
            
        print(f"✓ Función iniciada: {func_name} -> {return_type}")
    except Exception as e:
        print(f"✗ Error semántico en función: {e}")
        raise
        
    p[0] = {'type': return_type, 'name': func_name}

def p_func_tipo(p):
    '''func_tipo : NULA
                 | tipo'''
    p[0] = 'nula' if p[1] == 'nula' else p[1]

def p_params(p):
    '''params : param_list
              | empty'''
    p[0] = p[1] if p[1] else []

def p_param_list(p):
    '''param_list : param
                  | param COMA param_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_param(p):
    'param : ID DOSPUNTOS tipo'
    p[0] = (p[1], p[3])


def p_cuerpo(p):
    '''cuerpo : LLAVEIZQ estatutos LLAVEDER
              | estatutos'''
    p[0] = p[2] if len(p) == 4 else p[1]

def p_estatutos(p):
    '''estatutos : estatuto estatutos
                 | empty'''
    pass

def p_estatuto(p):
    '''estatuto : asigna
                | condicion
                | ciclo
                | llamada PUNTOCOMA
                | imprime PUNTOCOMA'''
    pass


def p_asigna(p):
    'asigna : ID ASIGNACION expresion PUNTOCOMA'
    var_name = p[1]
    
    if quadruple_manager.operands_stack:
        result_operand_address = quadruple_manager.operands_stack.pop()
        if quadruple_manager.types_stack:
            quadruple_manager.types_stack.pop()
    else:
        raise Exception("Error interno: No hay resultado para asignar.")
    
    current_scope = function_directory.get_current_scope()
    var_info = current_scope.get_variable(var_name)
    
    if var_info is None:
        raise Exception(f"Variable '{var_name}' no declarada")
    
    quadruple_manager.add_quadruple('=', result_operand_address, '', var_info['address'])


def p_condicion(p):
    'condicion : SI PARIZQ expresion PARDER cuerpo seen_if_body sino PUNTOCOMA'
    end_jump = quadruple_manager.pop_jump()
    quadruple_manager.patch(end_jump, quadruple_manager.next_quad())

def p_seen_if_body(p):
    'seen_if_body : empty'
    goto_end = quadruple_manager.add_quadruple('goto', '', '', '')
    
    false_jump = quadruple_manager.pop_jump()
    quadruple_manager.push_jump(goto_end)
    
    quadruple_manager.patch(false_jump, quadruple_manager.next_quad())

def p_sino(p):
    '''sino : SINO cuerpo
            | empty'''
    pass

def p_seen_mientras(p):
    'seen_mientras : empty'
    quadruple_manager.push_jump(quadruple_manager.next_quad())

def p_ciclo(p):
    'ciclo : MIENTRAS seen_mientras PARIZQ expresion PARDER HAZ cuerpo PUNTOCOMA'
    return_quad = quadruple_manager.add_quadruple('goto', '', '', '')
    
    false_jump = quadruple_manager.pop_jump()
    start_quad = quadruple_manager.pop_jump()
    
    quadruple_manager.patch(return_quad, start_quad)
    quadruple_manager.patch(false_jump, quadruple_manager.next_quad())


def p_llamada(p):
    'llamada : ID PARIZQ argumentos PARDER'
    func_name = p[1]
    arguments = p[3]
    
    try:
        arg_types = []
        arg_addresses = []
        
        for _ in range(len(arguments)):
            if quadruple_manager.operands_stack:
                arg_addresses.append(quadruple_manager.operands_stack.pop())
                arg_types.append(quadruple_manager.types_stack.pop())
        
        arg_addresses.reverse()
        arg_types.reverse()
        
        function_directory.validate_call(func_name, arg_types)
        func_info = function_directory.get_function(func_name)
        
        quadruple_manager.add_era(func_name)
        
        for i, arg_addr in enumerate(arg_addresses):
            param_info = func_info['parameters'][i]
            dest_addr = param_info['address']
            quadruple_manager.add_param(arg_addr, dest_addr)
            
        quadruple_manager.add_gosub(func_name, func_info['start_quad'])
        
        if func_info['return_type'] != 'nula':
            global_var = function_directory.global_scope.get_variable(func_name)
            ret_var_addr = global_var['address']
            
          
            temp_addr = quadruple_manager.new_temp(func_info['return_type'])
            
            quadruple_manager.add_quadruple('=', ret_var_addr, '', temp_addr)
            
            quadruple_manager.push_address(temp_addr, func_info['return_type'])
            
        p[0] = ('llamada', func_name, func_info['return_type'])
        
    except Exception as e:
        print(f"✗ Error en llamada a '{func_name}': {e}")
        raise

def p_argumentos(p):
    '''argumentos : expresion_lista
                  | empty'''
    p[0] = p[1] if p[1] else []

def p_expresion_lista(p):
    '''expresion_lista : expresion
                       | expresion COMA expresion_lista'''
    if len(p) == 2:
        p[0] = [1] 
    else:
        p[0] = [1] + p[3]


def p_imprime(p):
    'imprime : ESCRIBE PARIZQ imprime_lista PARDER'
    valores_a_imprimir = []
    
    for elemento in reversed(p[3]):
        if isinstance(elemento, str) and elemento.startswith('"'):
            val_limpio = elemento.strip('"')
            addr = memory_manager.get_constant_address(val_limpio, 'letrero')
            valores_a_imprimir.append(addr)
        else:
            if quadruple_manager.operands_stack:
                val_addr = quadruple_manager.operands_stack.pop()
                if quadruple_manager.types_stack: quadruple_manager.types_stack.pop()
                valores_a_imprimir.append(val_addr)
    
    valores_a_imprimir.reverse()
    
    for val in valores_a_imprimir:
        quadruple_manager.add_quadruple('print', val, '', '')

def p_imprime_lista(p):
    '''imprime_lista : elemento_imprimir
                     | elemento_imprimir COMA imprime_lista'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_elemento_imprimir(p):
    '''elemento_imprimir : expresion
                         | LETRERO'''
    if p.slice[1].type == 'LETRERO':
        p[0] = f'"{p[1]}"'
    else:
        p[0] = 'EXP'


def p_expresion(p):
    '''expresion : exp
                 | exp MENOR exp
                 | exp MAYOR exp
                 | exp IGUAL exp
                 | exp DIFERENTE exp
                 | exp MAYOR_IGUAL exp
                 | exp MENOR_IGUAL exp'''
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        operator = p[2]
        quadruple_manager.push_operator(operator)
        quadruple_manager.generate_quadruple()
        
        if len(p) == 4:
            if quadruple_manager.operands_stack:
                condition_result = quadruple_manager.operands_stack.pop()
                gotof_quad = quadruple_manager.add_quadruple('gotof', condition_result, '', '')
                quadruple_manager.push_jump(gotof_quad)

def p_exp(p):
    '''exp : termino
           | exp MAS termino
           | exp MENOS termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        quadruple_manager.push_operator(p[2])
        quadruple_manager.generate_quadruple()

def p_termino(p):
    '''termino : factor
               | termino MULT factor
               | termino DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        quadruple_manager.push_operator(p[2])
        quadruple_manager.generate_quadruple()

def p_factor(p):
    '''factor : CTE_ENT
              | CTE_FLOAT
              | ID
              | PARIZQ expresion PARDER
              | llamada'''
    if len(p) == 2:
        if isinstance(p[1], int):
            quadruple_manager.push_operand(p[1], 'entero')
        elif isinstance(p[1], float):
            quadruple_manager.push_operand(p[1], 'flotante')
        elif isinstance(p[1], str) and p.slice[1].type == 'ID':
            var_name = p[1]
            current_scope = function_directory.get_current_scope()
            var_info = current_scope.get_variable(var_name)
            
            if var_info is None:
                raise Exception(f"Variable '{var_name}' no declarada")
            
            quadruple_manager.push_address(var_info['address'], var_info['type'])
            
        elif isinstance(p[1], tuple) and p[1][0] == 'llamada':
            pass
    else:
        p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (Línea {p.lineno})")
    else:
        print("Error de sintaxis: Fin de archivo inesperado")

parser = yacc.yacc()