import ply.lex as lex

# Lista nazw tokenów
tokens = (
    'SELECT', 'FROM', 'WHERE', 'IN', 'BETWEEN', 'LIKE', 'AS',
    'JOIN', 'ON', 'AND', 'OR', 'ORDER', 'BY', 'GROUP', 'INNER', 'LEFT',
    'RIGHT', 'ASC', 'DESC', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'COMMA',
    'SEMICOLON', 'DOT', 'LPAREN', 'RPAREN', 'EQUALS', 'NOT_EQUALS',
    'LESS_THAN', 'LESS_OR_EQUAL', 'GREATER_THAN', 'GREATER_OR_EQUAL',
    'NUMBER', 'STRING', 'IDENTIFIER', 'INSERT', 'INTO','BOOLEAN','IS','NULL','UPDATE','SET','DELETE','VALUES','ALL',
    'HAVING','DISTINCT','LIMIT','INT','INTEGER','REAL','NUMERIC','TEXT','BLOB','UNION'
)

# Definicje reguł leksykalnych
t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_IN = r'IN'
t_BETWEEN = r'BETWEEN'
t_LIKE = r'LIKE'
t_IS=r'IS'
t_NULL=r'NULL'
t_AS = r'AS'
t_JOIN = r'JOIN'
t_ON = r'ON'
t_AND = r'AND'
t_OR = r'OR'
t_ORDER = r'ORDER'
t_GROUP = r'GROUP'
t_BY = r'BY'
t_INNER = r'INNER'
t_LEFT = r'LEFT'
t_RIGHT = r'RIGHT'
t_ASC = r'ASC'
t_DESC = r'DESC'
t_COUNT = r'COUNT'
t_SUM = r'SUM'
t_AVG = r'AVG'
t_MAX = r'MAX'
t_MIN = r'MIN'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_LESS_THAN = r'<'
t_LESS_OR_EQUAL = r'<='
t_GREATER_THAN = r'>'
t_GREATER_OR_EQUAL = r'>='
t_INSERT=r'INSERT'
t_INTO=r'INTO'
# t_BOOLEAN=r'BOOLEAN'
t_UPDATE=r'UPDATE'
t_SET=r'SET'
t_DELETE=r'DELETE'
t_VALUES=r'VALUES'
t_ALL=r'\*'
t_HAVING=r'HAVING'
t_DISTINCT=r'DISTINCT'
t_LIMIT=r'LIMIT'
t_INT=r'INT'
t_INTEGER=r'INTEGER'
t_REAL=r'REAL'
t_NUMERIC=r'NUMERIC'
t_TEXT=r'TEXT'
t_BLOB=r'BLOB'
t_UNION=r'UNION'

def t_NUMBER(t):
    r'[0-9]+(\.[0-9]+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_STRING(t):
    #r'\'[A-Za-z][A-Za-z0-9_]*\''
    r'\'(?:[^\']|\'\')*\''
    return t
def t_BOOLEAN(t):
    r'\b(TRUE|FALSE)\b'
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    else:
        t.type = 'IDENTIFIER'
    return t

# Ignorowanie białych znaków
t_ignore = ' \t'

# Reguła dla nowej linii
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Obsługa błędów
def t_error(t):
    print(f"Nieznany znak '{t.value[0]}'")
    t.lexer.skip(1)

# Tworzenie leksyka
lexer = lex.lex()

# lexer.input('select major from students where major=\'Physics\'')
#
# for tok in lexer:
#     print(tok)
