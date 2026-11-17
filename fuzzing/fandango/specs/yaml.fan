# Small valid YAML documents for Parsarium's yaml pilot.
# One document per file, a block-mapping root with fixed, distinct keys (each
# optional, always in the same order, so no key repeats), block and flow
# collections, quoted scalars with escapes, literal and folded block scalars
# and one anchor/alias pair. Every plain scalar is typed the same under YAML
# 1.1 resolvers and the YAML 1.2 core schema: no yes/no/on/off/y/n, no
# leading-zero, octal, hexadecimal or sexagesimal numbers, no exponent
# without a dot, no timestamps and no merge keys. Fanbase has no YAML spec.

<start> ::= <comment>? <marker>? "kind: " <word> "\n" <e_count>? <e_ratio>? <e_flag>? <e_none>? \
            <e_title>? <e_tags>? <e_point>? <e_items>? <e_note>? <e_anchor>? <end>?

<comment> ::= "# Parsarium Fandango YAML\n"
<marker> ::= "---\n"
<end> ::= "...\n"

<e_count> ::= "count: " <int> "\n"
<e_ratio> ::= "ratio: " <float> "\n"
<e_flag> ::= "enabled: " <bool> "\n"
<e_none> ::= "missing: " <null> "\n"
<e_title> ::= "title: " <quoted> "\n"
<e_tags> ::= "tags: [" <flow_items>? "]\n"
<e_point> ::= "point: {lat: " <int> ", lon: " <float> "}\n"
<e_items> ::= "items:\n" <item>+
<e_note> ::= "note: " <block_scalar>
<e_anchor> ::= "base: &base\n  retries: " <int> "\n  label: " <word> "\n" \
               "service:\n  settings: *base\n  label: " <word> "\n"

<item> ::= "  - id: " <int> "\n    name: " <scalar> "\n"
<flow_items> ::= <flow_scalar> | <flow_scalar> ", " <flow_items>
<flow_scalar> ::= <word> | <int> | <float> | <bool> | <dq>

<scalar> ::= <word> | <phrase> | <int> | <float> | <bool> | <null> | <quoted>
<block_scalar> ::= "|\n" <block_lines> | ">\n" <block_lines> | "|-\n" <block_lines>
<block_lines> ::= "  " <phrase> "\n" | "  " <phrase> "\n" <block_lines>

<quoted> ::= <dq> | <sq>
<dq> ::= "\"" <dq_part>+ "\""
<dq_part> ::= <word> | " " | "\\\"" | "\\t" | "\\n" | "\\u00e9" | "\\\\" | "10115" | "yes" | "0755"
<sq> ::= "'" <sq_part>+ "'"
<sq_part> ::= <word> | " " | "''" | "on" | "1:30"

<word> ::= "alpha" | "beta" | "edge" | "catalog" | "A-7" | "Zürich" | "café"
<phrase> ::= <word> | <word> " " <phrase>
<int> ::= "0" | "7" | "42" | "-17" | "2026"
<float> ::= "0.25" | "-2.5" | "12.5" | "0.75"
<bool> ::= "true" | "false"
<null> ::= "null" | "~"
