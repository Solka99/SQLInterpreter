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
<sql_statement> ::= <select_statement> | <insert_statement> | <update_statement> | <delete_statement> | <select_statement>

<select_statement> ::= SELECT <select_list> FROM <table_name> <opt_join_clause> <opt_where_clause> <opt_group_by_clause> <opt_order_by_clause> <opt_semicolon>

<insert_statement> ::= INSERT INTO <table_name> (<opt_column_list>) VALUES (<values_list>)

<update_statement> ::= UPDATE <table-name> SET <set-list> <opt_where-clause>

<delete_statement> ::= DELETE FROM <table-name> <opt_where-clause>

<opt_semicolon> ::= SEMICOLON | <empty>

<select_list> ::= <column-name> | <column-name> <as-clause> | <column-name>, <select-list> | <aggregate-function> | ALL

<column_list> ::= (<column_name_list>)

<column_name_list> ::= <column_name> | <column_name> COMMA <column_name_list>

<opt_column_list> ::= <empty> | <column_list>

<values_list> ::= <value> | <value>, <values_list>

<set_list> ::= <column_name> = <value> | <column_name> = <value>, <set_list>

<condition> ::= <expression> | <column_name> <in_list> | <column_name> BETWEEN <value> AND <value> | <column_name> LIKE <pattern> | <column_name> IS NULL

<expression> ::= <column_name> <comparator> <value> | <column_name> <comparator> <column_name> | <column_name> <comparator> <value> <logical_operator> <expression> | <column_name> <comparator> <column_name> <logical_operator> <expression>

<logical_operator> ::= AND | OR

<comparator> ::= = | != | < | <= | > | >=

<value> ::= <number> | <string> | <boolean>

<table_name> ::= IDENTIFIER

<column_name> ::= IDENTIFIER

<as_clause> ::= AS IDENTIFIER

<opt_join_clause> ::= <join_clause> | <empty>

<join_clause> ::= <join_type> JOIN <table_name> ON <condition>

<join_type> ::= INNER | LEFT | RIGHT

<opt_where_clause> ::= WHERE <condition> | <empty>

<opt_group_by_clause> ::= GROUP BY <group_by_list> | <empty>

<group_by_list> ::= <column_name> | <column_name>, <group_by_list>

<opt_order_by_clause> ::= ORDER BY <order_by_list> | <empty>

<order_by_list> ::= <order_specification> | <order_specification>, <order_by_list>

<order_specification> ::= <column_name> <order_direction>

<order_direction> ::= ASC | DESC

<aggregate_function> ::= COUNT(<column_name>) | SUM(<column_name>) | AVG(<column_name>) | MAX(<column_name>) | MIN(<column_name>)

<in_list> ::= IN (<value_list>)

<pattern> ::= STRING

<empty> ::= 

```

#### Krótka instrukcja obsługi
W polu tekstowym należy wpisać zapytanie w języku SQL, które chcemy wykonać. Aby to się stało, należy wcisnąć klawisz ENTER lub kliknąć przycisk "Wykonaj zapytanie". Jeżeli zapytanie jest poprawne składniowo, to wyświetli się tabela, która jest wynikiem naszego zapytania. Jeśli zapytanie jest niepoprawne, wyświetli się komunikat "Błąd przy wykonywaniu zapytania".


#### Przykładowe zapytania SQL
```sql

1. SELECT name AS student_name FROM students;
2. select * from students2 where name='Kasia';
3. update students set major='Computer Science' where age=21; select * from students;
4. SELECT name, age FROM students ORDER BY age DESC;
5. SELECT * FROM students WHERE major LIKE 'M%';
6. SELECT count(*) from students where age>20; select * from students
7. SELECT major,avg(age) as average_age FROM students GROUP BY major;
8. SELECT * FROM students WHERE age = (SELECT MIN(age) FROM students) or age = (SELECT max(age) FROM students)
9. SELECT major, AVG(age) AS average_age FROM students GROUP BY major HAVING avg(age) > 20;
10. select students.major from students inner join COMPANY on students.id=COMPANY.id;
``` 
