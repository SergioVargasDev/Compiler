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
    'programa : PROGRAMA ID PUNTOCOMA start_goto vars funcs fill_goto_main INICIO start_main cuerpo FIN'
    p[0] = ('programa', p[2], p[4], p[5], p[7])
    print("✓ Programa válido - Análisis semántico completado")
    quadruple_manager.complete_patching()
    quadruple_manager.print_quadruples()

def p_start_main(p):
    'start_main : empty'
    # Neuralgic point: Patch GOTO main to jump HERE (right after INICIO)
    if hasattr(quadruple_manager, 'goto_main_index') and quadruple_manager.goto_main_index is not None:
        quadruple_manager.patch(quadruple_manager.goto_main_index, quadruple_manager.next_quad())

def p_start_goto(p):
    'start_goto : empty'
    # Generar GOTO main al principio
    if quadruple_manager.next_quad() == 0:
        goto_main = quadruple_manager.add_quadruple('goto', '', '', '')
        quadruple_manager.goto_main_index = goto_main

def p_fill_goto_main(p):
    'fill_goto_main : empty'
    # Este punto se alcanza después de todas las funciones
    # El parche real se hace en start_main
    pass

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
            scope_type = 'global' if function_directory.current_function == 'global' else 'local'
            address = current_scope.add_variable(var_name, var_type, scope_type)
            # Sincronizar con quadruple_manager
            quadruple_manager.address_table[var_name] = address
            quadruple_manager.address_to_name[address] = var_name
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
    'func : func_header LLAVEIZQ vars cuerpo LLAVEDER'
    # func_header ya creó el scope y registró parámetros
    
    # Generar ENDFUNC al final de la función
    quadruple_manager.add_endfunc()
    
    function_directory.set_current_function('global')
    p[0] = ('func', p[1]['type'], p[1]['name'], p[1]['params'], p[3], p[4])

def p_func_header(p):
    'func_header : func_tipo ID PARIZQ params PARDER'
    return_type = p[1]
    func_name = p[2]
    parameters = p[4]
    
    try:
        function_directory.add_function(func_name, return_type, [])
        function_directory.set_current_function(func_name)
        
        # Marcar inicio de cuádruplos de la función
        start_quad = quadruple_manager.next_quad()
        function_directory.set_start_quad(func_name, start_quad)
        
        # Si tiene retorno, sincronizar la variable global del nombre de la función
        if return_type != 'nula':
            # La variable ya fue creada en symbol_table.add_function
            # Necesitamos obtener su dirección y registrarla en quadruple_manager
            var_info = function_directory.global_scope.get_variable(func_name)
            if var_info:
                quadruple_manager.address_table[func_name] = var_info['address']
                quadruple_manager.address_to_name[var_info['address']] = func_name
        
        for param_name, param_type in parameters:
            function_directory.add_parameter(func_name, param_name, param_type)
            # Obtener la dirección recién creada para el parámetro
            func_info = function_directory.get_function(func_name)
            param_address = func_info['parameters'][-1]['address']
            # Sincronizar con quadruple_manager
            quadruple_manager.address_table[param_name] = param_address
            quadruple_manager.address_to_name[param_address] = param_name
            
        print(f"✓ Función declarada: {func_name} -> {return_type}")
    except Exception as e:
        print(f"✗ Error semántico: {e}")
        raise
        
    p[0] = {'type': return_type, 'name': func_name, 'params': parameters}

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
    var_name = p[1]
    
    # Obtener el resultado de la expresión (último temporal generado)
    # The expression rule pushes the result's address onto the operands_stack
    if quadruple_manager.operands_stack:
        result_operand_address = quadruple_manager.operands_stack.pop()
        # Pop its type too
        if quadruple_manager.types_stack:
            quadruple_manager.types_stack.pop()
    else:
        raise Exception("Error semántico: No hay resultado de expresión para asignar.")
    
    # Verificar que la variable existe y obtener su dirección
    current_scope = function_directory.get_current_scope()
    var_info = current_scope.get_variable(var_name)
    
    if var_info is None:
        raise Exception(f"Variable '{var_name}' no declarada")
    
    # Generar cuádruplo de asignación usando la dirección de la variable
    quadruple_manager.add_quadruple('=', result_operand_address, '', var_info['address'])
    
    p[0] = ('asigna', p[1], p[3])

def p_condicion(p):
    'condicion : SI PARIZQ expresion PARDER cuerpo seen_if_body sino PUNTOCOMA'
    # Parchear el GOTO que salta el sino (generado en seen_if_body)
    end_jump = quadruple_manager.pop_jump()
    quadruple_manager.patch(end_jump, quadruple_manager.next_quad())
    p[0] = ('condicion', p[3], p[5], p[7])

def p_seen_if_body(p):
    'seen_if_body : empty'
    # Generar GOTO para saltar el bloque sino
    goto_end = quadruple_manager.add_quadruple('goto', '', '', '')
    
    # Parchear el GOTOF de la condición para que salte aquí (inicio del sino)
    # El GOTOF está en la pila (empujado en p_expresion)
    false_jump = quadruple_manager.pop_jump()
    quadruple_manager.patch(false_jump, quadruple_manager.next_quad())
    
    # Empujar el GOTO end para parchearlo al final
    quadruple_manager.push_jump(goto_end)

def p_sino(p):
    '''sino : SINO cuerpo
            | empty'''
    p[0] = p[2] if len(p) > 2 else None

def p_seen_mientras(p):
    'seen_mientras : empty'
    # Marcar inicio del ciclo
    quadruple_manager.push_jump(quadruple_manager.next_quad())

