<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}
$vendor = match ($package) {
    'mikehaertl/php-pdftk' => 'pdftk',
    'propa/tcpdi' => 'tcpdi',
    'popphp/pop-pdf' => 'pop_pdf',
    'iio/libmergepdf' => 'libmergepdf',
    'ottosmops/pdftotext' => 'ottosmops',
    default => '',
};
require __DIR__ . '/' . ($vendor === '' ? '' : $vendor . '/') . 'vendor/autoload.php';

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
    case 'mikehaertl/php-pdftk':
        $pdftk = getenv('PARSARIUM_PDFTK') ?: '/opt/homebrew/bin/pdftk';
        $document = new \mikehaertl\pdftk\Pdf($path, ['command' => $pdftk]);
        $data = $document->getData();
        if ($data === false) {
            throw new RuntimeException('pdftk could not parse PDF data: ' . $document->getError());
        }
        $fields = $data->__toArray();
        $output = ['pages' => (int) ($fields['NumberOfPages'] ?? 0), 'title' => $fields['Info']['Title'] ?? null];
        break;
    case 'propa/tcpdi':
        $document = new \TCPDI();
        $pages = $document->setSourceFile($path);
        $template = $document->importPage(1);
        $size = $document->getTemplateSize($template);
        $output = ['pages' => $pages, 'width' => round($size['w']), 'height' => round($size['h'])];
        break;
    case 'popphp/pop-pdf':
        $output = ['text' => trim(\Pop\Pdf\Pdf::extractTextFromFile($path))];
        break;
    case 'ottosmops/pdftotext':
        $output = ['text' => trim((new \Ottosmops\Pdftotext\Extract())->pdf($path)->text())];
        break;
    case 'iio/libmergepdf':
        $merger = new \iio\libmergepdf\Merger();
        $merger->addFile($path);
        $merged = $merger->merge();
        $output = ['pdf_header' => str_starts_with($merged, '%PDF-'), 'page_objects' => substr_count($merged, '/Type /Page ')];
        break;
    default:
        throw new InvalidArgumentException('unknown PDF package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
