<?php
declare(strict_types=1);
// Composer-equivalent autoload built from the pinned composer.lock: each package's psr-4 map and "files" entries.
(static function (): void {
    $lock = json_decode(file_get_contents(__DIR__ . '/composer.lock'), true, 512, JSON_THROW_ON_ERROR);
    $prefixes = []; $files = [];
    foreach ($lock['packages'] as $package) {
        $base = __DIR__ . '/vendor/' . $package['name'] . '/';
        foreach ($package['autoload']['psr-4'] ?? [] as $prefix => $path) { $prefixes[$prefix][] = $base . rtrim($path, '/') . '/'; }
        foreach ($package['autoload']['files'] ?? [] as $path) { $files[] = $base . $path; }
    }
    uksort($prefixes, fn (string $a, string $b): int => strlen($b) <=> strlen($a));
    spl_autoload_register(function (string $class) use ($prefixes): void {
        foreach ($prefixes as $prefix => $directories) {
            if (!str_starts_with($class, $prefix)) { continue; }
            foreach ($directories as $directory) {
                $file = $directory . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
                if (is_file($file)) { require $file; return; }
            }
        }
    });
    foreach ($files as $file) { require_once $file; }
})();
