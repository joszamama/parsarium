<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned imangazaliev/didom 2.0.1.
spl_autoload_register(function (string $class): void {
    $prefix = 'DiDom\\';
    if (str_starts_with($class, $prefix)) {
        require __DIR__ . '/vendor/imangazaliev/didom/src/DiDom/' . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
    }
});
