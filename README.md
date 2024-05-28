# Interpreter SQL z interfejsem graficznym
Dane studentów: Alicja Solarz, Katarzyna Woźniak, Bartosz Zieliński

Dane kontaktowe: alicjasol@student.agh.edu.pl

## Założenia programu - krótki opis

#### Ogólne cele programu:
Nasz projekt ma na celu stworzenie interpretera SQL, który umożliwi użytkownikom wykonywanie zapytań SQL za pomocą przyjaznego interfejsu graficznego (GUI). Program ma być przyjaznym narzędziem edukacyjnym oraz praktycznym rozwiązaniem dla osób, które chcą eksperymentować z językiem SQL i bazami danych bez konieczności instalowania pełnych systemów zarządzania bazami danych.

#### Rodzaj translatora:
Nasz projekt jest interpreterem, co znacza, że zapytania SQL będą analizowane i wykonywane w czasie rzeczywistym, bez potrzeby kompilacji do kodu pośredniego czy maszynowego. Interpreter przetwarza zapytania SQL bezpośrednio, dostarczając natychmiastowe wyniki użytkownikowi.

#### Planowany wynik działania programu:
Program będzie w stanie:
- Przyjmować zapytania SQL od użytkownika za pośrednictwem interfejsu graficznego.
- Analizować składnię i semantykę zapytań SQL.
- Wykonywać zapytania na wbudowanej bazie danych.
- Wyświetlać wyniki zapytań w formie tabeli w GUI.

#### Planowany język implementacji:
Planowanym językiem implementacji naszego projektu jest Python. Wybór ten wynika z jego szerokiego wsparcia dla bibliotek do przetwarzania języka naturalnego, generowania GUI oraz obsługi baz danych.

#### Sposób realizacji skanera/parsera - użycie generatora skanerów/parserów:

Do realizacji skanera i parsera planujemy użycie biblioteki PLY (Python Lex-Yacc), która jest implementacją narzędzi Lex i Yacc dla języka Python. PLY umożliwia łatwe tworzenie skanerów (lekserów) oraz parserów, co jest kluczowe dla naszego projektu.

#### Etapy realizacji:

1. Skanowanie (Leksykalizacja):
Za pomocą PLY stworzymy skaner, który będzie odpowiedzialny za rozpoznawanie podstawowych elementów języka SQL, takich jak słowa kluczowe, identyfikatory, operatory oraz literały.
Skaner będzie generował tokeny, które są podstawowymi jednostkami języka.

2. Parsowanie (Analiza składniowa):
Na podstawie wygenerowanych tokenów parser zbuduje drzewo składniowe, które reprezentuje strukturę zapytania SQL.
Parser będzie weryfikował poprawność składniową zapytań SQL zgodnie z określonymi regułami gramatycznymi.

3. Wykonanie zapytań:
Po wygenerowaniu drzewa składniowego, nasz interpreter przekształci je w wewnętrzną reprezentację, która będzie następnie używana do wykonywania zapytań na wbudowanej bazie danych.
Wyniki zapytań zostaną przetworzone i wyświetlone użytkownikowi za pośrednictwem interfejsu graficznego.

4. Interfejs graficzny:
Do stworzenia GUI planujemy użycie Flask'a. Interfejs będzie zawierał:
- Pole tekstowe do wprowadzania zapytań SQL.
- Przycisk do wykonania zapytania.
- Tabelę do wyświetlania wyników zapytań.

## Tokeny

