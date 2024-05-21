import ply.yacc as yacc
from tokens_ import tokens# zimportowana lista tokenów

# Definicje gramatyki
def p_sql_statement(p):
    '''sql_statement : select_statement
                    | insert_statement
                    | update_statement
                    | delete_statement
                     '''
    p[0] = p[1]

def p_select_statement(p):
    '''select_statement : SELECT select_list FROM table_name opt_join_clause opt_where_clause opt_group_by_clause opt_order_by_clause opt_semicolon'''
    p[0] = p[1:]

def p_insert_statement(p):
    '''insert_statement : INSERT INTO table_name opt_column_list VALUES LPAREN values_list RPAREN'''
    p[0] = p[1:]

def p_update_statement(p):
    '''update_statement : UPDATE table_name SET set_list opt_where_clause'''
    p[0] = p[1:]

def p_delete_statement(p):
    '''delete_statement : DELETE FROM table_name opt_where_clause'''
    p[0] = p[1:]

def p_opt_semicolon(p):
    '''opt_semicolon : SEMICOLON
                    | empty '''
    p[0] = p[1]
def p_select_list(p):
    '''select_list : column_name
                   | column_name as_clause
                   | column_name COMMA select_list
                   | aggregate_function
                   | ALL    '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1:]
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
        p[0] = p[1:]
    else:
        p[0] = p[1:4]+p[5]

def p_condition(p):
    '''condition : expression
                 | column_name in_list
                 | column_name BETWEEN value AND value
                 | column_name LIKE pattern
                 | column_name IS NULL'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2]=='IN':
        p[0] = p[1:]
    elif p[2] == 'BETWEEN':
        p[0] = p[1:]      #DECYZJA KTÓRE PODEJŚCIE LEPSZE
    elif p[2] == 'LIKE':
        p[0] = p[1:]
    else:
        p[0] = p[1:]

def p_expression(p):
    '''expression : column_name comparator value
                  | column_name comparator column_name
                  | column_name comparator value logical_operator expression
                  | column_name comparator column_name logical_operator expression'''
    p[0] = p[1:]

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
    p[0] = p[1:]

def p_join_type(p):
    '''join_type : INNER
                 | LEFT
                 | RIGHT'''
    p[0] = p[1]

def p_opt_where_clause(p):
    '''opt_where_clause : WHERE condition
                         | empty'''
    if p[1] is None:
        p[0]=p[0]
    else:
        p[0]=p[1:]


def p_opt_group_by_clause(p):
    '''opt_group_by_clause : GROUP BY group_by_list
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
    '''opt_order_by_clause : ORDER BY order_by_list
                           | empty'''
    p[0] = p[1:]

def p_order_by_list(p):
    '''order_by_list : order_specification
                     | order_specification COMMA order_by_list'''
    # if len(p) == 2:
    #     p[0] = [p[1]]
    # else:
    #     p[0] = [p[1]] + p[3]
    p[0]=p[1:]

def p_order_specification(p):
    '''order_specification : column_name order_direction'''
    p[0] = p[1:]

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
    p[0] = p[1:]

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

#Testowanie parsera
# sql = '''
# SELECT column1,abc FROM table WHERE abc LIKE "%a"
# '''
sql2 = '''
DELETE FROM table1 WHERE a>1
'''
sql3 = '''
UPDATE table3 SET column1 = 111, column2=123
'''
sql3 = '''
SELECT * FROM Products
ORDER BY ProductName DESC;
'''

#przy update nie działa set column1=column2

result = parser.parse(sql3)
print(result)




#result = parser.parse("select datepart(year, '2017-12-03') from a;")
result = parser.parse("SELECT productid,lll, kkk from q where q>0")
print(result)
#result = parser.parse("select distinct id from a intersect select id from b;")
#result = parser.parse("SELECT * from customers where a NOT IN (select customerid from orders);")
#result = parser.parse("SELECT x from a where a between a and abs(-6);")
#result = parser.parse("SELECT COALESCE(NULL, NULL, NULL, 'W3Schools.com', NULL, 'Example.com') from a;")
#result = parser.parse("SELECT CASE WHEN Quantity > 30 THEN x WHEN Quantity = 30 THEN 'The quantity is 30' END FROM OrderDetails;")
#result = parser.parse("CREATE FUNCTION a (arg1 int) returns int language plpgsql as $$ declare x int; begin 'aaa' end; $$;")
#result = parser.parse("create schema employee;")
#result = parser.parse("select distinct a from b;")
#result = parser.parse("DELETE FROM table_name WHERE x>y;")
#result = parser.parse("SELECT column1 FROM table1 EXCEPT SELECT column1 FROM table2;")
#result = parser.parse("ALTER TABLE table_name ADD COLUMN column_name int;")

#result = parser.parse("SELECT * from customers where a NOT IN (select customerid from orders);\nSELECT * from customers where a NOT IN (select customerid from orders);")
