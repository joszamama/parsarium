<?php
declare(strict_types=1);
/** @var PhpFuzzer\Config $config */
require __DIR__ . '/harness.php';
$config->setTarget(static function (string $input): void {
    try { parsarium_parse($input); }
    catch (\InvalidArgumentException | \UnexpectedValueException | \NetDNS2\Exception | \ValueError | \TypeError $rejected) {}
});
$config->setMaxLen(65535);
