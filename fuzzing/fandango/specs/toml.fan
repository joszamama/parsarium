# Small valid TOML 1.0.0 documents for Parsarium's toml pilot.
# Key names are fixed per position, so no key or table is defined twice.
# Arrays are homogeneous and integers fit in 32 bits. Date-times use an
# upper-case T or a space and an upper-case Z or numeric offset.

<start> ::= <comment>? <root> <server>? <owner>? <dotted>? <products>

<comment> ::= "# Parsarium Fandango TOML\n"

<root> ::= <title_kv> <enabled_kv>? <retries_kv>?
<title_kv> ::= "title" <eq> <string> "\n"
<enabled_kv> ::= "enabled" <eq> <bool> "\n"
<retries_kv> ::= "retries" <eq> <integer> "\n"

<server> ::= "\n[server]\n" "host" <eq> <string> "\n" <ports_kv>? <ratio_kv>? <limits_kv>?
<ports_kv> ::= "ports" <eq> <int_array> "\n"
<ratio_kv> ::= "ratio" <eq> <float> "\n"
<limits_kv> ::= "limits" <eq> <inline_table> "\n"

<owner> ::= "\n[owner]\n" "name" <eq> <string> "\n" <since_kv>? <day_kv>? <at_kv>?
<since_kv> ::= "since" <eq> <datetime> "\n"
<day_kv> ::= "day" <eq> <local_date> "\n"
<at_kv> ::= "at" <eq> <local_time> "\n"

<dotted> ::= "\n[keys]\n" "site.\"example.com\"" <eq> <bool> "\n" "a.b" <eq> <integer> "\n"

<products> ::= <product>{0,3}
<product> ::= "\n[[products]]\n" "name" <eq> <string> "\n" <sku_kv>? <tags_kv>?
<sku_kv> ::= "sku" <eq> <integer> "\n"
<tags_kv> ::= "tags" <eq> <string_array> "\n"

<eq> ::= " = " | "=" | "  =  "

<bool> ::= "true" | "false"
<integer> ::= <decimal> | <hex> | <octal> | <binary>
<decimal> ::= <sign>? <digit19> <digit>{0,6} | "0" | "1_000" | "-17"
<sign> ::= "+" | "-"
<digit19> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digit> ::= "0" | <digit19>
<hex> ::= "0x" <hexdigit>{1,6}
<hexdigit> ::= <digit> | "A" | "B" | "C" | "D" | "E" | "F" | "a" | "f"
<octal> ::= "0o" <octdigit>{1,6}
<octdigit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7"
<binary> ::= "0b" <bindigit>{1,12}
<bindigit> ::= "0" | "1"

<float> ::= <sign>? <int_part> "." <digit>{1,4} | <sign>? <int_part> <exponent> | <sign>? <int_part> "." <digit>{1,3} <exponent>
<int_part> ::= "0" | <digit19> <digit>{0,3}
<exponent> ::= ("e" | "E") <sign>? <digit>{1,2}

<string> ::= <basic_string> | <literal_string>
<basic_string> ::= "\"" <basic_char>* "\""
<basic_char> ::= <plain_char> | "\\t" | "\\n" | "\\\"" | "\\\\" | "\\u00e9" | "\\U0001F600" | "é" | "ü"
<literal_string> ::= "'" <literal_char>* "'"
<literal_char> ::= <plain_char> | "\\" | "\""
<plain_char> ::= "a" | "b" | "z" | "A" | "Q" | "0" | "9" | " " | "-" | "_" | "." | ":" | "/"

<int_array> ::= "[]" | "[" <integer> ("," <ws> <integer>){0,3} "]"
<string_array> ::= "[" <string> ("," <ws> <string>){0,2} <trailing_comma>? "]"
<trailing_comma> ::= ","
<ws> ::= "" | " " | "\n  "

<inline_table> ::= "{}" | "{ max = " <integer> " }" | "{ max = " <integer> ", min = " <integer> " }"

<datetime> ::= <date> <t> <time> <offset>
<local_date> ::= <date>
<local_time> ::= <time>
<t> ::= "T" | " "
<date> ::= <year> "-" <month> "-" <day>
<year> ::= "1979" | "2000" | "2024" | "1969"
<month> ::= "01" | "02" | "05" | "12"
<day> ::= "01" | "09" | "27" | "28"
<time> ::= <hour> ":" <minsec> ":" <minsec> <frac>?
<hour> ::= "00" | "07" | "12" | "23"
<minsec> ::= "00" | "32" | "59"
<frac> ::= "." <digit>{1,6}
<offset> ::= "Z" | "+00:00" | "-07:00" | "+05:30"
