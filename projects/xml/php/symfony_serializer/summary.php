<?php
declare(strict_types=1);

// Summary of an XmlEncoder::decode() result, comparable with an expat oracle in qualified-name mode.
// decode() returns the content of the root element, not its name: child elements are keyed by their
// qualified (prefix:local) name, repeated siblings become a list, attributes are '@'-keys (numeric values
// type-cast), '#' holds an element's text next to attributes, and the root's in-scope namespace
// declarations are added as '@xmlns' / '@xmlns:prefix' keys. Elements are walked in key order, so the
// summary lists root descendants, their attributes and text in document order when same-named siblings
// are adjacent (true for both shared controls).
function parsarium_xml_encoder_summary(mixed $decoded): array {
    $elements = []; $attributes = []; $segments = []; $namespaces = []; $maxDepth = 1;
    $walk = function (mixed $value, int $depth) use (&$walk, &$elements, &$attributes, &$segments, &$namespaces, &$maxDepth): void {
        $maxDepth = max($maxDepth, $depth);
        if (!is_array($value)) {
            if ((string) $value !== '') { $segments[] = (string) $value; }
            return;
        }
        foreach ($value as $key => $item) {
            $key = (string) $key;
            if ($depth === 1 && ($key === '@xmlns' || str_starts_with($key, '@xmlns:'))) {
                $namespaces[substr($key, 7)] = $item;
            } elseif (str_starts_with($key, '@')) {
                $attributes[] = substr($key, 1) . '=' . (is_string($item) ? $item : json_encode($item));
            } elseif ($key === '#') {
                if ((string) $item !== '') { $segments[] = (string) $item; }
            } else {
                foreach (is_array($item) && array_is_list($item) ? $item : [$item] as $child) {
                    $elements[] = $key;
                    $walk($child, $depth + 1);
                }
            }
        }
    };
    $walk($decoded, 1);
    ksort($namespaces, SORT_STRING);
    return ['attributes' => $attributes, 'elements' => $elements, 'max_depth' => $maxDepth,
            'root_namespaces' => $namespaces, 'text' => $segments];
}
