import ply.lex as lex

# Lista de tokens
tokens = (
    # Palabras reservadas
    'PROGRAMA', 'INICIO', 'FIN', 'VARS', 'ENTERO', 'FLOTANTE',
    'MIENTRAS', 'ESCRIBE', 'HAZ', 'SI', 'SINO', 'NULA',
    # Identificadores y constantes
    'ID', 'CTE_ENT', 'CTE_FLOAT', 'LETRERO',
    # Símbolos
    'DOSPUNTOS', 'COMA', 'PUNTOCOMA',
    'LLAVEIZQ', 'LLAVEDER', 'PARIZQ', 'PARDER',
    'MAS', 'MENOS', 'MULT', 'DIV',
    'MENOR', 'MAYOR', 'DIFERENTE', 'IGUAL',
    'ASIGNACION'
)

# Expresiones regulares simples
t_DOSPUNTOS = r':'
t_COMA = r','
t_PUNTOCOMA = r';'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MENOR = r'<'
t_MAYOR = r'>'
t_DIFERENTE = r'!='
t_IGUAL = r'=='
t_ASIGNACION = r'='

t_ignore = ' \t'

# Palabras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'inicio': 'INICIO',
    'fin': 'FIN',
    'vars': 'VARS',
    'entero': 'ENTERO',
    'flotante': 'FLOTANTE',
    'mientras': 'MIENTRAS',
    'escribe': 'ESCRIBE',
    'haz': 'HAZ',
    'si': 'SI',
    'sino': 'SINO',
    'nula': 'NULA'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Flotante antes que entero
def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_LETRERO(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'/\*.*?\*/'
    pass

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def test_lexer(data):
    print("=== ANÁLISIS LÉXICO ===")
    lexer.input(data)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append((tok.type, tok.value, tok.lineno))
        print(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
    return tokens_list
