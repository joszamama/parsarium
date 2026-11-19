# Small valid SVG 1.1 documents that every renderer can draw.
#
# The root always declares the SVG namespace and a positive width and height
# (1-512, unitless or px). Without a viewBox the user space is the viewport,
# so width and height are at least 32. With a viewBox the width and height
# may be as small as 1; the viewBox origin is in [-16, 4] and its width and
# height in [48, 128], so it always contains the square [4, 32] x [4, 32].
#
# The first painted element is an "anchor": an opaque-enough rect, circle,
# ellipse or closed path that always overlaps that square, so every file
# renders to a non-empty raster. The anchor may start at (0, 0), so some
# files paint the top-left pixel and others do not.
#
# References use fixed ids. Each document is one of four variants, and only
# a variant that defines an id may refer to it: plain (no defs), a gradient
# "g1" used through fill="url(#g1)" or stroke="url(#g1)", a reusable shape
# "s1" drawn through <use xlink:href="#s1">, or both. xmlns:xlink is declared
# exactly in the variants that contain <use>. There are no text elements,
# scripts, animation, images, external references or DOCTYPE.

<start> ::= <prolog>? <comment>? <document>

<prolog> ::= "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" | "<?xml version=\"1.0\"?>\n"
<comment> ::= "<!-- " <words> " -->\n"

<document> ::= <doc_plain> | <doc_grad> | <doc_use> | <doc_grad_use>

<doc_plain> ::= <svg_open> ">" <meta> <body_plain> "\n</svg>\n"
<doc_grad> ::= <svg_open> ">" <meta> "\n<defs>" <gradient> "\n</defs>" <body_grad> "\n</svg>\n"
<doc_use> ::= <svg_open> <xlink> ">" <meta> "\n<defs>" <reusable> "\n</defs>" <body_use> "\n</svg>\n"
<doc_grad_use> ::= <svg_open> <xlink> ">" <meta> "\n<defs>" <gradient> <reusable> "\n</defs>" <body_grad_use> "\n</svg>\n"

<svg_open> ::= "<svg xmlns=\"http://www.w3.org/2000/svg\"" <version>? <viewport>
<xlink> ::= " xmlns:xlink=\"http://www.w3.org/1999/xlink\""
<version> ::= " version=\"1.1\""

# Viewport: user space equal to the viewport, or a viewBox
<viewport> ::= <fixed_viewport> | <viewbox_viewport>
<fixed_viewport> ::= " width=\"" <big_dim> <unit>? "\" height=\"" <big_dim> <unit>? "\""
<viewbox_viewport> ::= " width=\"" <any_dim> <unit>? "\" height=\"" <any_dim> <unit>? "\" viewBox=\"" <vb_min> " " <vb_min> " " <vb_len> " " <vb_len> "\"" <aspect>?
<unit> ::= "px"
<big_dim> ::= "3" r"[2-9]" | r"[4-9][0-9]" | r"[1-4][0-9][0-9]" | "5" r"[01][0-2]" | "64" | "100" | "128" | "256"
<any_dim> ::= r"[1-9]" | r"[1-9][0-9]" | r"[1-4][0-9][0-9]" | "5" r"[01][0-2]" | "32" | "64" | "128" | "256"
<vb_min> ::= "0" | "-" r"[1-9]" | "-1" r"[0-6]" | r"[1-4]"
<vb_len> ::= "4" r"[89]" | r"[5-9][0-9]" | "1" r"[01][0-9]" | "12" r"[0-8]" | "64" | "100"
<aspect> ::= " preserveAspectRatio=\"" <aspect_value> "\""
<aspect_value> ::= "none" | <align> | <align> " meet"
<align> ::= "xMinYMin" | "xMidYMin" | "xMaxYMin" | "xMinYMid" | "xMidYMid" | "xMaxYMid" | "xMinYMax" | "xMidYMax" | "xMaxYMax"

<meta> ::= <title>? <desc>?
<title> ::= "\n<title>" <words> "</title>"
<desc> ::= "\n<desc>" <words> "</desc>"
<words> ::= <word> (" " <word>){0,3}
<word> ::= r"[A-Za-z][a-z0-9]{0,7}"

# Bodies: the anchor first, then further items. A variant with defs uses
# every id it defines at least once.
<body_plain> ::= <nl> <anchor> (<nl> <item_plain>){0,7}
<body_grad> ::= <nl> <anchor> (<nl> <item_grad>){0,3} <nl> <grad_shape> (<nl> <item_grad>){0,3}
<body_use> ::= <nl> <anchor> (<nl> <item_use>){0,3} <nl> <use> (<nl> <item_use>){0,3}
<body_grad_use> ::= <nl> <anchor> (<nl> <item_grad_use>){0,2} <nl> <grad_shape> (<nl> <item_grad_use>){0,2} <nl> <use_grad> (<nl> <item_grad_use>){0,2}

