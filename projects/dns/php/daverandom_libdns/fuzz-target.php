<?php
declare(strict_types=1);
/** @var PhpFuzzer\Config $config */
require __DIR__ . '/harness.php';
// php-fuzzer v0.0.11 instruments every file:// include through nikic/include-interceptor,
// which replaces the file:// stream wrapper with Nikic\IncludeInterceptor\Stream. Its rewrite of
// LibDNS's Records/Types/DomainName.php turns the class constant
// FLAG_NO_COMPRESSION = \PHP_INT_SIZE === 4 ? ... : ... into a non-constant expression
// ("Constant expression contains invalid operations"). That one class file is therefore
// compiled unmodified: the native file:// wrapper is restored for this single require and the
// interceptor's wrapper is registered again right after (the same steps as
// Interceptor::unwrap()/wrap()). Every other LibDNS file stays instrumented, and parsing is
// unchanged: the same source file defines the same class. Xdebug coverage (run-control.php and
// the AFL++ bridge) loads it through the normal autoloader and counts its lines.
// The parent class is autoloaded (and instrumented) first, so only DomainName.php is exempt.
class_exists(\LibDNS\Records\Types\Type::class);
stream_wrapper_restore('file');
try {
    require_once __DIR__ . '/vendor/daverandom/libdns/src/Records/Types/DomainName.php';
} finally {
    stream_wrapper_unregister('file');
    stream_wrapper_register('file', \Nikic\IncludeInterceptor\Stream::class);
}
$config->setTarget(static function (string $input): void {
    try { parsarium_parse($input); }
    catch (\InvalidArgumentException | \UnexpectedValueException $rejected) {}
});
$config->setMaxLen(65535);
