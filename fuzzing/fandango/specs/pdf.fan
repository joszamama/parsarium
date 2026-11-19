# PDF with one to five pages and a classic xref table.
#
# Object numbers are fixed by position in the page tree: 1 catalog, 2 pages,
# 3 info, page k is object 2k+2 and its content stream object 2k+3. Each page
# count is its own alternative with a literal /Kids array and /Count, so the
# tree stays consistent. The page MediaBox is either given on every page or
# inherited from the Pages node, never mixed.
#
# The xref rows, the xref and /Size object counts, every stream /Length and
# startxref are `where` constraints of the form <field> == f(...). The xref
# rows are computed as one block from the body bytes: obj_offsets() finds
# each "N 0 obj" line, so the constraint does not depend on how many objects
# precede an object. Fandango repairs these fields directly.

import re

OBJ = re.compile(rb'(?m)^(\d+) 0 obj\n')

def obj_offsets(header, body):
    base = len(bytes(header))
    found = {int(m.group(1)): base + m.start() for m in OBJ.finditer(bytes(body))}
    return [found[n] for n in sorted(found)]

def xref_rows(header, body):
    return b''.join(b'%010d 00000 n \n' % o for o in obj_offsets(header, body))

def size(header, body):
    return b'%d' % (len(obj_offsets(header, body)) + 1)

def dec(n):
    return b'%d' % n

<start> ::= <header> <body> <xref> <trailer>

<header> ::= b'%PDF-1.' rb'[3-7]' b'\n%\xe2\xe3\xcf\xd3\n'
<body> ::= <catalog> <page_tree> <info>

<catalog> ::= b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'

# Page tree: per-page MediaBox, or one MediaBox inherited from the Pages node
<page_tree> ::= <own_boxes> | <inherited_box>
<own_boxes> ::= <own_1> | <own_2> | <own_3> | <own_4> | <own_5>
<inherited_box> ::= <inh_1> | <inh_2> | <inh_3> | <inh_4> | <inh_5>

<own_1> ::= <pages_open> <kids_1> b' >>\nendobj\n' <page_1>
<own_2> ::= <pages_open> <kids_2> b' >>\nendobj\n' <page_1> <page_2>
<own_3> ::= <pages_open> <kids_3> b' >>\nendobj\n' <page_1> <page_2> <page_3>
<own_4> ::= <pages_open> <kids_4> b' >>\nendobj\n' <page_1> <page_2> <page_3> <page_4>
<own_5> ::= <pages_open> <kids_5> b' >>\nendobj\n' <page_1> <page_2> <page_3> <page_4> <page_5>
<inh_1> ::= <pages_open> <kids_1> <media_box> b' >>\nendobj\n' <ipage_1>
<inh_2> ::= <pages_open> <kids_2> <media_box> b' >>\nendobj\n' <ipage_1> <ipage_2>
<inh_3> ::= <pages_open> <kids_3> <media_box> b' >>\nendobj\n' <ipage_1> <ipage_2> <ipage_3>
<inh_4> ::= <pages_open> <kids_4> <media_box> b' >>\nendobj\n' <ipage_1> <ipage_2> <ipage_3> <ipage_4>
<inh_5> ::= <pages_open> <kids_5> <media_box> b' >>\nendobj\n' <ipage_1> <ipage_2> <ipage_3> <ipage_4> <ipage_5>

<pages_open> ::= b'2 0 obj\n<< /Type /Pages'
<kids_1> ::= b' /Kids [4 0 R] /Count 1'
<kids_2> ::= b' /Kids [4 0 R 6 0 R] /Count 2'
<kids_3> ::= b' /Kids [4 0 R 6 0 R 8 0 R] /Count 3'
<kids_4> ::= b' /Kids [4 0 R 6 0 R 8 0 R 10 0 R] /Count 4'
<kids_5> ::= b' /Kids [4 0 R 6 0 R 8 0 R 10 0 R 12 0 R] /Count 5'

