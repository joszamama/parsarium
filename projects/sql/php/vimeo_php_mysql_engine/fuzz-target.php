<?php
declare(strict_types=1);
/** @var PhpFuzzer\Config $config */
require __DIR__ . '/harness.php';
$config->setTarget(static function (string $input): void {
    try { parsarium_parse($input); }
    catch (\Exception | \TypeError $rejected) {}
});
$config->setMaxLen(1 << 20);
