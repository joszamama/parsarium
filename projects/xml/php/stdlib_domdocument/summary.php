<?php
declare(strict_types=1);

// Namespace-aware summary of a DOMDocument tree, matching controls/xml/check_controls.py.
// Namespace declarations come from DOMElement::getAttributeNames(), which lists the element's own
// xmlns / xmlns:prefix declarations (libxml2 nsDef) ahead of its attributes; DOMElement::$attributes
// holds only the non-declaration attributes.
function parsarium_xml_summary(DOMDocument $document): array {
    $state = ['elements' => [], 'attributes' => [], 'namespaces' => [], 'segments' => [],
              'declarations' => 0, 'max_depth' => 0, 'text' => ''];
    $clark = fn (?string $uri, string $local): string => ($uri ?? '') === '' ? $local : '{' . $uri . '}' . $local;
    $flush = function () use (&$state): void {
        $segment = trim($state['text'], " \t\n\r");
        if ($segment !== '') { $state['segments'][] = $segment; }
        $state['text'] = '';
    };
    $walk = function (DOMNode $node, int $depth) use (&$walk, &$state, $clark, $flush): void {
        foreach ($node->childNodes as $child) {
            switch ($child->nodeType) {
                case XML_ELEMENT_NODE:
                    $flush();
                    $state['elements'][] = $clark($child->namespaceURI, $child->localName);
                    $state['max_depth'] = max($state['max_depth'], $depth + 1);
                    foreach ($child->getAttributeNames() as $name) {
                        if ($name === 'xmlns' || str_starts_with($name, 'xmlns:')) {
                            $state['declarations']++;
                            $uri = $child->getAttribute($name);
                            if ($uri !== '') { $state['namespaces'][$uri] = true; }
                        }
                    }
                    foreach ($child->attributes as $attribute) {
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
