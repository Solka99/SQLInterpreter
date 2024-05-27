import ply.yacc as yacc
from tokens_ import tokens

current_table_name = None

# Definicje gramatyki
def p_statements(p):
    '''statements : sql_statement SEMICOLON statements
                  | sql_statement opt_semicolon'''
    if len(p) == 4:
        p[0] = [p[1] + ';'] + p[3]
    else:
        p[0] = [p[1] + p[2]]


def p_sql_statement(p):
    '''sql_statement : select_statement
                     | insert_statement
                     | update_statement
                     | delete_statement'''
    p[0] = p[1]


def p_select_statement(p):
    '''select_statement : SELECT select_list FROM table_name opt_join_clause opt_where_clause opt_group_by_clause opt_order_by_clause '''
    p[0] = ' '.join([str(x) for x in p[1:] if x])


def p_insert_statement(p):
    '''insert_statement : INSERT INTO table_name opt_column_list VALUES LPAREN values_list RPAREN '''
    p[0] = ' '.join([str(x) for x in p[1:] if x])


def p_update_statement(p):
    '''update_statement : UPDATE table_name SET set_list opt_where_clause '''
    p[0] = ' '.join([str(x) for x in p[1:] if x])


def p_delete_statement(p):
    '''delete_statement : DELETE FROM table_name opt_where_clause '''
    p[0] = ' '.join([str(x) for x in p[1:] if x])


def p_opt_semicolon(p):
    '''opt_semicolon : SEMICOLON
                    | empty '''
    p[0] = p[1] if p[1] else ''


def p_select_list(p):
    '''select_list : column_name
                   | column_name as_clause
                   | column_name COMMA select_list
                   | aggregate_function
                   | EVERY    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f"{p[1]} {p[2]}"
    elif len(p) == 4:
        p[0] = f"{p[1]}, {p[3]}"
    else:
        p[0] = p[1]

def p_column_list(p):
    '''column_list : LPAREN column_name_list RPAREN'''
    p[0] = f"({p[2]})"

def p_column_name_list(p):
    '''column_name_list : column_name
                        | column_name COMMA column_name_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_opt_column_list(p):
    '''opt_column_list : empty
                       | column_list'''
    p[0] = p[1] if p[1] else ''

def p_values_list(p):
    '''values_list : value
                   | value COMMA values_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_set_list(p):
    '''set_list : column_name EQUALS value
                | column_name EQUALS value COMMA set_list'''
    if len(p) == 4:
        p[0] = f"{p[1]} = {p[3]}"
    else:
        p[0] = f"{p[1]} = {p[3]}, {p[5]}"

def p_condition(p):
    '''condition : expression
                 | column_name in_list
                 | column_name BETWEEN value AND value
                 | column_name LIKE pattern
                 | column_name IS NULL'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == 'IN':
        p[0] = f"{p[1]} IN {p[3]}"
    elif p[2] == 'BETWEEN':
        p[0] = f"{p[1]} BETWEEN {p[3]} AND {p[5]}"
    elif p[2] == 'LIKE':
        p[0] = f"{p[1]} LIKE {p[3]}"
    else:
        p[0] = f"{p[1]} IS NULL"

def p_expression(p):
    '''expression : column_name comparator value
                  | column_name comparator column_name
                  | column_name comparator value logical_operator expression
                  | column_name comparator column_name logical_operator expression'''
    if len(p) == 4:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:
        p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]} {p[5]}"

def p_logical_operator(p):
    '''logical_operator : AND
                        | OR'''
    p[0] = p[1]

def p_comparator(p):
    '''comparator : EQUALS
                  | NOT_EQUALS
                  | LESS_THAN
                  | LESS_OR_EQUAL
                  | GREATER_THAN
                  | GREATER_OR_EQUAL'''
    p[0] = p[1]

def p_value(p):
    '''value : NUMBER
             | STRING
             | BOOLEAN'''
    p[0] = p[1]

def p_table_name(p):
    '''table_name : IDENTIFIER'''
    global current_table_name
    current_table_name = p[1]
    p[0] = p[1]

def p_column_name(p):
    '''column_name : IDENTIFIER'''
    p[0] = p[1]


def p_as_clause(p):
    '''as_clause : AS IDENTIFIER'''
    p[0] = f"AS {p[2]}"

def p_opt_join_clause(p):
    '''opt_join_clause : join_clause
                       | empty'''
    p[0] = p[1] if p[1] else ''

def p_join_clause(p):
    '''join_clause : join_type JOIN table_name ON condition'''
    p[0] = f"{p[1]} JOIN {p[3]} ON {p[5]}"

def p_join_type(p):
    '''join_type : INNER
                 | LEFT
                 | RIGHT'''
    p[0] = p[1]

def p_opt_where_clause(p):
    '''opt_where_clause : WHERE condition
                         | empty'''
    p[0] = f"WHERE {p[2]}" if p[1] else ''

