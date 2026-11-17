# Minimal one-page PDF with a classic xref table. Objects are fixed in
# order (catalog, pages, page, contents, info) so that each xref offset,
# the stream /Length and startxref can be stated as constraints over the
# byte lengths of preceding parts. Fandango repairs these fields directly.

def off(*parts):
    return b'%010d' % sum(len(bytes(p)) for p in parts)

def dec(n):
    return b'%d' % n

<start> ::= <header> <catalog> <pages> <page> <contents> <info> <xref> <trailer>

<header> ::= b'%PDF-1.' rb'[3-7]' b'\n%\xe2\xe3\xcf\xd3\n'

<catalog> ::= b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'
<pages> ::= b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n'
<page> ::= b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' <extent> b' ' <extent> b'] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /' <base_font> b' >> >> >> /Contents 4 0 R >>\nendobj\n'
<contents> ::= b'4 0 obj\n<< /Length ' <number> b' >>\nstream\n' <stream_data> b'\nendstream\nendobj\n'
<info> ::= b'5 0 obj\n<< /Title (' <text> b') /Producer (Parsarium Fandango) >>\nendobj\n'

<xref> ::= b'xref\n0 6\n0000000000 65535 f \n' <xref_1> <xref_2> <xref_3> <xref_4> <xref_5>
<xref_1> ::= <offset> b' 00000 n \n'
<xref_2> ::= <offset> b' 00000 n \n'
<xref_3> ::= <offset> b' 00000 n \n'
<xref_4> ::= <offset> b' 00000 n \n'
<xref_5> ::= <offset> b' 00000 n \n'
<offset> ::= rb'[0-9]'{10}
<trailer> ::= b'trailer\n<< /Size 6 /Root 1 0 R /Info 5 0 R >>\nstartxref\n' <number> b'\n%%EOF\n'

<number> ::= rb'[0-9]'+

# Page content: a few graphics and text operators
<stream_data> ::= <operation> (b'\n' <operation>){0,3}
<operation> ::= <fill> | <stroke> | <show_text>
<fill> ::= <color> b' rg ' <small> b' ' <small> b' ' <small> b' ' <small> b' re f'
<stroke> ::= <small> b' w ' <small> b' ' <small> b' m ' <small> b' ' <small> b' l S'
<show_text> ::= b'BT /F1 ' <small> b' Tf ' <small> b' ' <small> b' Td (' <text> b') Tj ET'
<color> ::= <unit> b' ' <unit> b' ' <unit>
<unit> ::= b'0' | b'1' | b'0.' rb'[0-9]'
<small> ::= rb'[1-9]' rb'[0-9]'?
<text> ::= rb'[A-Za-z0-9 ]'{1,16}
<extent> ::= b'72' | b'144' | b'200' | b'595' | b'612' | b'842'
<base_font> ::= b'Helvetica' | b'Times-Roman' | b'Courier'

where <contents>.<number> == dec(len(bytes(<contents>.<stream_data>)))
where <xref_1>.<offset> == off(<start>.<header>)
where <xref_2>.<offset> == off(<start>.<header>, <start>.<catalog>)
where <xref_3>.<offset> == off(<start>.<header>, <start>.<catalog>, <start>.<pages>)
where <xref_4>.<offset> == off(<start>.<header>, <start>.<catalog>, <start>.<pages>, <start>.<page>)
where <xref_5>.<offset> == off(<start>.<header>, <start>.<catalog>, <start>.<pages>, <start>.<page>, <start>.<contents>)
where <trailer>.<number> == dec(len(bytes(<start>)) - len(bytes(<start>.<xref>)) - len(bytes(<start>.<trailer>)))