# Page k (object 2k+2) followed by its content stream (object 2k+3)
<page_1> ::= b'4 0 obj\n' <page_open> <media_box> <page_attrs> b' /Contents 5 0 R >>\nendobj\n5 0 obj\n' <contents>
<page_2> ::= b'6 0 obj\n' <page_open> <media_box> <page_attrs> b' /Contents 7 0 R >>\nendobj\n7 0 obj\n' <contents>
<page_3> ::= b'8 0 obj\n' <page_open> <media_box> <page_attrs> b' /Contents 9 0 R >>\nendobj\n9 0 obj\n' <contents>
<page_4> ::= b'10 0 obj\n' <page_open> <media_box> <page_attrs> b' /Contents 11 0 R >>\nendobj\n11 0 obj\n' <contents>
<page_5> ::= b'12 0 obj\n' <page_open> <media_box> <page_attrs> b' /Contents 13 0 R >>\nendobj\n13 0 obj\n' <contents>
<ipage_1> ::= b'4 0 obj\n' <page_open> <page_attrs> b' /Contents 5 0 R >>\nendobj\n5 0 obj\n' <contents>
<ipage_2> ::= b'6 0 obj\n' <page_open> <page_attrs> b' /Contents 7 0 R >>\nendobj\n7 0 obj\n' <contents>
<ipage_3> ::= b'8 0 obj\n' <page_open> <page_attrs> b' /Contents 9 0 R >>\nendobj\n9 0 obj\n' <contents>
<ipage_4> ::= b'10 0 obj\n' <page_open> <page_attrs> b' /Contents 11 0 R >>\nendobj\n11 0 obj\n' <contents>
<ipage_5> ::= b'12 0 obj\n' <page_open> <page_attrs> b' /Contents 13 0 R >>\nendobj\n13 0 obj\n' <contents>

<page_open> ::= b'<< /Type /Page /Parent 2 0 R'
<media_box> ::= b' /MediaBox [0 0 ' <extent> b' ' <extent> b']'
<page_attrs> ::= <rotate>? b' /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /' <base_font> b' >> >> >>'
<rotate> ::= b' /Rotate ' (b'0' | b'90' | b'180' | b'270')

<contents> ::= b'<< /Length ' <length> b' >>\nstream\n' <stream_data> b'\nendstream\nendobj\n'
<length> ::= rb'[0-9]'+

<info> ::= b'3 0 obj\n<<' <title>? <author>? <subject>? <producer>? b' >>\nendobj\n'
<title> ::= b' /Title (' <text> b')'
<author> ::= b' /Author (' <text> b')'
<subject> ::= b' /Subject (' <text> b')'
<producer> ::= b' /Producer (' <text> b')'

<xref> ::= b'xref\n0 ' <xref_size> b'\n0000000000 65535 f \n' <xref_rows>
<xref_size> ::= rb'[0-9]'+
<xref_rows> ::= <xref_row>+
<xref_row> ::= rb'[0-9]'{10} b' 00000 n \n'
<trailer> ::= b'trailer\n<< /Size ' <trailer_size> b' /Root 1 0 R /Info 3 0 R >>\nstartxref\n' <startxref> b'\n%%EOF\n'
<trailer_size> ::= rb'[0-9]'+
<startxref> ::= rb'[0-9]'+

# Page content: every page shows its own text, with up to three graphics
# or text operators around it
<stream_data> ::= (<operation> b'\n'){0,2} <show_text> (b'\n' <operation>)?
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

where forall <c> in <contents>: <c>.<length> == dec(len(bytes(<c>.<stream_data>)))
where <xref>.<xref_rows> == xref_rows(<start>.<header>, <start>.<body>)
where <xref>.<xref_size> == size(<start>.<header>, <start>.<body>)
where <trailer>.<trailer_size> == size(<start>.<header>, <start>.<body>)
where <trailer>.<startxref> == dec(len(bytes(<start>.<header>)) + len(bytes(<start>.<body>)))
