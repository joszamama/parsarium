<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned laminas/laminas-xml 1.8.0.
spl_autoload_register(function (string $class): void {
    $prefix = 'Laminas\\Xml\\';
    if (str_starts_with($class, $prefix)) {
        require __DIR__ . '/vendor/laminas/laminas-xml/src/' . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
    }
});
