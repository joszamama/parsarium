<?php
declare(strict_types=1);
// Decodes each valid control through the default and the documented internal-decoder route of
// zend-json, plus the verified laminas-json successor, and records which package lines ran.
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
set_error_handler(static function (int $severity, string $message, string $file, int $line): never {
    throw new ErrorException($message, 0, $severity, $file, $line);
});
require __DIR__ . '/vendor/autoload.php';

const ZEND = '/work/vendor/zendframework/zend-json/';
const LAMINAS = '/work/laminas-json/';
spl_autoload_register(static function (string $class): void {
    if (str_starts_with($class, 'Laminas\\Json\\')) {
        require LAMINAS . 'src/' . str_replace('\\', '/', substr($class, strlen('Laminas\\Json\\'))) . '.php';
    }
});
// Load every class before coverage starts so Xdebug reports no file-load pseudo-lines.
foreach (['Zend', 'Laminas'] as $vendor) {
    foreach (['Json', 'Decoder', 'Exception\\ExceptionInterface', 'Exception\\RuntimeException',
              'Exception\\InvalidArgumentException'] as $name) {
        $class = "$vendor\\Json\\$name";
        if (!class_exists($class) && !interface_exists($class)) { throw new LogicException("cannot load $class"); }
    }
}

// Ordered type-tagged tree; integers and floats stay distinct.
function parsarium_tagged(mixed $value): array {
    return match (true) {
        $value === null => ['type' => 'null'],
        is_bool($value) => ['type' => 'boolean', 'value' => $value],
        is_int($value) => ['type' => 'integer', 'value' => (string) $value],
        is_float($value) => ['type' => 'float', 'value' => $value],
        is_string($value) => ['type' => 'string', 'value' => $value],
        is_array($value) && array_is_list($value) => ['type' => 'array', 'items' => array_map('parsarium_tagged', $value)],
        $value instanceof stdClass => ['type' => 'object', 'members' => array_map(
            static fn (string|int $key, mixed $child): array => [(string) $key, parsarium_tagged($child)],
            array_keys(get_object_vars($value)), array_values(get_object_vars($value)))],
        default => throw new UnexpectedValueException('unexpected decoded value: ' . get_debug_type($value)),
    };
}

// Maps executed lines to the declaring method so formatting-only line shifts between the two
// releases do not hide that the same lexer/parser methods ran.
function parsarium_methods(string $class, array $lines): array {
    $reflection = new ReflectionClass($class);
    $methods = [];
    foreach ($reflection->getMethods() as $method) {
        if ($method->getDeclaringClass()->getName() !== $class) { continue; }
        $hit = array_values(array_filter($lines, static fn (int $line): bool =>
            $line >= $method->getStartLine() && $line <= $method->getEndLine()));
        if ($hit !== []) { $methods[$method->getName()] = count($hit); }
    }
    ksort($methods);
    return $methods;
}

$routes = [
    'Zend\\Json\\Json::decode' => [ZEND, 'Zend\\Json', false],
    'Zend\\Json\\Json::decode with $useBuiltinEncoderDecoder = true' => [ZEND, 'Zend\\Json', true],
    'Laminas\\Json\\Json::decode with $useBuiltinEncoderDecoder = true' => [LAMINAS, 'Laminas\\Json', true],
];
$runs = [];
foreach (array_slice($argv, 1) as $path) {
    $text = file_get_contents($path);
    if ($text === false) { throw new RuntimeException("cannot read $path"); }
    foreach ($routes as $route => [$root, $namespace, $builtin]) {
        $json = "$namespace\\Json";
        $json::$useBuiltinEncoderDecoder = $builtin;
        xdebug_start_code_coverage();
        $value = $json::decode($text);
        $raw = xdebug_get_code_coverage();
        xdebug_stop_code_coverage();
        $json::$useBuiltinEncoderDecoder = false;
        $lines = [];
        $methods = [];
        foreach ($raw as $file => $hits) {
            if (!str_starts_with($file, $root)) { continue; }
            $executed = array_keys(array_filter($hits, static fn (int $hit): bool => $hit > 0));
            sort($executed);
            if ($executed === []) { continue; }
            $relative = substr($file, strlen($root));
            $lines[$relative] = $executed;
            $class = $namespace . '\\' . basename($relative, '.php');
            $methods[$relative] = parsarium_methods($class, $executed);
        }
        $runs[] = ['control' => basename($path), 'route' => $route, 'tree' => parsarium_tagged($value),
                   'identical_to_json_decode' => $value == json_decode($text, false, 512, JSON_THROW_ON_ERROR),
                   'package_lines_executed' => $lines, 'package_methods_executed' => $methods];
    }
}
$declared = [];
foreach (['Zend', 'Laminas'] as $vendor) {
    $methods = [];
    foreach ((new ReflectionClass("$vendor\\Json\\Decoder"))->getMethods() as $method) {
        $methods[] = implode(' ', Reflection::getModifierNames($method->getModifiers())) . ' ' . $method->getName();
    }
    sort($methods);
    $declared["$vendor\\Json\\Decoder"] = $methods;
}
echo json_encode(['php' => PHP_VERSION, 'xdebug' => phpversion('xdebug'),
                  'toolchain' => file(__DIR__ . '/toolchain.txt', FILE_IGNORE_NEW_LINES),
                  'decoder_methods' => $declared, 'runs' => $runs], JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION), "\n";
