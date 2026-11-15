<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';
function parsarium_parse_pdf(string $input): array|false {
 if ($input === '' || strlen($input) > (1 << 20)) return false;
 $path = tempnam('/tmp', 'parsarium-pdf-');
 if ($path === false) throw new RuntimeException('Could not create local input');
 try {
  if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write local input');
  $document = new \setasign\Fpdi\Fpdi();
  $pages = $document->setSourceFile($path);
  $template = $document->importPage(1);
  $size = $document->getTemplateSize($template);
  return ['pages' => $pages, 'width' => (int) round($size['width']), 'height' => (int) round($size['height'])];
 } finally { unlink($path); }
}
