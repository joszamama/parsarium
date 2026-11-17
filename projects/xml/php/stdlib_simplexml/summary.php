<?php
declare(strict_types=1);

// Namespace-aware summary of a SimpleXMLElement tree, using only the SimpleXML API, compared with
// controls/xml/check_controls.py. SimpleXML has no node-type or namespace-URI accessor, so:
// - children and attributes in document order come from SimpleXMLElement::xpath('*') and xpath('@*')
//   (children()/attributes() without arguments only return unprefixed nodes);
// - an element's namespace is the getNamespaces(false) candidate that self::*[namespace-uri()=...] selects,
//   since getNamespaces(false) also lists the namespaces of the element's prefixed attributes;
// - namespace declarations are getDocNamespaces(false, false): the element's own nsDef, xmlns="" included;
// - text is (string) of the element: its direct text and CDATA concatenated. SimpleXML does not expose
//   separate text nodes, so runs split by child elements, comments or PIs inside one element are merged
//   and placed before the element's children. Neither control has such mixed content.
function parsarium_xpath_literal(string $value): string {
    if (!str_contains($value, '"')) { return '"' . $value . '"'; }
    if (!str_contains($value, "'")) { return "'" . $value . "'"; }
    throw new RuntimeException('namespace URI contains both quote characters');
}

function parsarium_xml_summary(SimpleXMLElement $root): array {
    $state = ['elements' => [], 'attributes' => [], 'namespaces' => [], 'segments' => [],
              'declarations' => 0, 'max_depth' => 0];
    $clark = fn (string $uri, string $local): string => $uri === '' ? $local : '{' . $uri . '}' . $local;
    $walk = function (SimpleXMLElement $element, int $depth) use (&$walk, &$state, $clark): void {
        $uri = '';
        foreach (array_unique(array_values($element->getNamespaces(false))) as $candidate) {
            if ($element->xpath('self::*[namespace-uri()=' . parsarium_xpath_literal($candidate) . ']') !== []) {
                $uri = $candidate;
            }
        }
        $state['elements'][] = $clark($uri, $element->getName());
        $state['max_depth'] = max($state['max_depth'], $depth);
        foreach ($element->getDocNamespaces(false, false) as $declared) {
            $state['declarations']++;
            if ($declared !== '') { $state['namespaces'][$declared] = true; }
        }
        foreach ($element->xpath('@*') as $attribute) {
            $state['attributes'][] = $clark(array_values($attribute->getNamespaces(false))[0] ?? '', $attribute->getName())
                . '=' . (string) $attribute;
        }
        $segment = trim((string) $element, " \t\n\r");
        if ($segment !== '') { $state['segments'][] = $segment; }
        foreach ($element->xpath('*') as $child) {
            $walk($child, $depth + 1);
        }
    };
    $walk($root, 1);
    $namespaces = array_keys($state['namespaces']);
    sort($namespaces, SORT_STRING);
    return ['attributes' => $state['attributes'], 'elements' => $state['elements'], 'max_depth' => $state['max_depth'],
            'namespace_declarations' => $state['declarations'], 'namespaces' => $namespaces,
            'root' => $state['elements'][0] ?? null, 'text' => $state['segments']];
}
