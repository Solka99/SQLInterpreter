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
    NUMBER = '[0-9]+(\.[0-9]+)?'
    STRING = '"[^"]*"'
    IDENTIFIER = '[A-Za-z][A-Za-z0-9_]*'
```

## Gramatyka

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

#### Krótka instrukcja obsługi
W polu tekstowym należy wpisać zapytanie w języku SQL, które chcemy wykonać. Aby to się stało, należy wcisnąć klawisz ENTER lub kliknąć przycisk "Wykonaj zapytanie". Jeżeli zapytanie jest poprawne składniowo, to wyświetli się tabela, która jest wynikiem naszego zapytania. Jeśli zapytanie jest niepoprawne, wyświetli się komunikat "Błąd przy wykonywaniu zapytania".

