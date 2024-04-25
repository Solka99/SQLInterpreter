# SQL Interpreter README

## Introduction
This README provides an overview of the tokens and grammar used for a basic SQL interpreter.

## Tokens
Below are the tokens defined for the SQL interpreter based on the specified grammar:

```
    SELECT = 'SELECT'
    FROM = 'FROM'
    WHERE = 'WHERE'
    IN = 'IN'
    BETWEEN = 'BETWEEN'
    LIKE = 'LIKE'
    IS_NULL = 'IS NULL'
    AS = 'AS'
    JOIN = 'JOIN'
    ON = 'ON'
    AND = 'AND'
    OR = 'OR'
    ORDER_BY = 'ORDER BY'
    GROUP_BY = 'GROUP BY'
    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    ASC = 'ASC'
    DESC = 'DESC'
    COUNT = 'COUNT'
    SUM = 'SUM'
    AVG = 'AVG'
    MAX = 'MAX'
    MIN = 'MIN'
    COMMA = ','
    SEMICOLON = ';'
    DOT = '.'
    LPAREN = '('
    RPAREN = ')'
    EQUALS = '='
    NOT_EQUALS = '!='
    LESS_THAN = '<'
    LESS_OR_EQUAL = '<='
    GREATER_THAN = '>'
    GREATER_OR_EQUAL = '>='
    NUMBER = '?[0-9]+(\.[0-9]+)?'
    STRING = '"[^"]*"'
    IDENTIFIER = '[A-Za-z][A-Za-z0-9_]*'
```

## Grammar
The grammar used for the SQL interpreter is as follows:

```
<sql-statement> ::= <select-statement> | <insert-statement> | <update-statement> | <delete-statement>

<select-statement> ::= SELECT <select-list> FROM <table-name> [<join-clause>] [WHERE <condition>] [GROUP BY <group-by-list>] [ORDER BY <order-by-list>]

<insert-statement> ::= INSERT INTO <table-name> [(<column-list>)] VALUES (<values-list>)

<update-statement> ::= UPDATE <table-name> SET <set-list> [WHERE <condition>]

<delete-statement> ::= DELETE FROM <table-name> [WHERE <condition>]

<select-list> ::= <column-name> | <column-name> <as-clause> | <column-name>, <select-list> | <aggregate-function>

<column-list> ::= <column-name> | <column-name>, <column-list>

<values-list> ::= <value> | <value>, <values-list>

<set-list> ::= <column-name> = <value> | <column-name> = <value>, <set-list>

<condition> ::= <expression> [<logical-operator> <condition>] | <column-name> <in-list> | <column-name> BETWEEN <value> AND <value> | <column-name> LIKE <pattern> | <column-name> IS NULL

<expression> ::= <column-name> <comparator> <value> | <column-name> <comparator> <column-name>

<logical-operator> ::= AND | OR

<comparator> ::= = | != | < | <= | > | >=

<value> ::= <number> | <string> | <boolean>

<table-name> ::= <identifier>

<column-name> ::= <identifier>

<identifier> ::= <letter> [<letter-or-digit> ...]

<letter> ::= [A-Za-z]

<letter-or-digit> ::= <letter> | [0-9]

<as-clause> ::= AS <identifier>

<join-clause> ::= <join-type> JOIN <table-name> ON <condition>

<join-type> ::= INNER | LEFT | RIGHT

<group-by-list> ::= <column-name> | <column-name>, <group-by-list>

<order-by-list> ::= <order-specification> | <order-specification>, <order-by-list>

<order-specification> ::= <column-name> <order-direction>

<order-direction> ::= ASC | DESC

<aggregate-function> ::= COUNT(<column-name>) | SUM(<column-name>) | AVG(<column-name>) | MAX(<column-name>) | MIN(<column-name>)

<in-list> ::= IN (<value-list>)

<pattern> ::= <string>
```
