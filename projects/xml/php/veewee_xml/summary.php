<?php
declare(strict_types=1);

// Summary of a VeeWee\Xml\Encoding\xml_decode() array, comparable with an expat oracle in qualified-name mode.
// xml_decode returns [rootQName => content]. Content is a string for an element without attributes, namespace
// declarations or child elements, else an array with optional '@namespaces' (that element's own xmlns
// declarations, '' for the default namespace), '@attributes' (qualified names, string values), '@value' (text of
// an element without child elements) and child elements keyed by qualified name, same-named siblings grouped
// into a list. Elements are walked in key order, which is document order when same-named siblings are adjacent
// (true for both shared controls). Each declaration is listed as '<element index> <element qname> xmlns[:prefix]=<uri>'.
// Text of elements with child elements, comments and PIs are not exposed.
function parsarium_veewee_summary(array $decoded): array {
    $elements = []; $attributes = []; $namespaces = []; $segments = []; $maxDepth = 0;
    $text = function (string $value) use (&$segments): void {
        $value = trim($value, " \t\n\r");
        if ($value !== '') { $segments[] = $value; }
    };
    $walk = function (string $name, mixed $content, int $depth) use (&$walk, &$elements, &$attributes, &$namespaces, &$maxDepth, $text): void {
        $index = count($elements);
        $elements[] = $name;
        $maxDepth = max($maxDepth, $depth);
        if (is_string($content)) { $text($content); return; }
        foreach ($content as $key => $value) {
            $key = (string) $key;
            if ($key === '@namespaces') {
                foreach ($value as $prefix => $uri) {
                    $namespaces[] = $index . ' ' . $name . ' ' . ($prefix === '' ? 'xmlns' : "xmlns:$prefix") . '=' . $uri;
                }
            } elseif ($key === '@attributes') {
                foreach ($value as $attribute => $item) { $attributes[] = $attribute . '=' . $item; }
            } elseif ($key === '@value') {
                $text($value);
            } else {
                foreach (is_array($value) && array_is_list($value) ? $value : [$value] as $child) {
                    $walk($key, $child, $depth + 1);
                }
            }
        }
    };
    if (count($decoded) !== 1) { throw new UnexpectedValueException('xml_decode must return one root'); }
    $walk((string) array_key_first($decoded), $decoded[array_key_first($decoded)], 1);
    return ['attributes' => $attributes, 'elements' => $elements, 'max_depth' => $maxDepth,
            'namespace_declarations' => $namespaces, 'root' => $elements[0], 'text' => $segments];
}
