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
    'rhukster/dom-sanitizer' => 'rhukster',
    'atelier/rasterizer' => 'rasterizer',
    'itools/svgsecuritycheck' => 'itools',
    'mober/phpsvg' => 'mober',
    'mgrulich/php-svg-lib' => 'mgrulich',
    'mediashowroom/php-svg' => 'mediashowroom',
    'choowx/rasterize-svg' => 'choowx',
    'phil/svg-sanitizer' => 'phil',
    'decmuc/svgsanitizer' => 'decmuc',
    'yoya/php-svg' => 'yoya',
    'renfordt/php-svg' => 'renfordt',
    'bitandblack/image-information' => 'bitandblack',
    'darylldoyle/safe-svg' => 'safe_svg',
    'laratusk/larasvg' => 'laratusk',
    default => throw new InvalidArgumentException('unknown package: ' . $package),
};
    require __DIR__ . '/vendor/autoload.php';

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
    case 'rhukster/dom-sanitizer':
        $sanitized = (new \Rhukster\DomSanitizer\DOMSanitizer(\Rhukster\DomSanitizer\DOMSanitizer::SVG))
            ->sanitize(file_get_contents($path));
        $doc = new DOMDocument();
        if (!$doc->loadXML($sanitized)) {
            throw new RuntimeException('sanitized SVG is not XML');
        }
        $rects = $doc->getElementsByTagName('rect');
        $output = ['root' => $doc->documentElement->localName,
            'rectangles' => $rects->length, 'first_fill' => $rects->item(0)->getAttribute('fill')];
        break;
    case 'atelier/rasterizer':
        $bitmap = \Atelier\Rasterizer\Rasterizer::rsvgConvert()->rasterize(
            \Atelier\Rasterizer\Svg\SvgInput::fromFile($path));
        $size = getimagesizefromstring($bitmap->contents);
        $image = imagecreatefromstring($bitmap->contents);
        $red = imagecolorsforindex($image, imagecolorat($image, 0, 0));
        $green = imagecolorsforindex($image, imagecolorat($image, 1, 0));
        $output = ['width' => $size[0], 'height' => $size[1],
            'left_rgb' => [$red['red'], $red['green'], $red['blue']],
            'right_rgb' => [$green['red'], $green['green'], $green['blue']]];
        break;
    case 'itools/svgsecuritycheck':
        $result = \Itools\SvgSecurityCheck\SvgSecurityCheck::checkFile($path);
        $output = ['accepted_svg' => $result->ok, 'violations' => count($result->errors)];
        break;
    case 'mober/phpsvg':
        $document = new \mober\phpsvg\SVGDocument($path);
        $output = ['width' => $document->getWidth(), 'height' => $document->getHeight(),
            'rectangles' => count($document->xpath('//*[local-name()="rect"]'))];
        break;
    case 'mgrulich/php-svg-lib':
        $document = new \Svg\Document();
        $document->loadFile($path);
        $size = $document->getDimensions();
        $output = ['width' => (int) $size['width'], 'height' => (int) $size['height']];
        break;
    case 'mediashowroom/php-svg':
        $image = \SVG\SVGImage::fromFile($path);
        $root = $image->getDocument();
        $output = ['width' => (string) $root->getWidth(), 'height' => (string) $root->getHeight(),
            'rectangles' => $root->countChildren()];
        break;
    case 'choowx/rasterize-svg':
        $png = \Choowx\RasterizeSvg\Svg::make(file_get_contents($path))->toPng();
        $size = getimagesizefromstring($png);
        $image = imagecreatefromstring($png);
        $red = imagecolorsforindex($image, imagecolorat($image, 0, 0));
        $green = imagecolorsforindex($image, imagecolorat($image, 1, 0));
        $output = ['width' => $size[0], 'height' => $size[1],
            'left_rgb' => [$red['red'], $red['green'], $red['blue']],
            'right_rgb' => [$green['red'], $green['green'], $green['blue']]];
        break;
    case 'phil/svg-sanitizer':
        $result = (new \Phil\SvgSanitizer\SvgSanitizer())->sanitize(file_get_contents($path));
        $doc = new DOMDocument();
        if (!$doc->loadXML($result->svg)) {
            throw new RuntimeException('sanitized SVG is not XML');
        }
        $rects = $doc->getElementsByTagName('rect');
        $output = ['rectangles' => $rects->length, 'first_fill' => $rects->item(0)->getAttribute('fill')];
        break;
    case 'decmuc/svgsanitizer':
        $result = \decMuc\SvgSanitizer\SvgSanitizer::isSafe(file_get_contents($path));
        if (!$result['status']) {
            throw new RuntimeException('SVG sanitizer rejected valid control');
        }
        $doc = new DOMDocument();
        if (!$doc->loadXML($result['svg'])) {
            throw new RuntimeException('sanitized SVG is not XML');
        }
        $rects = $doc->getElementsByTagName('rect');
        $output = ['rectangles' => $rects->length, 'first_fill' => $rects->item(0)->getAttribute('fill')];
        break;
    case 'yoya/php-svg':
        $image = \SVG\SVGImage::fromFile($path);
        $root = $image->getDocument();
        $output = ['width' => (string) $root->getWidth(), 'height' => (string) $root->getHeight(),
            'rectangles' => $root->countChildren()];
        break;
    case 'renfordt/php-svg':
        $image = \SVG\SVG::fromFile($path);
        $root = $image->getDocument();
        $rects = $root->getElementsByTagName('rect');
        $output = ['width' => (string) $root->getWidth(), 'height' => (string) $root->getHeight(),
            'rectangles' => count($rects)];
        break;
    case 'bitandblack/image-information':
        $image = new \BitAndBlack\ImageInformation\Image(
            new \BitAndBlack\ImageInformation\Source\File($path));
        $size = $image->getSize();
        $output = ['width' => (int) $size['width'], 'height' => (int) $size['height']];
        break;
    case 'darylldoyle/safe-svg':
        // Supply WordPress's default filter behavior for this package's public helper.
        define('ABSPATH', __DIR__);
        function get_option($key) { return false; }
        function apply_filters($name, $value) { return $value; }
        $base = __DIR__ . '/safe_svg/vendor/darylldoyle/safe-svg/includes/';
        require $base . 'safe-svg-tags.php';
        require $base . 'safe-svg-attributes.php';
        require $base . 'safe-svg-sanitizer.php';
        $cleaned = \SafeSvg\Svg_Sanitizer::sanitize_markup(file_get_contents($path));
        if ($cleaned === false) {
            throw new RuntimeException('safe-svg rejected valid control');
        }
        $doc = new DOMDocument();
        if (!$doc->loadXML($cleaned)) {
            throw new RuntimeException('sanitized SVG is not XML');
        }
        $rects = $doc->getElementsByTagName('rect');
        $output = ['rectangles' => $rects->length, 'first_fill' => $rects->item(0)->getAttribute('fill')];
        break;
    case 'laratusk/larasvg':
        \Illuminate\Support\Facades\Process::swap(new \Illuminate\Process\Factory());
        $converter = new \Laratusk\Larasvg\Converters\RsvgConvertConverter(
            $path, getenv('PARSARIUM_RSVG_CONVERT') ?: '/opt/homebrew/bin/rsvg-convert');
        $png = $converter->toStdout('png');
        $size = getimagesizefromstring($png);
        $image = imagecreatefromstring($png);
        $red = imagecolorsforindex($image, imagecolorat($image, 0, 0));
        $green = imagecolorsforindex($image, imagecolorat($image, 1, 0));
        $output = ['width' => $size[0], 'height' => $size[1],
            'left_rgb' => [$red['red'], $red['green'], $red['blue']],
            'right_rgb' => [$green['red'], $green['green'], $green['blue']]];
        break;
}
echo json_encode($output, JSON_THROW_ON_ERROR) . PHP_EOL;
