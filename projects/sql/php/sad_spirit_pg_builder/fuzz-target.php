<?php
declare(strict_types=1);
/** @var PhpFuzzer\Config $config */
require __DIR__ . '/harness.php';
$config->setTarget(static function (string $input): void {
    try { parsarium_parse($input); }
    catch (\sad_spirit\pg_builder\Exception | \InvalidArgumentException | \UnexpectedValueException | \TypeError $rejected) {}
});
$config->setMaxLen(1 << 20);