def p_ciclo(p):
    'ciclo : MIENTRAS seen_mientras PARIZQ expresion PARDER HAZ cuerpo PUNTOCOMA'
    # Punto neurálgico: Cuádruplos para ciclo con GOTOs
    # Al final del cuerpo del ciclo, generar GOTO al inicio
    return_quad = quadruple_manager.add_quadruple('goto', '', '', '')
    
    # El orden en la pila es: [start_quad, gotof_quad]
    # Así que primero sacamos gotof_quad (tope)
    false_jump = quadruple_manager.pop_jump()
    
    # Luego sacamos start_quad
    start_quad = quadruple_manager.pop_jump()
    
    # Parchear el GOTO de retorno al inicio del ciclo
    if start_quad is not None:
        quadruple_manager.patch(return_quad, start_quad)
    
    # Parchear el gotof (si la condición es falsa) al final
    if false_jump is not None:
        quadruple_manager.patch(false_jump, quadruple_manager.next_quad())
    
    p[0] = ('ciclo', p[4], p[7])

def p_llamada(p):
    'llamada : ID PARIZQ argumentos PARDER'
    func_name = p[1]
    arguments = p[3]
    
    try:
        arg_types = []
        arg_addresses = []
        
        # Extraer direcciones y tipos de la pila (están en orden inverso)
        for _ in range(len(arguments)):
            if quadruple_manager.operands_stack:
                arg_addresses.append(quadruple_manager.operands_stack.pop())
                arg_types.append(quadruple_manager.types_stack.pop())
        
        # Revertir para tener el orden correcto
        arg_addresses.reverse()
        arg_types.reverse()
        
        function_directory.validate_call(func_name, arg_types)
        func_info = function_directory.get_function(func_name)
        
        # Generar ERA
        quadruple_manager.add_era(func_name)
        
        # Generar PARAMs
        for i, arg_addr in enumerate(arg_addresses):
            param_info = func_info['parameters'][i]
            dest_addr = param_info['address']
            quadruple_manager.add_param(arg_addr, dest_addr)
            
        # Generar GOSUB
        quadruple_manager.add_gosub(func_name, func_info['start_quad'])
        
        # Si tiene retorno, asignar a temporal
        if func_info['return_type'] != 'nula':
            # Obtener dirección de la variable global de retorno
            ret_var_addr = quadruple_manager.get_variable_address(func_name, func_info['return_type'], 'global')
            # Generar temporal para el resultado
            temp_name, temp_addr = quadruple_manager.new_temp(func_info['return_type'])
            # Asignar valor de retorno al temporal: temp = func_name
            quadruple_manager.add_quadruple('=', ret_var_addr, '', temp_addr)
            # Poner temporal en pila de operandos
            quadruple_manager.push_operand(temp_name, func_info['return_type'])
            
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

# ... (skip to p_imprime) ...

def p_imprime(p):
    'imprime : ESCRIBE PARIZQ imprime_lista PARDER'
    # La lista p[3] tiene los elementos en orden: [exp1, "lit", exp2]
    # La pila de operandos tiene los resultados de las expresiones en orden: [res_exp1, res_exp2]
    # (Los literales de string no ponen nada en la pila)
    
    # Necesitamos correlacionar los elementos de la lista con la pila.
    # Como la pila es LIFO, si iteramos la lista en reverso, coincidiremos con el tope de la pila.
    
    valores_a_imprimir = []
    
    for elemento in reversed(p[3]):
        if isinstance(elemento, str) and elemento.startswith('"'):
            # Es un letrero literal, no consume pila
            valores_a_imprimir.append(elemento)
        else:
            # Es una expresión, consume un valor de la pila
            if quadruple_manager.operands_stack:
                value_addr = quadruple_manager.operands_stack.pop()
                if quadruple_manager.types_stack:
                    quadruple_manager.types_stack.pop()
                valores_a_imprimir.append(value_addr)
            else:
                raise Exception("Error interno: Pila de operandos vacía al generar print")
    
    # Ahora valores_a_imprimir tiene [res_exp2, "lit", res_exp1]
    # Lo invertimos para tener el orden original
    valores_a_imprimir.reverse()
    
    # Generar cuádruplos
    for valor in valores_a_imprimir:
        quadruple_manager.add_quadruple('print', valor, '', '')
        
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
    # Verificar si es un letrero usando el tipo del token
    if p.slice[1].type == 'LETRERO':
        # Es un letrero, agregar comillas para que p_imprime lo reconozca
        p[0] = f'"{p[1]}"'
    else:
        # Es una expresión
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
              | PARIZQ expresion PARDER
              | llamada'''
    if len(p) == 2:
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
        elif isinstance(p[1], tuple) and p[1][0] == 'llamada':
            # Llamada a función (ya manejada en p_llamada)
            # If the function returns 'nula', it cannot be used in an expression
            return_type = p[1][3]
            if return_type == 'nula':
                raise Exception("No se puede usar una función 'nula' en una expresión")
            p[0] = 'llamada' # The result of the call is already pushed to operand stack
        else:
            # ID de variable
            var_name = p[1]
            current_scope = function_directory.get_current_scope()
            var_info = current_scope.get_variable(var_name)
            
            if var_info is None:
                raise Exception(f"Variable '{var_name}' no declarada")
            
            # Usar la dirección de la variable directamente
            quadruple_manager.push_address(var_info['address'], var_info['type'])
            p[0] = 'variable'
    else:
        # Expresión entre paréntesis: (expresion)
        p[0] = p[2]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en '{p.value}' (tipo: {p.type}, línea {p.lineno})"
        print(error_msg)
        raise Exception(error_msg)
    else:
        error_msg = "Error de sintaxis: fin de archivo inesperado"
        print(error_msg)
        raise Exception(error_msg)

parser = yacc.yacc()