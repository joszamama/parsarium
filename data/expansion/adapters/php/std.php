<?php
// PHP bundled-extension JSON/XML control adapter. Usage: php std.php <api> <control>
[$api, $path] = [$argv[1], $argv[2]];
$data = file_get_contents($path);
$ns = 'urn:parsarium:control';
switch ($api) {
  case 'json_decode':
    $d = json_decode($data, true, 512, JSON_THROW_ON_ERROR);
    $k = array_keys($d); sort($k);
    $out = ['keys' => $k, 'items' => count($d['items']), 'text' => $d['nested']['text'], 'count' => $d['count']];
    break;
  case 'simplexml_load_string':
    $r = simplexml_load_string($data);
    if ($r === false) exit(2);
    $c = $r->children($ns); $ids = []; $texts = [];
    foreach ($c->item as $i) { $ids[] = (string)$i->attributes()['id']; $texts[] = (string)$i; }
    $out = ['root' => '{' . $ns . '}' . $r->getName(), 'children' => count($c), 'ids' => $ids, 'texts' => $texts];
    break;
  case 'DOMDocument::loadXML':
    $doc = new DOMDocument();
    if (!$doc->loadXML($data)) exit(2);
    $r = $doc->documentElement; $kids = []; $ids = []; $texts = [];
    foreach ($r->childNodes as $n) if ($n->nodeType === XML_ELEMENT_NODE) $kids[] = $n;
    foreach ($kids as $n) if ($n->localName === 'item') { $ids[] = $n->getAttribute('id'); $texts[] = $n->textContent; }
    $out = ['root' => '{' . $r->namespaceURI . '}' . $r->localName, 'children' => count($kids), 'ids' => $ids, 'texts' => $texts];
    break;
  case 'XMLReader::XML':
    $x = XMLReader::XML($data);
    $root = null; $children = 0; $ids = []; $texts = [];
    while ($x->read()) {
      if ($x->nodeType !== XMLReader::ELEMENT) continue;
      if ($x->depth === 0) $root = '{' . $x->namespaceURI . '}' . $x->localName;
      elseif ($x->depth === 1) {
        $children++;
        if ($x->localName === 'item') { $ids[] = $x->getAttribute('id'); $texts[] = $x->readString(); }
      }
    }
    $out = ['root' => $root, 'children' => $children, 'ids' => $ids, 'texts' => $texts];
    break;
  default: exit(3);
}
ksort($out);
echo json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
