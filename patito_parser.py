import ply.yacc as yacc
from patito_lexer import tokens, lexer

# Importar las estructuras semánticas
from semantic_cube import semantic_cube
from symbol_table import function_directory

precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
    ('nonassoc', 'MENOR', 'MAYOR', 'IGUAL', 'DIFERENTE'),
)

def p_programa(p):
    'programa : PROGRAMA ID PUNTOCOMA vars funcs INICIO cuerpo FIN'
    # Punto neurálgico: Programa principal
    p[0] = ('programa', p[2], p[4], p[5], p[7])
    print("✓ Programa válido - Análisis semántico completado")

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
    # Punto neurálgico: Declaración de variables
    var_type = p[3]
    for var_name in p[1]:
        try:
            # Agregar variable al ámbito actual
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
    # Punto neurálgico: Declaración de función
    return_type = p[1]
    func_name = p[2]
    parameters = p[4]
    
    try:
        # Agregar función al directorio
        function_directory.add_function(func_name, return_type, [])
        
        # Establecer como función actual y agregar parámetros
        function_directory.set_current_function(func_name)
        for param_name, param_type in parameters:
            function_directory.add_parameter(func_name, param_name, param_type)
        
        print(f"✓ Función declarada: {func_name} -> {return_type}")
        
    except Exception as e:
        print(f"✗ Error semántico: {e}")
        raise
    
    p[0] = ('func', p[1], p[2], p[4], p[7], p[8])
    
    # Regresar al ámbito global después de procesar la función
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
    # Punto neurálgico: Parámetro de función
    p[0] = (p[1], p[3])  # (nombre, tipo)

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
    # Punto neurálgico: Asignación
    var_name = p[1]
    expr_result = p[3]  # Puede ser tipo o tupla
    
    # Obtener el tipo de la expresión
    if isinstance(expr_result, tuple) and len(expr_result) > 1:
        # Es una operación, obtener el último elemento que es el tipo
        expr_type = expr_result[-1] if isinstance(expr_result[-1], str) else 'entero'
    else:
        # Es un tipo simple
        expr_type = expr_result
    
    # Verificar que la variable existe
    current_scope = function_directory.get_current_scope()
    var_info = current_scope.get_variable(var_name)
    
    if var_info is None:
        raise Exception(f"Variable '{var_name}' no declarada")
    
    # Verificar compatibilidad de tipos usando el cubo semántico
    if not semantic_cube.is_operation_valid(var_info['type'], expr_type, '='):
        raise Exception(f"Tipos incompatibles en asignación: {var_info['type']} = {expr_type}")
    
    p[0] = ('asigna', p[1], p[3])

def p_condicion(p):
    'condicion : SI PARIZQ expresion PARDER cuerpo sino PUNTOCOMA'
    p[0] = ('condicion', p[3], p[5], p[6])

def p_sino(p):
    '''sino : SINO cuerpo
            | empty'''
    p[0] = p[2] if len(p) > 2 else None

def p_ciclo(p):
    'ciclo : MIENTRAS PARIZQ expresion PARDER HAZ cuerpo PUNTOCOMA'
    p[0] = ('ciclo', p[3], p[6])

def p_llamada(p):
    'llamada : ID PARIZQ argumentos PARDER'
    # Punto neurálgico: Llamada a función
    func_name = p[1]
    arguments = p[3]  # Lista de tipos de argumentos
    
    # Validar que la función existe y los argumentos son correctos
    try:
        # Extraer tipos de los argumentos
        arg_types = []
        for arg in arguments:
            if isinstance(arg, tuple) and len(arg) > 1:
                arg_type = arg[-1] if isinstance(arg[-1], str) else 'entero'
            else:
                arg_type = arg
            arg_types.append(arg_type)
        
        function_directory.validate_call(func_name, arg_types)
        func_info = function_directory.get_function(func_name)
        p[0] = ('llamada', p[1], p[3], func_info['return_type'])  # Incluir tipo de retorno
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
                 | exp DIFERENTE exp'''
    if len(p) == 2:
        p[0] = p[1]  # Tipo de la expresión simple
    else:
        # Punto neurálgico: Operación relacional
        left_result = p[1]
        right_result = p[3]
        operator = p[2]
        
        # Obtener tipos de los operandos
        left_type = left_result if isinstance(left_result, str) else 'entero'
        right_type = right_result if isinstance(right_result, str) else 'entero'
        
        # Validar tipos usando cubo semántico
        if not semantic_cube.is_operation_valid(left_type, right_type, operator):
            raise Exception(f"Tipos incompatibles en operación {operator}: {left_type} y {right_type}")
        
        result_type = semantic_cube.get_result_type(left_type, right_type, operator)
        p[0] = ('op_relacional', p[2], p[1], p[3], result_type)

def p_exp(p):
    '''exp : termino
           | exp MAS termino
           | exp MENOS termino'''
    if len(p) == 2:
        p[0] = p[1]  # Tipo del término
    else:
        # Punto neurálgico: Operación aritmética
        left_result = p[1]
        right_result = p[3]
        operator = p[2]
        
        # Obtener tipos de los operandos
        left_type = left_result if isinstance(left_result, str) else 'entero'
        right_type = right_result if isinstance(right_result, str) else 'entero'
        
        # Validar tipos usando cubo semántico
        if not semantic_cube.is_operation_valid(left_type, right_type, operator):
            raise Exception(f"Tipos incompatibles en operación {operator}: {left_type} y {right_type}")
        
        result_type = semantic_cube.get_result_type(left_type, right_type, operator)
        p[0] = ('op_aritmetica', p[2], p[1], p[3], result_type)

def p_termino(p):
    '''termino : factor
               | termino MULT factor
               | termino DIV factor'''
    if len(p) == 2:
        p[0] = p[1]  # Tipo del factor
    else:
        # Punto neurálgico: Operación aritmética
        left_result = p[1]
        right_result = p[3]
        operator = p[2]
        
        # Obtener tipos de los operandos
        left_type = left_result if isinstance(left_result, str) else 'entero'
        right_type = right_result if isinstance(right_result, str) else 'entero'
        
        # Validar tipos usando cubo semántico
        if not semantic_cube.is_operation_valid(left_type, right_type, operator):
            raise Exception(f"Tipos incompatibles en operación {operator}: {left_type} y {right_type}")
        
        result_type = semantic_cube.get_result_type(left_type, right_type, operator)
        p[0] = ('op_aritmetica', p[2], p[1], p[3], result_type)

def p_factor(p):
    '''factor : CTE_ENT
              | CTE_FLOAT
              | ID
              | PARIZQ expresion PARDER
              | llamada
              | MENOS factor'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = 'entero'  # Tipo de constante entera
        elif isinstance(p[1], float):
            p[0] = 'flotante'  # Tipo de constante flotante
        elif isinstance(p[1], str) and p[1] not in ['entero', 'flotante']:
            # Es un ID - verificar que existe y obtener su tipo
            var_name = p[1]
            current_scope = function_directory.get_current_scope()
            var_info = current_scope.get_variable(var_name)
            
            if var_info is None:
                raise Exception(f"Variable '{var_name}' no declarada")
            
            p[0] = var_info['type']
        else:
            p[0] = p[1]  # Para llamadas a función (ya incluye el tipo)
    elif len(p) == 3:
        # Factor negativo - mantener el mismo tipo
        factor_result = p[2]
        if isinstance(factor_result, str):
            p[0] = factor_result
        else:
            p[0] = 'entero'  # Por defecto
    else:
        p[0] = p[2]  # Tipo de la expresión entre paréntesis

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()