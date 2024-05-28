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
    '''select_statement : SELECT opt_distinct select_list FROM table_name opt_join_clause opt_where_clause opt_group_by_clause opt_order_by_clause opt_limit_clause '''
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
                   | aggregate_function COMMA select_list
                   | aggregate_function as_clause
                   | aggregate_function as_clause COMMA select_list
                   | ALL    '''
    # if len(p) == 2:
    #     p[0] = p[1]
    # elif len(p) == 3:
    #     p[0] = f"{p[1]} {p[2]}"
    # elif len(p) == 4:
    #     p[0] = f"{p[1]}, {p[3]}"
    # else:
    #     p[0] = ' '.join([str(x) for x in p[1:] if x])
    p[0] = ' '.join([str(x) for x in p[1:] if x])

def p_opt_distinct(p):
    '''opt_distinct : DISTINCT
                    | empty'''
    p[0]=p[1]
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

def p_opt_limit_clause(p):
    '''opt_limit_clause : LIMIT NUMBER
                        | empty'''
    p[0] = f"LIMIT {p[2]}" if p[1] else ''

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
    elif p[2][0:2] == 'IN':
        p[0] = f"{p[1]} {p[2]}"
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
                  | column_name comparator column_name logical_operator expression
                  | column_name comparator LPAREN select_statement RPAREN
                  | column_name comparator LPAREN select_statement RPAREN logical_operator expression '''
    # if len(p) == 4:
    #     p[0] = f"{p[1]} {p[2]} {p[3]}"
    # else:
    #     p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]} {p[5]}"
    p[0] = ' '.join([str(x) for x in p[1:] if x])



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
    '''column_name : IDENTIFIER
                    | table_name DOT IDENTIFIER'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0]=f"{p[1]} . {p[2]}"


def p_identifier(p):
    '''identifier : IDENTIFIER'''
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
    '''opt_group_by_clause : GROUP BY group_by_list opt_having_clause
                           | empty'''
    p[0] = ' '.join([str(x) for x in p[1:] if x])



def p_group_by_list(p):
    '''group_by_list : column_name
                     | column_name COMMA group_by_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_opt_having_clause(p):
    '''opt_having_clause : HAVING condition
                         | HAVING aggregate_function having_expression
                         | empty'''
    p[0] = ' '.join([str(x) for x in p[1:] if x])

def p_having_expression(p):
    '''having_expression : comparator value
                  | comparator value logical_operator expression
                  | comparator LPAREN select_statement RPAREN
                  | comparator LPAREN select_statement RPAREN logical_operator expression '''

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
    '''in_list : IN LPAREN values_list RPAREN
                | IN LPAREN select_statement RPAREN'''
    p[0] = f"IN ({p[3]})"

def p_pattern(p):
    '''pattern : STRING'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = ''

def p_create_statement(p):
    '''create : CREATE DATABASE database_name opt_semicolon
                | CREATE TABLE table_name create_table_list opt_semicolon
                | CREATE TABLE table_name AS select_statement '''
    if len(p) == 5:
        p[0] = f"CREATE DATABASE {p[3]} {p[4]}"
    elif p[4]=='AS':
        p[0] = f"CREATE TABLE {p[3]} AS {p[5]}"
    else:
        p[0] = f"CREATE TABLE {p[3]} {p[4]} {p[5]}"
def p_database_name(p):
    '''database_name: IDENTIFIER'''
    p[0] = p[1]

def p_create_table_list(p):
    '''create_table_list : LPAREN table_name_type_optconstraint_list opt_comma opt_constraint_list RPAREN'''
    p[0] = f"({p[2]}{p[3]}{p[4]})"


def p_table_name_type_optconstraint_list(p):
    '''table_name_type_optconstraint_list : column_name column_type opt_constraint_clause
                        | column_name column_type opt_constraint_clause COMMA table_name_type_optconstraint_list'''
    if len(p) == 4:
        p[0] = f"{p[1]}{p[2]}{p[3]}"
    else:
        p[0] = f"{p[1]} {p[2]} {p[3]},{p[5]}"

def p_column_type(p):
    '''column_type : INT | INTEGER | FLOAT | DOUBLE LEFTPAREN NUMBER COMMA NUMBER RIGHTPAREN | DECIMAL LEFTPAREN NUMBER COMMA NUMBER RIGHTPAREN | DEC LEFTPAREN NUMBER COMMA NUMBER RIGHTPAREN | NUMERIC
    | CHAR LEFTPAREN NUMBER RIGHTPAREN | CHARACTER LEFTPAREN NUMBER RIGHTPAREN | VARCHAR LEFTPAREN NUMBER RIGHTPAREN | TEXT
    | DATE | TIME | TIMESTAMP | DATETIME | INTERVAL | YEAR
    | BOOL | BOOLEAN | BINARY LEFTPAREN NUMBER RIGHTPAREN | VARBINARY LEFTPAREN NUMBER RIGHTPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 7:
        p[0] = f"{p[1]}(NUMBER,NUMBER)"
    else:
        p[0] = f"{p[1]}(NUMBER)"

