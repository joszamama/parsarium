# Small valid SQL statements for Parsarium's sql pilot cell.
# Dialect-neutral subset (see catalog/sql/PROTOCOL.md): one SELECT or one
# multi-row INSERT over the two control tables, lowercase unquoted
# identifiers, ASCII, ending in ";\n". Every output is accepted by SQLite's
# sqlite3_prepare against the control schema; the syntax is also within the
# PostgreSQL and MySQL grammars (parse only; semantic checks such as
# GROUP BY functional dependence are out of scope). Not a complete SQL grammar.

<start> ::= <select> | <insert>

<select> ::= "SELECT " <projection> " FROM customers AS c" <join>? <filter>? <grouping>? <ordering>? ";\n"
<projection> ::= <item> | <item> ", " <item> | <item> ", " <item> ", " <item>
<item> ::= "c.id" | "c.region" | "COUNT(*) AS n" | "MAX(c.id) AS peak" | "'x' AS tag" | "1 AS one"
<join> ::= " INNER JOIN orders AS o ON o.customer_id = c.id"
<filter> ::= " WHERE " <predicate> | " WHERE " <predicate> " AND " <predicate>
<predicate> ::= "c.id > " <integer> | "c.region = " <string> | "c.id <= " <integer> | "c.region <> " <string>
<grouping> ::= " GROUP BY c.region"
<ordering> ::= " ORDER BY c.region" | " ORDER BY c.id DESC"

<insert> ::= "INSERT INTO orders (id, customer_id, total, status) VALUES " <row> <more_rows> ";\n"
<more_rows> ::= "" | ", " <row> | ", " <row> ", " <row>
<row> ::= "(" <integer> ", " <integer> ", " <number> ", " <string> ")"

<integer> ::= "0" | <nonzero> <digit>{0,3}
<nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<number> ::= <integer> | <integer> "." <digit> <digit>?
<string> ::= "'" <letter>{1,8} "'"
<letter> ::= "a" | "b" | "e" | "o" | "p" | "u" | "z"
