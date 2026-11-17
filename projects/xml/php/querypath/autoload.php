<?php
declare(strict_types=1);
// Composer-equivalent autoload for the pinned querypath/querypath 3.0.5.
spl_autoload_register(function (string $class): void {
    // psr-0 'QueryPath' => src/
    if ($class === 'QueryPath' || str_starts_with($class, 'QueryPath\\')) {
        $file = __DIR__ . '/vendor/querypath/querypath/src/' . str_replace('\\', '/', $class) . '.php';
        if (is_file($file)) { require $file; }
    }
});
require __DIR__ . '/vendor/querypath/querypath/src/qp_functions.php';