```
    SELECT = 'SELECT'
    FROM = 'FROM'
    WHERE = 'WHERE'
    IN = 'IN'
    BETWEEN = 'BETWEEN'
    LIKE = 'LIKE'
    AS = 'AS'
    JOIN = 'JOIN'
    ON = 'ON'
    AND = 'AND'
    OR = 'OR'
    ORDER = 'ORDER'
    BY = 'BY'
    GROUP = 'GROUP'
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
    NUMBER = '[0-9]+(\.[0-9]+)?'
    STRING = '"[^"]*"'
    IDENTIFIER = '[A-Za-z][A-Za-z0-9_]*'
    INSERT =  'INSERT'
    INTO = 'INTO'
    BOOLEAN = 'BOOLEAN'
    IS = 'IS'
    NULL = 'NULL'
    UPDATE = 'UPDATE'
    SET = 'SET'
    DELETE = 'DELETE'
    VALUES = 'VALUES'
    EVERY = '\*'
    CREATE = 'CREATE'
    DATABASE = 'DATABASE'
    DROP = 'DROP'
    TABLE = 'TABLE'
    ALTER = 'ALTER'
    ADD = 'ADD'
    CONSTRAINT = 'CONSTRAINT'
    RENAME = 'RENAME'
    COLUMN = 'COLUMN'
    TO = 'TO'
    REPLACE = 'REPLACE'
    HAVING = 'HAVING'
    NOT = 'NOT'
    UNIQUE = 'UNIQUE'
    PRIMARY = 'PRIMARY'
    KEY = 'KEY'
    FOREIGN = 'FOREIGN'
    CHECK = 'CHECK'
    LIMIT = 'LIMIT'
    TOP = 'TOP'
    TRUNCATE = 'TRUNCATE'
    UNION = 'UNION'
    DISTINCT = 'DISTINCT'
    
    
```

## Gramatyka

