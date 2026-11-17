<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned symfony/dom-crawler 8.1.10 and its required polyfills.
spl_autoload_register(function (string $class): void {
    $prefixes = ['Symfony\\Component\\DomCrawler\\' => 'dom-crawler',
                 'Symfony\\Polyfill\\Ctype\\' => 'polyfill-ctype',
                 'Symfony\\Polyfill\\Mbstring\\' => 'polyfill-mbstring'];
    foreach ($prefixes as $prefix => $package) {
        if (str_starts_with($class, $prefix)) {
            require __DIR__ . "/vendor/symfony/$package/" . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
        }
    }
});
require __DIR__ . '/vendor/symfony/polyfill-ctype/bootstrap.php';
require __DIR__ . '/vendor/symfony/polyfill-mbstring/bootstrap.php';
