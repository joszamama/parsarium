<?php
declare(strict_types=1);
// Composer-equivalent psr-4 autoload for the pinned simplesamlphp/xml-common v3.0.8 and its runtime
// dependencies simplesamlphp/assert v3.0.5 and webmozart/assert 2.1.6 (psr/clock and the Composer
// installer plugin are not needed by DOMDocumentFactory::fromString and are not installed).
spl_autoload_register(function (string $class): void {
    $map = [
        'SimpleSAML\\XMLSchema\\' => '/vendor/simplesamlphp/xml-common/src/XMLSchema/',
        'SimpleSAML\\XML\\' => '/vendor/simplesamlphp/xml-common/src/XML/',
        'SimpleSAML\\XPath\\' => '/vendor/simplesamlphp/xml-common/src/XPath/',
        'SimpleSAML\\Assert\\' => '/vendor/simplesamlphp/assert/src/',
        'Webmozart\\Assert\\' => '/vendor/webmozart/assert/src/',
    ];
    foreach ($map as $prefix => $dir) {
        if (str_starts_with($class, $prefix)) {
            $file = __DIR__ . $dir . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
            if (is_file($file)) { require $file; }
            return;
        }
    }
});