```

<statements> ::= <sql_statement> SEMICOLON <statements> | <sql_statement> <opt_semicolon> 

<sql_statement> ::= <select_statement> | <insert_statement> | <update_statement> | <delete_statement> | <union_statement> | <create_statement> | <drop_statement> | <alter>

<select_statement> ::= SELECT <opt_distinct> <select_list> FROM <table_name> <opt_join_clause> <opt_where_clause> <opt_group_by_clause> <opt_order_by_clause> <opt_limit_clause>

<insert_statement> ::= INSERT INTO <table_name> <opt_column_list> VALUES (<values_list>)

<update_statement> ::= UPDATE <table_name> SET <set_list> <opt_where_clause>

<delete_statement> ::= DELETE FROM <table_name> <opt_where_clause>

<union_statement> ::= <select_statement> UNION <select_statement>

<drop_statement> ::= DROP COLUMN <column_name> | DROP CONSTRAINT <constraint_name> | DROP PRIMARY KEY | DROP FOREIGN KEY <key_name> | DROP CHECK <check_name> | DROP DATABASE <database_name> | DROP TABLE <table_name>

<key_name> ::= IDENTIFIER

<check_name> ::= IDENTIFIER

<alter> ::= ALTER TABLE <table_name> <add_statement> | ALTER TABLE <table_name> <drop_statement> | ALTER TABLE <table_name> ALTER COLUMN <column_name> <column_type> | ALTER TABLE <table_name> RENAME COLUMN <column_name> TO <column_name>

<add_statement> ::= ADD <column_name> <column_type> | ADD <constraint_clause> | ADD UNIQUE (<column_name>) | ADD PRIMARY KEY (<column_name>) | ADD FOREIGN KEY (<column_name>) REFERENCES <table_name> (<column_name>) | ADD CHECK (<expression>)

<opt_semicolon> ::= SEMICOLON | <empty>

<select_list> ::= <column_name> | <column_name> <as_clause> | <column-name>, <select-list> | <aggregate-function> | <aggregate_function> , <select_list> | <aggregate_function> <as_clause> | <aggregate_function> <as_clause> , <select_list> | *

<opt_distinct> ::= DISTINCT | <empty>

<column_list> ::= (<column_name_list>)

<column_name_list> ::= <column_name> | <column_name> , <column_name_list>

<opt_column_list> ::= <empty> | <column_list>

<opt_limit_clause> ::= LIMIT NUMBER | <empty>

<values_list> ::= <value> | <value>, <values_list>

<set_list> ::= <column_name> = <value> | <column_name> = <value>, <set_list>

<condition> ::= <expression> | <column_name> <in_list> | <column_name> BETWEEN <value> AND <value> | <column_name> LIKE <pattern> | <column_name> IS NULL

<expression> ::= <column_name> <comparator> <value> | <column_name> <comparator> <column_name> | <column_name> <comparator> <value> <logical_operator> <expression> | <column_name> <comparator> <column_name> <logical_operator> <expression> | <column_name> <comparator> (<select_statement>) | <column_name> <comparator> (<select_statement>) <logical_operator> <expression>

<logical_operator> ::= AND | OR

<comparator> ::= = | != | < | <= | > | >=

<value> ::= NUMBER | STRING | BOOLEAN

<table_name> ::= IDENTIFIER

<column_name> ::= IDENTIFIER | <table_name> DOT IDENTIFIER

<as_clause> ::= AS IDENTIFIER

<opt_join_clause> ::= <join_clause> | <empty>

<join_clause> ::= <join_type> JOIN <table_name> ON <join_condition>

<join_type> ::= INNER | LEFT | RIGHT

<join_condition> ::= <table_name> DOT IDENTIFIER EQUALS <table_name> DOT IDENTIFIER

<opt_where_clause> ::= WHERE <condition> | <empty>

<opt_group_by_clause> ::= GROUP BY <group_by_list> <opt_having_clause> | <empty>

<group_by_list> ::= <column_name> | <column_name>, <group_by_list>

<opt_having_clause> ::= HAVING <condition> | HAVING <aggregate_function> <having_expression> | <empty>

<having_expression> ::= <comparator> <value> | <comparator> <value> <logical_operator> <expression> | <comparator> (<select_statement>) | <comparator> (<select_statement>) <logical_operator> <expression>

<opt_order_by_clause> ::= ORDER BY <order_by_list> | <empty>

<order_by_list> ::= <order_specification> | <order_specification>, <order_by_list>

<order_specification> ::= <column_name> <order_direction>

<order_direction> ::= ASC | DESC

<aggregate_function> ::= COUNT(<column_name>) | COUNT (*) | SUM(<column_name>) | AVG(<column_name>) | MAX(<column_name>) | MIN(<column_name>)

<in_list> ::= IN (<values_list>) | IN (<select_statement>)

<pattern> ::= STRING

<empty> ::= 

<create_statement> ::= CREATE DATABASE <database_name> | CREATE TABLE <table_name> (<create_table_list>) | CREATE TABLE <table_name> AS <select_statement>

<database_name> ::= IDENTIFIER

<create_table_list> ::= <table_name_type_optconstraint_list> | <table_name_type_optconstraint_list> , <create_table_list>

<table_name_type_optconstraint_list> ::= <column_name> <column_type> <opt_constraint_clause> | <column_name> <column_type> <opt_constraint_clause> , <table_name_type_optconstraint_list>

<opt_constraint_clause> ::= <constraint_clause> | <empty>

<constraint_clause> ::= PRIMARY KEY | UNIQUE | NOT NULL | CHECK (<expression>) | FOREIGN KEY (<column_name>) REFERENCES <table_name> (<column_name>)

<column_type> ::= INT | INTEGER | REAL | NUMERIC | TEXT | BLOB | BOOLEAN

<constraint_name> ::= IDENTIFIER



```

#### Krótka instrukcja obsługi
W polu tekstowym należy wpisać zapytanie w języku SQL, które chcemy wykonać. Aby to się stało, należy wcisnąć klawisz ENTER lub kliknąć przycisk "Wykonaj zapytanie". Jeżeli zapytanie jest poprawne składniowo, to wyświetli się tabela, która jest wynikiem naszego zapytania. Jeśli zapytanie jest niepoprawne, wyświetli się komunikat "Błąd przy wykonywaniu zapytania".

