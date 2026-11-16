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
    'magento/zend-pdf' => 'zend_pdf',
    'webklex/laravel-pdfmerger' => 'webklex',
    'jurosh/pdf-merge' => 'jurosh',
    'karriere/pdf-merge' => 'karriere',
    'howtomakeaturn/pdfinfo' => 'pdfinfo',
    'rafikhaceb/tcpdi' => 'rafikhaceb',
    'andreaventuri/tcpdi' => 'andreaventuri',
    'tomsgu/pdf-merger' => 'tomsgu',
    'gufy/pdftohtml-php' => 'gufy',
    default => '',
};
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
        $output = ['pdf_header' => str_starts_with($merged, '%PDF-'), 'page_objects' => preg_match_all('~/Type\s*/Page\b~', $merged)];
        break;
    case 'magento/zend-pdf':
        $document = \Zend_Pdf::load($path);
        $output = ['pages' => count($document->pages), 'title' => $document->properties['Title'] ?? null];
        break;
    case 'webklex/laravel-pdfmerger':
        $merger = new \Webklex\PDFMerger\PDFMerger(new \Illuminate\Filesystem\Filesystem());
        $merger->addPDF($path, [1]);
        $merger->merge();
        $merged = $merger->output();
        $output = ['pdf_header' => str_starts_with($merged, '%PDF-'), 'page_objects' => preg_match_all('~/Type\s*/Page\b~', $merged)];
        break;
    case 'jurosh/pdf-merge':
        $merged = (new \Jurosh\PDFMerge\PDFMerger())->addPDF($path)->merge('string');
        $output = ['pdf_header' => str_starts_with($merged, '%PDF-'), 'page_objects' => preg_match_all('~/Type\s*/Page\b~', $merged)];
        break;
    case 'karriere/pdf-merge':
        $merger = new \Karriere\PdfMerge\PdfMerge();
        $merger->add($path);
        $merged = $merger->merge('parsarium.pdf', 'S');
        $output = ['pdf_header' => str_starts_with($merged, '%PDF-'), 'page_objects' => preg_match_all('~/Type\s*/Page\b~', $merged)];
        break;
    case 'howtomakeaturn/pdfinfo':
        $document = new \Howtomakeaturn\PDFInfo\PDFInfo($path);
        $output = ['pages' => (int) $document->pages, 'title' => $document->title];
        break;
    case 'rafikhaceb/tcpdi':
    case 'andreaventuri/tcpdi':
        $document = new \TCPDI();
        $pages = $document->setSourceFile($path);
        $template = $document->importPage(1);
        $size = $document->getTemplateSize($template);
        $output = ['pages' => $pages, 'width' => round($size['w']), 'height' => round($size['h'])];
        break;
    case 'tomsgu/pdf-merger':
        $collection = new \Tomsgu\PdfMerger\PdfCollection();
        $collection->addPdf($path);
        $merger = new \Tomsgu\PdfMerger\PdfMerger(new \setasign\Fpdi\Fpdi());
        $merged = $merger->merge($collection, 'parsarium.pdf', \Tomsgu\PdfMerger\PdfMerger::MODE_STRING);
        $output = ['pdf_header' => str_starts_with($merged, '%PDF-'), 'page_objects' => preg_match_all('~/Type\s*/Page\b~', $merged)];
        break;
    case 'gufy/pdftohtml-php':
        \Gufy\PdfToHtml\Config::set('pdfinfo.bin', getenv('PARSARIUM_PDFINFO') ?: '/opt/homebrew/bin/pdfinfo');
        \Gufy\PdfToHtml\Config::set('pdftohtml.bin', getenv('PARSARIUM_PDFTOHTML') ?: '/opt/homebrew/bin/pdftohtml');
        $document = new \Gufy\PdfToHtml\Pdf($path);
        $html = $document->html();
        $text = trim(preg_replace('/\s+/u', ' ', html_entity_decode(strip_tags($html))));
        $output = ['pages' => (int) $document->getPages(), 'text' => $text];
        break;
    default:
        throw new InvalidArgumentException('unknown PDF package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