def p_opt_group_by_clause(p):
    '''opt_group_by_clause : GROUP BY group_by_list
                           | empty'''
    p[0] = f"GROUP BY {p[3]}" if p[1] else ''

def p_group_by_list(p):
    '''group_by_list : column_name
                     | column_name COMMA group_by_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_opt_order_by_clause(p):
    '''opt_order_by_clause : ORDER BY order_by_list
                           | empty'''
    p[0] = f"ORDER BY {p[3]}" if p[1] else ''

def p_order_by_list(p):
    '''order_by_list : order_specification
                     | order_specification COMMA order_by_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_order_specification(p):
    '''order_specification : column_name order_direction'''
    p[0] = f"{p[1]} {p[2]}"

def p_order_direction(p):
    '''order_direction : ASC
                       | DESC'''
    p[0] = p[1]

def p_aggregate_function(p):
    '''aggregate_function : COUNT LPAREN column_name RPAREN
                          | SUM LPAREN column_name RPAREN
                          | AVG LPAREN column_name RPAREN
                          | MAX LPAREN column_name RPAREN
                          | MIN LPAREN column_name RPAREN'''
    p[0] = f"{p[1]}({p[3]})"

def p_in_list(p):
    '''in_list : IN LPAREN values_list RPAREN'''
    p[0] = f"IN ({p[3]})"

def p_pattern(p):
    '''pattern : STRING'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = ''

def p_create_statement(p):
    '''create : CREATE DATABASE database_name opt_semicolon
                | CREATE TABLE table_name column_type_list opt_semicolon
                | CREATE TABLE table_name AS select_statement '''

def p_database_name(p):
    '''database_name: IDENTIFIER'''
    p[0] = p[1]

def p_column_type_list(p):
    '''column_type_list : LPAREN column_name_type_list RPAREN'''
    p[0] = f"({p[2]})"

def p_column_name_type_list(p):
    '''column_name_type_list : column_name column_type
                        | column_name column_type COMMA column_name_type_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_column_type(p):
    '''column_type : INT | INTEGER | FLOAT | DECIMAL | NUMERIC
    | CHAR(NUMBER) | CHARACTER(NUMBER) | VARCHAR(NUMBER) | CHARACTER VARYING(NUMBER) | TEXT
    | DATE | TIME | TIMESTAMP | DATETIME | INTERVAL
    | BOOLEAN | BINARY(NUMBER)'''

# def p_opt_column_type_list(p):
#     '''opt_column_type_list : empty
#                        | column_type_list'''
#     p[0] = p[1] if p[1] else ''

def p_drop_statement(p):
    '''drop: DROP COLUMN column_name
            | DROP CONSTRAINT constraint_name
            | DROP PRIMARY KEY
            | DROP FOREIGN KEY key_name
            | DROP CHECK check_name
            | DROP DATABASE database_name
            | DROP TABLE table_name'''

def p_constraint_name(p):
    '''constraint_name: IDENTIFIER'''
    p[0] = p[1]

def p_key_name(p):
    '''key_name: IDENTIFIER'''
    p[0] = p[1]

def p_check_name(p):
    '''check_name: IDENTIFIER'''
    p[0] = p[1]

def p_alter(p):
    '''alter: ALTER TABLE table_name add_statement opt_semicolon
            | ALTER TABLE table_name drop_statement opt_semicolon
            | ALTER TABLE table_name ALTER COLUMN column_name column_type'''

def p_add_statement(p):
    '''add_statement: TODO'''

def p_error(p):
    if p:
        # Uzyskiwanie poprzedniego tokenu ze stosu symboli
        prev_token = parser.symstack[-1] if len(parser.symstack) > 1 else None
        # Uzyskiwanie następnego tokenu jako bieżącego tokenu, ponieważ p jest bieżącym tokenem
        next_token = p

        if prev_token and prev_token.type == '$end':
            error_message = f"Unexpected end of input after '{prev_token.value}' (line {p.lineno}, position {p.lexpos})"
        elif next_token and next_token.type == '$end':
            error_message = f"Unexpected end of input before '{next_token.value}' (line {p.lineno}, position {p.lexpos})"
        elif prev_token and next_token:
            error_message = (f"Syntax error near '{prev_token.value}' and '{next_token.value}' "
                             f"(line {p.lineno}, position {p.lexpos})")
        elif prev_token:
            error_message = (f"Syntax error after '{prev_token.value}' "
                             f"(line {p.lineno}, position {p.lexpos})")
        elif next_token:
            error_message = (f"Syntax error before '{next_token.value}' "
                             f"(line {p.lineno}, position {p.lexpos})")
        else:
            error_message = (f"Syntax error at token '{p.value}' "
                             f"(line {p.lineno}, position {p.lexpos})")
    else:
        error_message = "Syntax error at EOF. Possibly missing keyword or token."

    raise SyntaxError(error_message)




# Tworzenie parsera
parser = yacc.yacc()

def update():
    parser = yacc.yacc()
    return current_table_name