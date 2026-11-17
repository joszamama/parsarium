<?php
declare(strict_types=1);

// Namespace-aware summary of an XML document read with XMLReader, matching controls/xml/check_controls.py.
function parsarium_xml_summary(XMLReader $reader): array {
    $elements = []; $attributes = []; $namespaces = []; $segments = [];
    $declarations = 0; $depth = 0; $maxDepth = 0; $text = '';
    $flush = function () use (&$text, &$segments): void {
        $segment = trim($text, " \t\n\r");
        if ($segment !== '') { $segments[] = $segment; }
        $text = '';
    };
    $clark = fn (?string $uri, string $local): string => ($uri ?? '') === '' ? $local : '{' . $uri . '}' . $local;
    while ($reader->read()) {
        switch ($reader->nodeType) {
            case XMLReader::ELEMENT:
                $flush();
                $elements[] = $clark($reader->namespaceURI, $reader->localName);
                $empty = $reader->isEmptyElement;
                $maxDepth = max($maxDepth, ++$depth);
                if ($reader->moveToFirstAttribute()) {
                    do {
                        if ($reader->namespaceURI === 'http://www.w3.org/2000/xmlns/') {
                            $declarations++;
                            if ($reader->value !== '') { $namespaces[$reader->value] = true; }
                        } else {
                            $attributes[] = $clark($reader->namespaceURI, $reader->localName) . '=' . $reader->value;
                        }
                    } while ($reader->moveToNextAttribute());
                    $reader->moveToElement();
                }
                if ($empty) { $flush(); $depth--; }
                break;
            case XMLReader::END_ELEMENT:
                $flush();
                $depth--;
                break;
            case XMLReader::TEXT:
            case XMLReader::CDATA:
            case XMLReader::WHITESPACE:
            case XMLReader::SIGNIFICANT_WHITESPACE:
                $text .= $reader->value;
                break;
            case XMLReader::COMMENT:
            case XMLReader::PI:
                $flush();
                break;
        }
    }
    $namespaces = array_keys($namespaces);
    sort($namespaces, SORT_STRING);
    return ['attributes' => $attributes, 'elements' => $elements, 'max_depth' => $maxDepth,
            'namespace_declarations' => $declarations, 'namespaces' => $namespaces,
            'root' => $elements[0] ?? null, 'text' => $segments];
}
