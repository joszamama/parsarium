<?php
// This isolated adapter runs the pinned PHP 5/7-only sanitizer under PHP 7.4.
if ($argc !== 2 || !is_file($argv[1])) {
    throw new InvalidArgumentException('usage: php parse_legacy.php LOCAL_SVG');
}
    require __DIR__ . '/vendor/autoload.php';
$sanitized = (new \enshrined\svgSanitize\Sanitizer())->sanitize(file_get_contents($argv[1]));
if ($sanitized === false) {
    throw new RuntimeException('SVG sanitizer rejected valid control');
}
$doc = new DOMDocument();
if (!$doc->loadXML($sanitized)) {
    throw new RuntimeException('sanitized SVG is not XML');
}
$rects = $doc->getElementsByTagName('rect');
$output = array('rectangles' => $rects->length);
if ($rects->length > 0) {
    $output['first_fill'] = $rects->item(0)->getAttribute('fill');
}
echo json_encode($output) . PHP_EOL;
