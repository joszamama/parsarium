<?php
declare(strict_types=1);

// Namespace-aware summary of a Dom\XMLDocument tree, matching controls/xml/check_controls.py.
// In the PHP 8.4+ DOM API, xmlns / xmlns:prefix declarations are attributes in the
// http://www.w3.org/2000/xmlns/ namespace; they are counted as declarations, not attributes.
function parsarium_xml_summary(Dom\XMLDocument $document): array {
    $xmlns = 'http://www.w3.org/2000/xmlns/';
    $state = ['elements' => [], 'attributes' => [], 'namespaces' => [], 'segments' => [],
              'declarations' => 0, 'max_depth' => 0, 'text' => ''];
    $clark = fn (?string $uri, string $local): string => ($uri ?? '') === '' ? $local : '{' . $uri . '}' . $local;
    $flush = function () use (&$state): void {
        $segment = trim($state['text'], " \t\n\r");
        if ($segment !== '') { $state['segments'][] = $segment; }
        $state['text'] = '';
    };
    $walk = function (Dom\Node $node, int $depth) use (&$walk, &$state, $clark, $flush, $xmlns): void {
        foreach ($node->childNodes as $child) {
            switch ($child->nodeType) {
                case XML_ELEMENT_NODE:
                    $flush();
                    $state['elements'][] = $clark($child->namespaceURI, $child->localName);
                    $state['max_depth'] = max($state['max_depth'], $depth + 1);
                    foreach ($child->attributes as $attribute) {
                        if ($attribute->namespaceURI === $xmlns) {
                            $state['declarations']++;
                            if ($attribute->value !== '') { $state['namespaces'][$attribute->value] = true; }
                            continue;
                        }
                        $state['attributes'][] = $clark($attribute->namespaceURI, $attribute->localName) . '=' . $attribute->value;
                    }
                    $walk($child, $depth + 1);
                    $flush();
                    break;
                case XML_TEXT_NODE:
                case XML_CDATA_SECTION_NODE:
                    $state['text'] .= $child->data;
                    break;
                case XML_COMMENT_NODE:
                case XML_PI_NODE:
                    $flush();
                    break;
            }
        }
    };
    $walk($document, 0);
    $namespaces = array_keys($state['namespaces']);
    sort($namespaces, SORT_STRING);
    return ['attributes' => $state['attributes'], 'elements' => $state['elements'], 'max_depth' => $state['max_depth'],
            'namespace_declarations' => $state['declarations'], 'namespaces' => $namespaces,
            'root' => $state['elements'][0] ?? null, 'text' => $state['segments']];
}
