# Small valid plain PPM (P3) images for Parsarium's ascii_pnm cell.
# Width, height and sample count are coupled structurally; every sample is
# drawn from a set bounded by the declared maxval.

<start> ::= "P3" <header_ws> <comment>? <image> <trailer>

<comment> ::= "# Parsarium Fandango P3\n"

<image> ::= <image_255> | <image_15>

<image_255> ::= "1" <hs> "1" <hs> "255" <ws1> <px_255> \
              | "2" <hs> "1" <hs> "255" <ws1> <px_255> <ss> <px_255> \
              | "1" <hs> "2" <hs> "255" <ws1> <px_255> <ss> <px_255> \
              | "2" <hs> "2" <hs> "255" <ws1> <px_255> <ss> <px_255> <ss> <px_255> <ss> <px_255>
<image_15> ::= "1" <hs> "1" <hs> "15" <ws1> <px_15> \
             | "2" <hs> "1" <hs> "15" <ws1> <px_15> <ss> <px_15> \
             | "1" <hs> "2" <hs> "15" <ws1> <px_15> <ss> <px_15> \
             | "2" <hs> "2" <hs> "15" <ws1> <px_15> <ss> <px_15> <ss> <px_15> <ss> <px_15>

<px_255> ::= <s_255> " " <s_255> " " <s_255>
<px_15> ::= <s_15> " " <s_15> " " <s_15>
<s_255> ::= "0" | "7" | "128" | "255"
<s_15> ::= "0" | "1" | "8" | "15"

<header_ws> ::= "\n" | " "
<hs> ::= " " | "\n"  # between width, height and maxval
<ws1> ::= "\n" | " "  # single whitespace after maxval
<ss> ::= " " | "  " | "\n"  # between pixels
<trailer> ::= "\n" | ""
