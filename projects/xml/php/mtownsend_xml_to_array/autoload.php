<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned mtownsend/xml-to-array 2.0.1 (psr-4 src/ plus the files entry).
spl_autoload_register(function (string $class): void {
    $prefix = 'Mtownsend\\XmlToArray\\';
    if (str_starts_with($class, $prefix)) {
        require __DIR__ . '/vendor/mtownsend/xml-to-array/src/' . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
    }
});
require __DIR__ . '/vendor/mtownsend/xml-to-array/src/helpers.php';