<item_plain> ::= <shape> | <group>
<item_grad> ::= <shape> | <group> | <grad_shape>
<item_use> ::= <shape> | <group> | <use>
<item_grad_use> ::= <shape> | <group> | <grad_shape> | <use_grad>
<nl> ::= "\n" | "\n  "

# Anchor: overlaps [4, 32] x [4, 32]; solid paint with opacity at least 0.6
<anchor> ::= <anchor_rect> | <anchor_circle> | <anchor_ellipse> | <anchor_path> | <anchor_quad>
<anchor_rect> ::= "<rect x=\"" <a_xy> "\" y=\"" <a_xy> "\" width=\"" <a_len> "\" height=\"" <a_len> "\"" <corner>? <anchor_paint> "/>"
<anchor_circle> ::= "<circle cx=\"" <a_center> "\" cy=\"" <a_center> "\" r=\"" <a_radius> "\"" <anchor_paint> "/>"
<anchor_ellipse> ::= "<ellipse cx=\"" <a_center> "\" cy=\"" <a_center> "\" rx=\"" <a_radius> "\" ry=\"" <a_radius> "\"" <anchor_paint> "/>"
<anchor_path> ::= "<path d=\"M" <a_xy> " " <a_xy> " h" <a_len> " v" <a_len> " h-" <a_len> " z\"" <anchor_paint> "/>"
<anchor_quad> ::= "<path d=\"M " <a_xy> "," <a_xy> " L " <a_far> "," <a_xy> " L " <a_far> "," <a_far> " L " <a_xy> "," <a_far> " Z\"" <anchor_paint> "/>"
<a_xy> ::= "0" | r"[1-9]" | "1" r"[0-5]"
<a_len> ::= "1" r"[6-9]" | r"[2-4][0-9]"
<a_far> ::= "3" r"[2-9]" | "4" r"[0-8]"
<a_center> ::= "2" r"[0-9]" | "3" r"[0-6]"
<a_radius> ::= "1" r"[0-9]" | "2" r"[0-4]"
<anchor_paint> ::= <anchor_fill>? <stroke>? <strong_opacity>? | <anchor_style>
<anchor_fill> ::= " fill=\"" <color> "\""
<anchor_style> ::= " style=\"fill:" <color> <style_stroke>? <style_strong_opacity>? "\""
<strong_opacity> ::= " opacity=\"" <strong_unit> "\"" | " fill-opacity=\"" <strong_unit> "\""
<style_strong_opacity> ::= ";opacity:" <strong_unit>
<strong_unit> ::= "1" | "0." r"[6-9]" | "0." r"[6-9][0-9]"

# Shapes
<shape> ::= <rect> | <circle> | <ellipse> | <line> | <polyline> | <polygon> | <path>
<rect> ::= "<rect x=\"" <num> "\" y=\"" <num> "\" width=\"" <pos> "\" height=\"" <pos> "\"" <corner>? <paint> "/>"
<corner> ::= " rx=\"" <pos> "\"" | " rx=\"" <pos> "\" ry=\"" <pos> "\""
<circle> ::= "<circle cx=\"" <num> "\" cy=\"" <num> "\" r=\"" <pos> "\"" <paint> "/>"
<ellipse> ::= "<ellipse cx=\"" <num> "\" cy=\"" <num> "\" rx=\"" <pos> "\" ry=\"" <pos> "\"" <paint> "/>"
<line> ::= "<line x1=\"" <num> "\" y1=\"" <num> "\" x2=\"" <num> "\" y2=\"" <num> "\"" <stroke> <opacity>? "/>"
<polyline> ::= "<polyline points=\"" <point> (" " <point>){1,5} "\"" <polyline_fill> <stroke> <opacity>? "/>"
<polyline_fill> ::= " fill=\"none\"" | " fill=\"" <color> "\""
<polygon> ::= "<polygon points=\"" <point> (" " <point>){2,5} "\"" <paint> "/>"
<path> ::= "<path d=\"" <path_data> "\"" <transform>? <paint> "/>"
<point> ::= <num> "," <num> | <num> " " <num>

