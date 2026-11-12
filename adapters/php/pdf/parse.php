<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}
require __DIR__ . '/vendor/autoload.php';

switch ($package) {
    case 'smalot/pdfparser':
        $document = (new \Smalot\PdfParser\Parser())->parseFile($path);
        $output = [
            'pages' => count($document->getPages()),
            'text' => trim($document->getText()),
        ];
        break;
    case 'setasign/fpdi':
        $document = new \setasign\Fpdi\Fpdi();
        $pages = $document->setSourceFile($path);
        $template = $document->importPage(1);
        $size = $document->getTemplateSize($template);
        $output = [
            'pages' => $pages,
            'width' => round($size['width']),
            'height' => round($size['height']),
        ];
        break;
    case 'spatie/pdf-to-text':
        $output = ['text' => trim(\Spatie\PdfToText\Pdf::getText($path))];
        break;
    case 'prinsfrank/pdfparser':
        $document = (new \PrinsFrank\PdfParser\PdfParser())->parseFile($path);
        $output = ['text' => trim($document->getText())];
        break;
    case 'asika/pdf2text':
        $output = ['text' => trim((new \Asika\Pdf2text())->decode($path))];
        break;
    case 'tecnickcom/tc-lib-pdf-parser':
        [$xref, $objects] = (new \Com\Tecnick\Pdf\Parser\Parser())->parse(file_get_contents($path));
        $output = [
            'objects' => count($objects),
            'xref_type' => get_debug_type($xref),
        ];
        break;
    default:
        throw new InvalidArgumentException('unknown PDF package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
