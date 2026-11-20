# Valid plain PPM (P3) images for Parsarium's ascii_pnm cell.
#
# Width and height are 1-32 and maxval 1-65535 (mostly 1-255). Header tokens
# are separated by blanks, tabs, LF or CRLF, with optional comments after any
# separator before the maxval. One whitespace character follows the maxval.
#
# The raster is one `where` constraint of the form <raster> == f(...), which
# Fandango repairs directly: raster() keeps a raster that already holds exactly
# width x height x 3 decimal samples, each at most maxval, on lines of at most
# 68 characters; otherwise it lays out a new one, with sample values and line
# layout drawn from a generator seeded by the SHA-256 of the raster Fandango
# derived first. Every file ends in white space after the last sample.

import hashlib
import random

LINE = 68  # plus a trailing blank or tab, lines stay within 70 characters
# Room for the header's last line when the raster starts on the maxval line.
HEADER_ROOM = 20


def _tokens(text):
    return text.split()


def _valid(text, count, maxval):
    tokens = _tokens(text)
    if len(tokens) != count:
        return False
    for token in tokens:
        if not token.isdigit() or (len(token) > 1 and token[0] == "0") or int(token) > maxval:
            return False
    lines = text.replace("\r\n", "\n").split("\n")
    return len(lines[0]) <= LINE - HEADER_ROOM and all(len(line) <= LINE for line in lines)


def _values(rng, width, height, maxval):
    mode = rng.choice(("uniform", "palette", "gradient", "extremes"))
    count = width * height
    if mode == "uniform":
        return [rng.randint(0, maxval) for _ in range(count * 3)]
    if mode == "extremes":
        return [rng.choice((0, maxval)) for _ in range(count * 3)]
    if mode == "palette":
        palette = [[rng.choice((0, maxval, rng.randint(0, maxval))) for _ in range(3)]
                   for _ in range(rng.randint(1, 6))]
        return [s for _ in range(count) for s in rng.choice(palette)]
    out = []
    for y in range(height):
        for x in range(width):
            out += [maxval * x // max(width - 1, 1), maxval * y // max(height - 1, 1),
                    maxval * (x + y) // max(width + height - 2, 1)]
    return out


def _layout(rng, samples, width):
    style = rng.choice(("row", "row", "pixel", "packed", "packed", "single"))
    eol = "\r\n" if rng.random() < 0.1 else "\n"
    gap = rng.choice([" ", " ", " ", " ", " ", " ", "  ", "\t"])
    pixel_gap = rng.choice([gap, gap, gap, gap, "  ", "\t"])
    limit = LINE if style in ("row", "single") else rng.randint(12, LINE)
    pixels = [samples[i:i + 3] for i in range(0, len(samples), 3)]
    if style == "pixel":
        groups = [[p] for p in pixels]
    elif style == "row":
        groups = [pixels[i:i + width] for i in range(0, len(pixels), width)]
    else:
        groups = [pixels]
    lines = []
    for group in groups:
        line = ""
        for index, pixel in enumerate(group):
            for k, sample in enumerate(pixel):
                piece = str(sample)
                sep = "" if not line else (gap if k else pixel_gap)
                room = (limit if lines else min(limit, LINE - HEADER_ROOM))
                if line and len(line) + len(sep) + len(piece) > room:
                    lines.append(line)
                    line, sep = "", ""
                line += sep + piece
        lines.append(line)
    return eol.join(lines)


def raster(width, height, maxval, current):
    width, height, maxval = int(str(width)), int(str(height)), int(str(maxval))
    text = str(current)
    if _valid(text, width * height * 3, maxval):
        return text
    rng = random.Random(hashlib.sha256(text.encode()).digest())
    return _layout(rng, _values(rng, width, height, maxval), width)


<start> ::= "P3" <hsep> <width> <hsep> <height> <hsep> <maxval> <ws1> <raster> <trailer>

# Header separators: whitespace, optionally followed by one comment line.
# Equivalent single-character alternatives are separate symbols so that tabs,
# CRs and comments stay a minority of separators.
<hsep> ::= <hws_space> | <hws_newline> | <hws_space2> | <hws_newline2> | <hws_alt> \
         | <hws> <comment> <hws_opt>
<hws_space> ::= " "
<hws_newline> ::= "\n"
<hws_space2> ::= " "
<hws_newline2> ::= "\n"
<hws> ::= " " | "\n"
<hws_alt> ::= "  " | " \n" | "\n\n" | <hws_rare>
<hws_rare> ::= "\t" | "\r\n"
<hws_opt> ::= "" | " " | "\t"
<comment> ::= "#" <comment_text> "\n"
<comment_text> ::= "" | " Parsarium Fandango P3" | " CREATOR: GIMP PNM Filter Version 1.1" \
                 | " plain PPM" | "comment without a space" | " 1 2 3 # digits are ignored here"

<width> ::= <dim>
<height> ::= <dim>
<dim> ::= <dim_one> | <dim_tiny> | <dim_small> | <dim_mid> | <dim_large>
<dim_one> ::= "1"
<dim_tiny> ::= "2" | "3" | "4"
<dim_small> ::= "5" | "6" | "7" | "8" | "9"
<dim_mid> ::= "1" <digit>
<dim_large> ::= "2" <digit> | "3" ("0" | "1" | "2")

# Maxval: 255, other common 8-bit values, any value 1-255, and 16-bit values
# 256-65535 (one alternative in five).
<maxval> ::= <max_255> | <max_common> | <max_byte> | <max_byte_high> | <max_wide>
<max_255> ::= "255"
<max_common> ::= "15" | "1" | "3" | "7" | "31" | "63" | "100" | "127"
<max_byte> ::= <nonzero> | <nonzero> <digit>
<max_byte_high> ::= "1" <digit> <digit> | "2" ("0" | "1" | "2" | "3" | "4") <digit> | "25" ("0" | "1" | "2" | "3" | "4" | "5")
<max_wide> ::= "65535" | "4095" | "1023" | "256" | "1000" \
             | ("3" | "4" | "5" | "6" | "7" | "8" | "9") <digit> <digit> \
             | <nonzero> <digit> <digit> <digit> \
             | ("1" | "2" | "3" | "4" | "5") <digit> <digit> <digit> <digit>
<nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

# Exactly one whitespace character ends the header.
<ws1> ::= <ws1_space> | <ws1_newline> | <ws1_newline2> | <ws1_space2> | <ws1_rare>
<ws1_space> ::= " "
<ws1_space2> ::= " "
<ws1_newline> ::= "\n"
<ws1_newline2> ::= "\n"
<ws1_rare> ::= "\t" | "\r"

<raster> ::= <sample> (<rsep> <sample>)*
<sample> ::= <digit>+
<rsep> ::= (" " | "\t" | "\n" | "\r")+

# Netpbm's plain PPM definition gives every raster sample white space before
# and after it, so the last sample is always followed by white space.
<trailer> ::= <trailer_newline> | <trailer_newline2> | <trailer_newline3> | <trailer_space> | <trailer_other>
<trailer_newline> ::= "\n"
<trailer_newline2> ::= "\n"
<trailer_newline3> ::= "\n"
<trailer_space> ::= " "
<trailer_other> ::= " \n" | "\r\n" | "\n\n" | "\t"

where <raster> == raster(<start>.<width>, <start>.<height>, <start>.<maxval>, <raster>)
