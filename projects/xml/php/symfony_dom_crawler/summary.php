<?php
declare(strict_types=1);

use Symfony\Component\DomCrawler\Crawler;

// Summary of an XML Crawler, comparable with controls/xml/check_controls.py.
// Traversal uses Crawler::children(), each(), nodeName(), attr() and text(); the expanded
// {namespace}local name and the attribute list come from the selected DOM node. The xpath map counts
// each element name through Crawler::filterXPath(): prefixed names use Crawler's namespace
// discovery, while default-namespace URIs are registered as ns1, ns2, ... with registerNamespace(),
// because Crawler's "default" prefix resolves to the last default declaration in the document.
function parsarium_crawler_summary(Crawler $crawler): array {
    $elements = []; $attributes = []; $segments = []; $xpath = []; $defaults = []; $maxDepth = 0;
    $clark = fn (?string $uri, string $local): string => $uri === null || $uri === '' ? $local : "{{$uri}}$local";
    $walk = function (Crawler $node, int $depth) use (&$walk, &$elements, &$attributes, &$segments, &$xpath, &$defaults, &$maxDepth, $clark, $crawler): void {
        $element = $node->getNode(0);
        $elements[] = $clark($element->namespaceURI, $element->localName);
        $maxDepth = max($maxDepth, $depth);
        foreach ($element->attributes as $attribute) {
            $attributes[] = $clark($attribute->namespaceURI, $attribute->localName) . '=' . $node->attr($attribute->nodeName);
        }
        $qname = $node->nodeName();
        if (!str_contains($qname, ':') && $element->namespaceURI !== null) {
            if (!isset($defaults[$element->namespaceURI])) {
                $defaults[$element->namespaceURI] = 'ns' . (count($defaults) + 1);
                $crawler->registerNamespace($defaults[$element->namespaceURI], $element->namespaceURI);
            }
            $qname = $defaults[$element->namespaceURI] . ':' . $qname;
        }
        $xpath["//$qname"] ??= $crawler->filterXPath("//$qname")->count();
        $children = $node->children();
        if ($children->count() === 0) {
            $text = $node->text();
            if ($text !== '') { $segments[] = $text; }
        }
        $children->each(fn (Crawler $child) => $walk($child, $depth + 1));
    };
    $walk($crawler, 1);
    return ['attributes' => $attributes, 'elements' => $elements, 'max_depth' => $maxDepth,
            'root' => $elements[0], 'text' => $segments, 'xpath' => $xpath];
}
