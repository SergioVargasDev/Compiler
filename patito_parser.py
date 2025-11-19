import ply.yacc as yacc
from patito_lexer import tokens, lexer
from semantic_cube import semantic_cube
from symbol_table import function_directory
from quadruples import quadruple_manager

# PRECEDENCIA CORREGIDA
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
    ('nonassoc', 'MENOR', 'MAYOR', 'IGUAL', 'DIFERENTE', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
)

def p_programa(p):
    'programa : PROGRAMA ID PUNTOCOMA vars funcs INICIO cuerpo FIN'
    p[0] = ('programa', p[2], p[4], p[5], p[7])
    print("✓ Programa válido - Análisis semántico completado")
    quadruple_manager.complete_patching()
    quadruple_manager.print_quadruples()

def p_vars(p):
    '''vars : VARS declaraciones
            | empty'''
    p[0] = p[2] if len(p) > 2 else []

def p_declaraciones(p):
    '''declaraciones : declaracion declaraciones
                     | declaracion'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_declaracion(p):
    'declaracion : lista_ids DOSPUNTOS tipo PUNTOCOMA'
    var_type = p[3]
    for var_name in p[1]:
        try:
            current_scope = function_directory.get_current_scope()
            current_scope.add_variable(var_name, var_type)
            print(f"✓ Variable declarada: {var_name} : {var_type}")
        except Exception as e:
            print(f"✗ Error semántico: {e}")
            raise
    
    p[0] = ('declaracion', p[1], p[3])

def p_lista_ids(p):
    '''lista_ids : ID
                 | ID COMA lista_ids'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_tipo(p):
    '''tipo : ENTERO
            | FLOTANTE'''
    p[0] = p[1]

def p_funcs(p):
    '''funcs : func funcs
             | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_func(p):
    'func : func_tipo ID PARIZQ params PARDER LLAVEIZQ vars cuerpo LLAVEDER'
    return_type = p[1]
    func_name = p[2]
    parameters = p[4]
    
    try:
        function_directory.add_function(func_name, return_type, [])
        function_directory.set_current_function(func_name)
        for param_name, param_type in parameters:
            function_directory.add_parameter(func_name, param_name, param_type)
        print(f"✓ Función declarada: {func_name} -> {return_type}")
    except Exception as e:
        print(f"✗ Error semántico: {e}")
        raise
    
    p[0] = ('func', p[1], p[2], p[4], p[7], p[8])
    function_directory.set_current_function('global')

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
    if len(p) == 3 and p[2]:
        p[0] = [p[1]] + p[2]
    elif len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_estatuto(p):
    '''estatuto : asigna
                | condicion
                | ciclo
                | llamada PUNTOCOMA
                | imprime PUNTOCOMA'''
    p[0] = p[1]

def p_asigna(p):
    'asigna : ID ASIGNACION expresion PUNTOCOMA'
    # Punto neurálgico: Generar cuádruplo de asignación
    var_name = p[1]
    
    # Obtener el resultado de la expresión (último temporal generado)
    if quadruple_manager.operands_stack:
        result_operand = quadruple_manager.operands_stack.pop()
        # Generar cuádruplo de asignación
        quadruple_manager.add_quadruple('=', result_operand, '', var_name)
    
    current_scope = function_directory.get_current_scope()
    var_info = current_scope.get_variable(var_name)
    
    if var_info is None:
        raise Exception(f"Variable '{var_name}' no declarada")
    
    p[0] = ('asigna', p[1], p[3])

def p_condicion(p):
    'condicion : SI PARIZQ expresion PARDER cuerpo sino PUNTOCOMA'
    # Punto neurálgico: Cuádruplos para condicional
    # Después de procesar el cuerpo del if, generar GOTO al final
    end_quad = quadruple_manager.add_quadruple('goto', '', '', '')
    
    # Si hay sino, parchear el gotof al inicio del sino
    if p[6]:  # Hay bloque sino
        sino_quad = quadruple_manager.next_quad()
        quadruple_manager.patch(quadruple_manager.pop_jump(), sino_quad)
    else:
        # No hay sino, parchear gotof al final del if
        false_jump = quadruple_manager.pop_jump()
        if false_jump is not None:
            quadruple_manager.patch(false_jump, quadruple_manager.next_quad())
    
    # Parchear el GOTO final
    quadruple_manager.patch(end_quad, quadruple_manager.next_quad())
    
    p[0] = ('condicion', p[3], p[5], p[6])

def p_sino(p):
    '''sino : SINO cuerpo
            | empty'''
    if len(p) > 2:
        # Hay bloque sino, empujar GOTO al final
        end_quad = quadruple_manager.add_quadruple('goto', '', '', '')
        quadruple_manager.push_jump(end_quad)
        p[0] = p[2]
    else:
        p[0] = None

def p_ciclo(p):
    'ciclo : MIENTRAS PARIZQ expresion PARDER HAZ cuerpo PUNTOCOMA'
    # Punto neurálgico: Cuádruplos para ciclo con GOTOs
    # Al final del cuerpo del ciclo, generar GOTO al inicio
    return_quad = quadruple_manager.add_quadruple('goto', '', '', '')
    
    # Parchear el GOTO de retorno al inicio del ciclo
    start_quad = quadruple_manager.pop_jump()
    if start_quad is not None:
        quadruple_manager.patch(return_quad, start_quad)
    
    # Parchear el gotof (si la condición es falsa) al final
    false_jump = quadruple_manager.pop_jump()
    if false_jump is not None:
        quadruple_manager.patch(false_jump, quadruple_manager.next_quad())
    
    p[0] = ('ciclo', p[3], p[6])

def p_llamada(p):
    'llamada : ID PARIZQ argumentos PARDER'
    func_name = p[1]
    arguments = p[3]
    
    try:
        arg_types = []
        for arg in arguments:
            if isinstance(arg, tuple) and len(arg) > 1:
                arg_type = arg[-1] if isinstance(arg[-1], str) else 'entero'
            else:
                arg_type = arg
            arg_types.append(arg_type)
        
        function_directory.validate_call(func_name, arg_types)
        func_info = function_directory.get_function(func_name)
        p[0] = ('llamada', p[1], p[3], func_info['return_type'])
    except Exception as e:
        print(f"✗ Error en llamada a función: {e}")
        raise

def p_argumentos(p):
    '''argumentos : expresion_lista
                  | empty'''
    p[0] = p[1] if p[1] else []

def p_expresion_lista(p):
    '''expresion_lista : expresion
                       | expresion COMA expresion_lista'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_imprime(p):
    'imprime : ESCRIBE PARIZQ imprime_lista PARDER'
    # Generar cuádruplos PRINT para cada elemento
    for elemento in p[3]:
        if elemento == 'expresion_aritmetica' or elemento == 'expresion_relacional':
            # Es una expresión - usar el último temporal de la pila
            if quadruple_manager.operands_stack:
                value_addr = quadruple_manager.operands_stack.pop()
                # Obtener el nombre legible para el print
                value_name = quadruple_manager.address_to_name.get(value_addr, f"temp_{value_addr}")
                quadruple_manager.add_quadruple('print', value_name, '', '')
        elif isinstance(elemento, str) and not elemento.startswith('expresion'):
            # Es un letrero literal
            quadruple_manager.add_quadruple('print', f'"{elemento}"', '', '')
    p[0] = ('imprime', p[3])

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
    p[0] = p[1]

