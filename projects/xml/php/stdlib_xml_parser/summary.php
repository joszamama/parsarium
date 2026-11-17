<?php
declare(strict_types=1);

// Namespace-aware summary built from ext/xml (XML Parser) events, compared with controls/xml/check_controls.py.
// xml_parser_create_ns runs libxml2's push parser (xmlCreatePushParserCtxt, then xmlParseChunk from xml_parse)
// through ext/xml/compat.c, the expat-compatible SAX layer; the summary is collected in the event handlers
// while xml_parse runs, and the input is never handed to any other parser.
// - Expanded names arrive as URI . SEPARATOR . local. The separator is "\x01": it cannot occur in an RFC 3986
//   URI and is not an XML 1.0 Char, so no well-formed XML 1.0 namespace name or local name contains it.
//   compat.c only uses the first byte of the separator argument.
// - Case folding is on by default in ext/xml; XML_OPTION_CASE_FOLDING is set to false so names keep their case.
// - Namespace declarations come from the start-namespace-declaration handler (libxml2 SAX2 nsDef order).
// - Character data and CDATA both arrive through the character data handler; runs are flushed at element
//   starts and ends, processing instructions and comments, as the expat oracle does.
// - ext/xml has no comment handler; compat.c passes comments to the default handler as "<!--...-->". Any other
//   default-handler data (an unexpanded user-defined entity reference, which needs a DTD) is reported as an
//   error rather than silently summarized.
const PARSARIUM_NS_SEPARATOR = "\x01";

function parsarium_clark(string $name): string {
    $at = strpos($name, PARSARIUM_NS_SEPARATOR);
    return $at === false ? $name : '{' . substr($name, 0, $at) . '}' . substr($name, $at + 1);
}

function parsarium_xml_parse(string $bytes): array {
    $state = ['elements' => [], 'attributes' => [], 'namespaces' => [], 'segments' => [], 'text' => '',
              'declarations' => 0, 'depth' => 0, 'max_depth' => 0, 'unexpected' => null];
    $flush = function () use (&$state): void {
        $segment = trim($state['text'], " \t\n\r");
        if ($segment !== '') { $state['segments'][] = $segment; }
        $state['text'] = '';
    };
    $parser = xml_parser_create_ns('UTF-8', PARSARIUM_NS_SEPARATOR);
    xml_parser_set_option($parser, XML_OPTION_CASE_FOLDING, false);
    xml_parser_set_option($parser, XML_OPTION_SKIP_WHITE, false);
    xml_set_element_handler($parser,
        function ($parser, string $name, array $attributes) use (&$state, $flush): void {
            $flush();
            $state['elements'][] = parsarium_clark($name);
            $state['depth']++;
            $state['max_depth'] = max($state['max_depth'], $state['depth']);
            foreach ($attributes as $key => $value) {
                $state['attributes'][] = parsarium_clark((string) $key) . '=' . $value;
            }
        },
        function ($parser, string $name) use (&$state, $flush): void {
            $flush();
            $state['depth']--;
        });
    xml_set_start_namespace_decl_handler($parser, function ($parser, $prefix, $uri) use (&$state): void {
        $state['declarations']++;
        if ((string) $uri !== '') { $state['namespaces'][(string) $uri] = true; }
    });
    xml_set_character_data_handler($parser, function ($parser, string $data) use (&$state): void {
        $state['text'] .= $data;
    });
    xml_set_processing_instruction_handler($parser, function ($parser, string $target, string $data) use ($flush): void {
        $flush();
    });
    xml_set_default_handler($parser, function ($parser, string $data) use (&$state, $flush): void {
        if (str_starts_with($data, '<!--')) { $flush(); return; }
        $state['unexpected'] ??= $data;
    });
    $ok = xml_parse($parser, $bytes, true);
    if ($ok !== 1) {
        throw new RuntimeException(sprintf('XML parse error %d at line %d: %s', xml_get_error_code($parser),
            xml_get_current_line_number($parser), xml_error_string(xml_get_error_code($parser))));
    }
    if ($state['unexpected'] !== null) {
        throw new RuntimeException('unexpected default-handler data: ' . $state['unexpected']);
    }
    $namespaces = array_keys($state['namespaces']);
    sort($namespaces, SORT_STRING);
    return ['attributes' => $state['attributes'], 'elements' => $state['elements'], 'max_depth' => $state['max_depth'],
            'namespace_declarations' => $state['declarations'], 'namespaces' => $namespaces,
            'root' => $state['elements'][0] ?? null, 'text' => $state['segments']];
}
