import ply.yacc as yacc
from patito_lexer import tokens, lexer

precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
    ('nonassoc', 'MENOR', 'MAYOR', 'IGUAL', 'DIFERENTE'),
)

def p_programa(p):
    'programa : PROGRAMA ID PUNTOCOMA vars funcs INICIO cuerpo FIN'
    p[0] = ('programa', p[2], p[4], p[5], p[7])
    print("✓ Programa válido")

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

# ✅ Quitamos el PUNTOCOMA al final del bloque
def p_func(p):
    'func : func_tipo ID PARIZQ params PARDER LLAVEIZQ vars cuerpo LLAVEDER'
    p[0] = ('func', p[1], p[2], p[4], p[7], p[8])

def p_func_tipo(p):
    '''func_tipo : NULA
                 | tipo'''
    p[0] = p[1]

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
    p[0] = ('param', p[1], p[3])

# ✅ Acepta cuerpo con o sin llaves
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
    p[0] = ('llamada', p[1], p[3])

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
        p[0] = p[1]
    else:
        p[0] = ('op_relacional', p[2], p[1], p[3])

def p_exp(p):
    '''exp : termino
           | exp MAS termino
           | exp MENOS termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('op_aritmetica', p[2], p[1], p[3])

def p_termino(p):
    '''termino : factor
               | termino MULT factor
               | termino DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('op_aritmetica', p[2], p[1], p[3])

def p_factor(p):
    '''factor : CTE_ENT
              | CTE_FLOAT
              | ID
              | PARIZQ expresion PARDER
              | llamada
              | MENOS factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('negativo', p[2])
    else:
        p[0] = p[2]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()
