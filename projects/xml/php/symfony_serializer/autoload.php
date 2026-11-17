<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned symfony/serializer 8.1.11 and its required packages.
spl_autoload_register(function (string $class): void {
    $prefixes = ['Symfony\\Component\\Serializer\\' => 'serializer',
                 'Symfony\\Polyfill\\Ctype\\' => 'polyfill-ctype'];
    foreach ($prefixes as $prefix => $package) {
        if (str_starts_with($class, $prefix)) {
            require __DIR__ . "/vendor/symfony/$package/" . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
        }
    }
});
require __DIR__ . '/vendor/symfony/deprecation-contracts/function.php';
require __DIR__ . '/vendor/symfony/polyfill-ctype/bootstrap.php';