# def p_opt_column_type_list(p):
#     '''opt_column_type_list : empty
#                        | column_type_list'''
#     p[0] = p[1] if p[1] else ''

def p_drop_statement(p):
    '''drop_statement: DROP COLUMN column_name
            | DROP CONSTRAINT constraint_name
            | DROP PRIMARY KEY
            | DROP FOREIGN KEY key_name
            | DROP CHECK check_name
            | DROP DATABASE database_name
            | DROP TABLE table_name'''
    if p[2] == 'COLUMN':
        p[0] = f"DROP COLUMN {p[3]}"
    elif p[2] == 'CONSTRAINT':
        p[0] = f"DROP CONSTRAINT {p[3]}"
    elif p[2] == 'PRIMARY':
        p[0] = f"DROP PRIMARY KEY"
    elif p[2] == 'FOREIGN':
        p[0] = f"DROP FOREIGN KEY {p[4]}"
    elif p[2] == 'CHECK':
        p[0] = f"DROP CHECK {p[3]}"
    elif p[2] == 'DATABASE':
        p[0] = f"DROP DATABASE {p[3]}"
    else:
        p[0] = f"DROP TABLE {p[3]}"

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
            | ALTER TABLE table_name ALTER COLUMN column_name column_type opt_semicolon'''
    if len(p) == 6:
        p[0] = f"ALTER TABLE {p[3]}{p[4]}{p[5]}"
    else:
        p[0] = f"ALTER TABLE {p[3]} ALTER COLUMN {p[6]} {p[7]} {p[8]}"

def p_add_statement(p):
    '''add_statement: ADD column_name column_type opt_semicolon
                    | ADD constraint_clause opt_semicolon'''
    if len(p) == 5:
        p[0] = f"ADD {p[2]} {p[3]} {p[4]}"
    else:
        p[0] = f"ADD {p[2]}{p[3]}"

def p_constraint_clause(p):
    '''constraint_clause: CONSTRAINT constraint_name constraint_type'''
    p[0] = f"CONSTRAINT {p[2]}{p[3]}"
def p_constraint_type(p):
    '''constraint_type: NOT NULL | UNIQUE LEFTPAREN column_name_list RIGHTPAREN'''

def p_opt_constraint_type(p):
    '''opt_constraint_type: empty | constraint_type'''
    p[0]=p[1]
def p_opt_constraint_list(p):
    '''opt_constraint_list: empty | constraint_clause'''
    p[0] = p[1]

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
    try:
        parser = yacc.yacc()
    except Exception as e:
        # Ignoruj wszystkie błędy
        pass
    return current_table_name

# print(parser.parse("SELECT students.name, students.age, departments.name FROM students JOIN departments ON "
#                    "students.department_id = departments.id;"))