def p_expresion(p):
    '''expresion : exp
                 | exp MENOR exp
                 | exp MAYOR exp
                 | exp IGUAL exp
                 | exp DIFERENTE exp
                 | exp MAYOR_IGUAL exp
                 | exp MENOR_IGUAL exp'''
    
    if len(p) == 2:
        p[0] = p[1]  # Expresión simple
    else:
        # Expresión relacional - generar cuádruplo
        operator = p[2]
        quadruple_manager.push_operator(operator)
        quadruple_manager.generate_quadruple()
        
        # Para estructuras de control, generar GOTOF
        if len(p) == 4:  # Es una expresión relacional completa
            # Guardar el resultado de la expresión relacional
            if quadruple_manager.operands_stack:
                condition_result = quadruple_manager.operands_stack.pop()
                # Generar GOTOF (goto if false)
                gotof_quad = quadruple_manager.add_quadruple('gotof', condition_result, '', '')
                quadruple_manager.push_jump(gotof_quad)
                
                # Si estamos en un contexto de ciclo, guardar también la posición de inicio
                # Esto se maneja en la regla del ciclo específicamente
        
        p[0] = 'expresion_relacional'

def p_exp(p):
    '''exp : termino
           | exp MAS termino
           | exp MENOS termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Operaciones aritméticas
        operator = p[2]
        quadruple_manager.push_operator(operator)
        quadruple_manager.generate_quadruple()
        p[0] = 'expresion_aritmetica'

def p_termino(p):
    '''termino : factor
               | termino MULT factor
               | termino DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Operaciones aritméticas
        operator = p[2]
        quadruple_manager.push_operator(operator)
        quadruple_manager.generate_quadruple()
        p[0] = 'termino_aritmetico'

def p_factor(p):
    '''factor : CTE_ENT
              | CTE_FLOAT
              | ID
              | PARIZQ expresion PARDER'''
    
    if len(p) == 2:
        # Caso simple: constante o variable
        if isinstance(p[1], int):
            # Constante entera
            constant_value = str(p[1])
            quadruple_manager.push_operand(constant_value, 'entero')
            p[0] = 'constante_entera'
        elif isinstance(p[1], float):
            # Constante flotante
            constant_value = str(p[1])
            quadruple_manager.push_operand(constant_value, 'flotante')
            p[0] = 'constante_flotante'
        else:
            # ID de variable
            var_name = p[1]
            current_scope = function_directory.get_current_scope()
            var_info = current_scope.get_variable(var_name)
            
            if var_info is None:
                raise Exception(f"Variable '{var_name}' no declarada")
            
            quadruple_manager.push_operand(var_name, var_info['type'])
            p[0] = 'variable'
    else:
        # Expresión entre paréntesis: (expresion)
        p[0] = p[2]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (tipo: {p.type}, línea {p.lineno})")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()