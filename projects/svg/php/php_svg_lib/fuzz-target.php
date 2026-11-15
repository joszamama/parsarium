<?php
declare(strict_types=1);

/** @var PhpFuzzer\Config $config */
require __DIR__ . '/harness.php';

$config->setTarget(static function (string $input): void {
    parsarium_parse_svg($input);
});
$config->setMaxLen(1 << 20);
