<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null || !is_file($path)) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE LOCAL_SVG');
}
$vendor = match ($package) {
    'dompdf/php-svg-lib' => 'dompdf',
    'meyfa/php-svg' => 'meyfa',
    'enshrined/svg-sanitize' => 'enshrined',
    'atelier/svg' => 'atelier',
    'mathiasreker/php-svg-optimizer' => 'mathias',
    default => throw new InvalidArgumentException('unknown package: ' . $package),
};
require __DIR__ . '/' . $vendor . '/vendor/autoload.php';

switch ($package) {
    case 'dompdf/php-svg-lib':
        $document = new \Svg\Document();
        $document->loadFile($path);
        $size = $document->getDimensions();
        $output = ['width' => (int) $size['width'], 'height' => (int) $size['height']];
        break;
    case 'meyfa/php-svg':
        $image = \SVG\SVG::fromFile($path);
        if ($image === null) {
            throw new RuntimeException('SVG parser returned null');
        }
        $root = $image->getDocument();
        $rects = $root->getElementsByTagName('rect');
        $output = ['width' => $root->getWidth(), 'height' => $root->getHeight(),
            'rectangles' => count($rects), 'first_rect_width' => $rects[0]->getWidth()];
        break;
    case 'enshrined/svg-sanitize':
        $sanitized = (new \enshrined\svgSanitize\Sanitizer())->sanitize(file_get_contents($path));
        if ($sanitized === false) {
            throw new RuntimeException('SVG sanitizer rejected valid control');
        }
        $doc = new DOMDocument();
        if (!$doc->loadXML($sanitized)) {
            throw new RuntimeException('sanitized SVG is not XML');
        }
        $output = ['root' => $doc->documentElement->localName,
            'rectangles' => $doc->getElementsByTagName('rect')->length,
            'first_fill' => $doc->getElementsByTagName('rect')->item(0)->getAttribute('fill')];
        break;
    case 'atelier/svg':
        $image = \Atelier\Svg\Svg::load($path);
        $rectangles = $image->querySelectorAll('rect');
        $output = ['rectangles' => count($rectangles)];
        break;
    case 'mathiasreker/php-svg-optimizer':
        $optimized = (new \MathiasReker\PhpSvgOptimizer\SvgOptimizer())
            ->withRules(\MathiasReker\PhpSvgOptimizer\Rule::MinifyColors)
            ->optimizeFile($path)->getContent();
        $doc = new DOMDocument();
        if (!$doc->loadXML($optimized)) {
            throw new RuntimeException('optimized SVG is not XML');
        }
        $rects = $doc->getElementsByTagName('rect');
        $output = ['rectangles' => $rects->length, 'first_fill' => $rects->item(0)->getAttribute('fill')];
        break;
}
echo json_encode($output, JSON_THROW_ON_ERROR) . PHP_EOL;
