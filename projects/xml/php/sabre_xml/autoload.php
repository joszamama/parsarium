<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned sabre/xml 4.1.0 and sabre/uri 3.1.0 sources.
spl_autoload_register(function (string $class): void {
    foreach (['Sabre\\Xml\\' => 'xml', 'Sabre\\Uri\\' => 'uri'] as $prefix => $package) {
        if (str_starts_with($class, $prefix)) {
            require __DIR__ . "/vendor/sabre/$package/lib/" . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
        }
    }
});
require __DIR__ . '/vendor/sabre/uri/lib/functions.php';
require __DIR__ . '/vendor/sabre/xml/lib/Deserializer/functions.php';
require __DIR__ . '/vendor/sabre/xml/lib/Serializer/functions.php';