# Path data: absolute and relative M/L/H/V/C/Q/A/Z
<path_data> ::= "M" <sp> <num> <sep> <num> (" " <segment>){1,6} <close>?
<close> ::= " Z" | " z"
<segment> ::= "L" <sp> <num> <sep> <num> | "l" <sp> <snum> <sep> <snum> | "H" <sp> <num> | "h" <sp> <snum> | "V" <sp> <num> | "v" <sp> <snum> | "C" <sp> <num> <sep> <num> <sep> <num> <sep> <num> <sep> <num> <sep> <num> | "c" <sp> <snum> <sep> <snum> <sep> <snum> <sep> <snum> <sep> <snum> <sep> <snum> | "Q" <sp> <num> <sep> <num> <sep> <num> <sep> <num> | "q" <sp> <snum> <sep> <snum> <sep> <snum> <sep> <snum> | "A" <sp> <pos> <sep> <pos> " " <angle> " " <flag> " " <flag> " " <num> <sep> <num> | "a" <sp> <pos> <sep> <pos> " " <angle> " " <flag> " " <flag> " " <snum> <sep> <snum> | "z m" <sp> <snum> <sep> <snum>
<flag> ::= "0" | "1"
<sp> ::= "" | " "
<sep> ::= " " | ","

# Groups with transforms; one level of nesting
<group> ::= "<g" <transform> <group_paint>? ">" (<nl> "  " <group_item>){1,3} <nl> "</g>"
<group_item> ::= <shape> | <inner_group>
<inner_group> ::= "<g" <transform> <group_paint>? ">" (<nl> "    " <shape>){1,2} <nl> "  </g>"
<group_paint> ::= " fill=\"" <color> "\"" | " stroke=\"" <color> "\"" | " opacity=\"" <unit_interval> "\"" | " fill=\"" <color> "\" opacity=\"" <unit_interval> "\""
<transform> ::= " transform=\"" <transform_item> (" " <transform_item>){0,2} "\""
<transform_item> ::= "translate(" <snum> ")" | "translate(" <snum> <sep> <snum> ")" | "scale(" <scale> ")" | "scale(" <scale> <sep> <scale> ")" | "rotate(" <angle> ")" | "rotate(" <angle> " " <num> " " <num> ")" | "skewX(" <skew> ")" | "skewY(" <skew> ")" | "matrix(" <scale> " 0 0 " <scale> " " <snum> " " <snum> ")"
<scale> ::= "0.5" | "0.75" | "1" | "1.25" | "1.5" | "2" | "-1"
<angle> ::= r"[0-9]" | r"[1-9][0-9]" | "-" r"[1-9]" | "-" r"[1-9][0-9]" | "1" r"[0-7][0-9]"
<skew> ::= r"[0-9]" | r"[1-5][0-9]" | "-" r"[1-9]" | "-" r"[1-5][0-9]"

# Paint for ordinary shapes: attributes or a style attribute
<paint> ::= <fill>? <stroke>? <opacity>? | <style>
<fill> ::= " fill=\"" <color> "\"" | " fill=\"none\""
<stroke> ::= " stroke=\"" <color> "\"" <stroke_width>? <linecap>? <linejoin>? <dasharray>?
<stroke_width> ::= " stroke-width=\"" <width> "\""
<linecap> ::= " stroke-linecap=\"" ("butt" | "round" | "square") "\""
<linejoin> ::= " stroke-linejoin=\"" ("miter" | "round" | "bevel") "\""
<dasharray> ::= " stroke-dasharray=\"" <pos> <sep> <pos> "\""
<opacity> ::= " opacity=\"" <unit_interval> "\"" | " fill-opacity=\"" <unit_interval> "\"" | " stroke-opacity=\"" <unit_interval> "\""
<style> ::= " style=\"fill:" <color> <style_stroke>? <style_opacity>? "\""
<style_stroke> ::= ";stroke:" <color> | ";stroke:" <color> ";stroke-width:" <width>
<style_opacity> ::= ";opacity:" <unit_interval> | ";fill-opacity:" <unit_interval>
<width> ::= "0.5" | r"[1-6]" | r"[1-5]" ".5"
<unit_interval> ::= "0" | "1" | "0." r"[0-9]" | "0." r"[0-9][1-9]" | "1.0"

