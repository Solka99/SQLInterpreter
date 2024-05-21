import ply.yacc as yacc
from tokens_ import tokens# zimportowana lista tokenów

# Definicje gramatyki
def p_sql_statement(p):
    '''sql_statement : select_statement
                     '''
    p[0] = p[1]

# def p_sql_statement(p):
#     '''sql_statement : select_statement
#                      | insert_statement
#                      | update_statement
#                      | delete_statement'''
#     p[0] = p[1]

def p_select_statement(p):
    '''select_statement : SELECT select_list FROM table_name opt_join_clause opt_where_clause opt_group_by_clause opt_order_by_clause'''
    p[0] = p[1:]

# def p_insert_statement(p):
#     '''insert_statement : INSERT INTO table_name LPAREN opt_column_list RPAREN VALUES LPAREN values_list RPAREN'''
#     p[0] = ('insert', p[3], p[5], p[8])
#
# def p_update_statement(p):
#     '''update_statement : UPDATE table_name SET set_list opt_where_clause'''
#     p[0] = ('update', p[2], p[4], p[5])
#
# def p_delete_statement(p):
#     '''delete_statement : DELETE FROM table_name opt_where_clause'''
#     p[0] = ('delete', p[3], p[4])

def p_select_list(p):
    '''select_list : column_name
                   | column_name as_clause
                   | column_name COMMA select_list
                   | aggregate_function'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [(p[1], p[2])]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_column_list(p):
    '''column_list : LPAREN column_name_list RPAREN'''
    p[0] = p[2]

def p_column_name_list(p):
    '''column_name_list : column_name
                        | column_name COMMA column_name_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_opt_column_list(p):
    '''opt_column_list : empty
                       | column_list'''
    p[0] = p[1]

def p_values_list(p):
    '''values_list : value
                   | value COMMA values_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_set_list(p):
    '''set_list : column_name EQUALS value
                | column_name EQUALS value COMMA set_list'''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3])] + p[5]

def p_condition(p):
    '''condition : expression
                 | column_name in_list
                 | column_name BETWEEN value AND value
                 | column_name LIKE pattern
                 | column_name IS NULL'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2]=='IN':
        p[0] = ('in', p[1], p[2])
    elif p[2] == 'BETWEEN':
        p[0] = p[1:]      #DECYZJA KTÓRE PODEJŚCIE LEPSZE
    elif p[2] == 'LIKE':
        p[0] = ('like', p[1], p[3])
    else:
        p[0] = ('IS NULL', p[1])

def p_expression(p):
    '''expression : column_name comparator value
                  | column_name comparator column_name'''
    p[0] = (p[2], p[1], p[3])

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
    '''table_name : identifier'''
    p[0] = p[1]

def p_column_name(p):
    '''column_name : identifier'''
    p[0] = p[1]

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = p[1]

def p_as_clause(p):
    '''as_clause : AS identifier'''
    p[0] = p[2]

def p_opt_join_clause(p):
    '''opt_join_clause : join_clause
                       | empty'''
    p[0] = p[1]

def p_join_clause(p):
    '''join_clause : join_type JOIN table_name ON condition'''
    p[0] = (p[1], p[3], p[5])

def p_join_type(p):
    '''join_type : INNER
                 | LEFT
                 | RIGHT'''
    p[0] = p[1]

def p_opt_where_clause(p):
    '''opt_where_clause : WHERE condition
                         | empty'''
    p[0]=p[1:]


def p_opt_group_by_clause(p):
    '''opt_group_by_clause : GROUP_BY group_by_list
                           | empty'''
    p[0] = p[1]

def p_group_by_list(p):
    '''group_by_list : column_name
                     | column_name COMMA group_by_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_opt_order_by_clause(p):
    '''opt_order_by_clause : ORDER_BY order_by_list
                           | empty'''
    p[0] = p[1]

def p_order_by_list(p):
    '''order_by_list : order_specification
                     | order_specification COMMA order_by_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_order_specification(p):
    '''order_specification : column_name order_direction'''
    p[0] = (p[1], p[2])

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
    p[0] = (p[1], p[3])

def p_in_list(p):
    '''in_list : IN LPAREN values_list RPAREN'''
    p[0] = p[3]

def p_pattern(p):
    '''pattern : STRING'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Tworzenie parsera
parser = yacc.yacc()

# Testowanie parsera
sql = '''
SELECT column1,abc FROM table WHERE abc = 10
'''

result = parser.parse(sql)
print(result)
