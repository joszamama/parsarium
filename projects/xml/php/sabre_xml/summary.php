<?php
declare(strict_types=1);

// Summary of the Clark-notation tree from Sabre\Xml\Reader::parse(), comparable with controls/xml/check_controls.py.
// sabre/xml drops xmlns declarations and keeps text only for elements without child elements.
function parsarium_sabre_summary(array $tree): array {
    $elements = []; $attributes = []; $segments = []; $maxDepth = 0;
    $name = fn (string $clark): string => str_starts_with($clark, '{}') ? substr($clark, 2) : $clark;
    $walk = function (array $node, int $depth) use (&$walk, &$elements, &$attributes, &$segments, &$maxDepth, $name): void {
        $elements[] = $name($node['name']);
        $maxDepth = max($maxDepth, $depth);
        foreach ($node['attributes'] as $key => $attribute) { $attributes[] = $name((string) $key) . '=' . $attribute; }
        if (is_array($node['value'])) {
            foreach ($node['value'] as $child) { $walk($child, $depth + 1); }
        } elseif (is_string($node['value']) && trim($node['value'], " \t\n\r") !== '') {
            $segments[] = trim($node['value'], " \t\n\r");
        }
    };
    $walk($tree, 1);
    return ['attributes' => $attributes, 'elements' => $elements, 'max_depth' => $maxDepth,
            'root' => $elements[0], 'text' => $segments];
}