# Gradient g1 and the shapes that use it
<gradient> ::= <nl> "<linearGradient id=\"g1\"" <grad_vector>? <grad_units>? <spread>? ">" <stops> <nl> "</linearGradient>"
<grad_vector> ::= " x1=\"" <percent> "\" y1=\"" <percent> "\" x2=\"" <percent> "\" y2=\"" <percent> "\""
<grad_units> ::= " gradientUnits=\"objectBoundingBox\"" | " gradientUnits=\"userSpaceOnUse\""
<spread> ::= " spreadMethod=\"" ("pad" | "reflect" | "repeat") "\""
<stops> ::= <stop_first> <stop_last> | <stop_first> <stop_middle> <stop_last>
<stop_first> ::= <nl> "  <stop offset=\"0\"" <stop_paint> "/>"
<stop_middle> ::= <nl> "  <stop offset=\"" ("0." r"[1-9]" | r"[1-9]0%") "\"" <stop_paint> "/>"
<stop_last> ::= <nl> "  <stop offset=\"" ("1" | "100%") "\"" <stop_paint> "/>"
<stop_paint> ::= " stop-color=\"" <color> "\"" (" stop-opacity=\"" <unit_interval> "\"")? | " style=\"stop-color:" <color> (";stop-opacity:" <unit_interval>)? "\""
<percent> ::= r"[0-9]" "%" | r"[1-9][0-9]" "%" | "100%"
<grad_shape> ::= "<rect x=\"" <num> "\" y=\"" <num> "\" width=\"" <pos> "\" height=\"" <pos> "\"" <corner>? <grad_paint> "/>" | "<circle cx=\"" <num> "\" cy=\"" <num> "\" r=\"" <pos> "\"" <grad_paint> "/>" | "<ellipse cx=\"" <num> "\" cy=\"" <num> "\" rx=\"" <pos> "\" ry=\"" <pos> "\"" <grad_paint> "/>"
<grad_paint> ::= " fill=\"url(#g1)\"" <stroke>? <opacity>? | " fill=\"" <color> "\" stroke=\"url(#g1)\"" <stroke_width>? | " style=\"fill:url(#g1)" <style_stroke>? "\""

# Reusable shape s1 and <use> elements that draw it
<reusable> ::= <nl> <reusable_shape>
<reusable_shape> ::= "<rect id=\"s1\" x=\"" <num> "\" y=\"" <num> "\" width=\"" <pos> "\" height=\"" <pos> "\"" <reusable_paint>? "/>" | "<circle id=\"s1\" cx=\"" <num> "\" cy=\"" <num> "\" r=\"" <pos> "\"" <reusable_paint>? "/>" | "<ellipse id=\"s1\" cx=\"" <num> "\" cy=\"" <num> "\" rx=\"" <pos> "\" ry=\"" <pos> "\"" <reusable_paint>? "/>" | "<path id=\"s1\" d=\"" <path_data> "\"" <reusable_paint>? "/>"
<reusable_paint> ::= <stroke> | " fill=\"" <color> "\"" <stroke>?
<use> ::= "<use xlink:href=\"#s1\"" <use_position>? <transform>? <use_paint>? "/>"
<use_grad> ::= "<use xlink:href=\"#s1\"" <use_position>? <transform>? <use_grad_paint>? "/>"
<use_position> ::= " x=\"" <snum> "\" y=\"" <snum> "\""
<use_paint> ::= " fill=\"" <color> "\"" <opacity>?
<use_grad_paint> ::= <use_paint> | " fill=\"url(#g1)\""

# Colors: #rgb, #rrggbb, rgb() with integers or percentages, and SVG names
<color> ::= <hex3> | <hex6> | <rgb_int> | <rgb_percent> | <named>
<hex3> ::= "#" r"[0-9a-fA-F]{3}"
<hex6> ::= "#" r"[0-9a-f]{6}" | "#" r"[0-9A-F]{6}"
<rgb_int> ::= "rgb(" <byte> "," <sp> <byte> "," <sp> <byte> ")"
<rgb_percent> ::= "rgb(" <pct> "%," <sp> <pct> "%," <sp> <pct> "%)"
<byte> ::= r"[0-9]" | r"[1-9][0-9]" | "1" r"[0-9][0-9]" | "2" r"[0-4][0-9]" | "25" r"[0-5]"
<pct> ::= r"[0-9]" | r"[1-9][0-9]" | "100"
<named> ::= "black" | "white" | "red" | "green" | "blue" | "yellow" | "teal" | "navy" | "orange" | "purple" | "gold" | "maroon" | "olive" | "silver" | "gray" | "coral" | "crimson" | "indigo" | "orchid" | "salmon" | "tomato" | "steelblue"

# Numbers in user units
<num> ::= r"[0-9]" | r"[1-5][0-9]" | r"[0-9]" "." r"[0-9]" | r"[1-5][0-9]" "." r"[0-9]"
<snum> ::= <num> | "-" <pos>
<pos> ::= r"[1-9]" | r"[1-3][0-9]" | r"[1-9]" "." r"[0-9]" | "0." r"[1-9]"
