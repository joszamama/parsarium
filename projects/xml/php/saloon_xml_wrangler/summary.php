<?php
declare(strict_types=1);

use Saloon\XmlWrangler\Data\Element;

// Summary of the Element tree returned by XmlReader::elements(), comparable with oracle.py.
// XML Wrangler keys elements and attributes by raw qualified name and resolves no namespace URI.
// Repeated same-name children arrive as one Element whose content is a list; each list item is one
// occurrence of that name. Namespace declarations arrive as xmlns/xmlns:* attributes (only those
// with a non-empty URI); they are listed per element, sorted by attribute name, because the package
// does not keep their source order. Text is the string content of elements without child elements.
function parsarium_wrangler_summary(array $elements): array {
    $names = []; $attributes = []; $declarations = []; $text = []; $maxDepth = 0;
    $walk = function (string $name, Element $element, int $depth) use (&$walk, &$names, &$attributes, &$declarations, &$text, &$maxDepth): void {
        $names[] = $name;
        $maxDepth = max($maxDepth, $depth);
        $declared = [];
        foreach ($element->getAttributes() as $key => $value) {
            if ($key === 'xmlns' || str_starts_with((string) $key, 'xmlns:')) {
                $declared["$key"] = "$name $key=$value";
            } else {
                $attributes[] = "$key=$value";
            }
        }
        ksort($declared, SORT_STRING);
        array_push($declarations, ...array_values($declared));
        $content = $element->getContent();
        if (!is_array($content)) {
            $text[] = (string) $content;
            return;
        }
        foreach ($content as $childName => $child) {
            $group = $child->getContent();
            if (is_array($group) && array_is_list($group) && $group !== []) {
                foreach ($group as $occurrence) { $walk((string) $childName, $occurrence, $depth + 1); }
            } else {
                $walk((string) $childName, $child, $depth + 1);
            }
        }
    };
    foreach ($elements as $name => $element) { $walk((string) $name, $element, 1); }
    return ['attributes' => $attributes, 'elements' => $names, 'leaf_text' => $text,
            'max_depth' => $maxDepth, 'namespace_declarations' => $declarations, 'root' => $names[0]];
}
