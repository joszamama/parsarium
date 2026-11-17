<?php
declare(strict_types=1);

// Summary of an XmlToArray::convert($xml, true) result, comparable with an expat oracle in qualified-name mode.
// convert() keys child elements by DOM tagName (prefix:local), groups same-named siblings into a list and
// unwraps single children; an element with only text becomes that trimmed string, or ['@content' => text]
// when it has attributes; attributes sit under '@attributes' keyed by the DOMNamedNodeMap iteration key
// (the local name, so prefixes are dropped); '@root' is the root tagName. No namespace URI or xmlns
// declaration is returned, so none is summarized. Children are walked in key order, so the summary is in
// document order when same-named siblings are adjacent (true for both shared controls).
function parsarium_xml_to_array_summary(array $decoded): array {
    $elements = []; $attributes = []; $segments = []; $maxDepth = 1;
    $walk = function (mixed $value, int $depth) use (&$walk, &$elements, &$attributes, &$segments, &$maxDepth): void {
        $maxDepth = max($maxDepth, $depth);
        if (!is_array($value)) {
            if ((string) $value !== '') { $segments[] = (string) $value; }
            return;
        }
        foreach ($value['@attributes'] ?? [] as $name => $text) { $attributes[] = "$name=$text"; }
        if (isset($value['@content']) && (string) $value['@content'] !== '') { $segments[] = (string) $value['@content']; }
        foreach ($value as $key => $item) {
            $key = (string) $key;
            if (str_starts_with($key, '@')) { continue; }
            // Element arrays have name keys only, so a non-empty list means repeated siblings; [] is one empty element.
            foreach (is_array($item) && $item !== [] && array_is_list($item) ? $item : [$item] as $child) {
                $elements[] = $key;
                $walk($child, $depth + 1);
            }
        }
    };
    $walk($decoded, 1);
    return ['attributes' => $attributes, 'elements' => $elements, 'max_depth' => $maxDepth,
            'root' => (string) ($decoded['@root'] ?? ''), 'text' => $segments];
}
