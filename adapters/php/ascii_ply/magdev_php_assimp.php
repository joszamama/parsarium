<?php
/* Verify the published 0.3.2 InfoVerb on a supplied local ASCII PLY file. */
error_reporting(E_ALL & ~E_DEPRECATED & ~E_USER_DEPRECATED);

if ($argc !== 2 || !is_file($argv[1])) {
    exit(2);
}
require __DIR__ . '/vendor/autoload.php';

$binary = getenv('PARSARIUM_ASSIMP_BIN') ?: '/opt/homebrew/Cellar/assimp/6.0.6/bin/assimp';
$verb = new Assimp\Command\Verbs\InfoVerb($argv[1]);
$result = (new Assimp\Command\Command($binary))->execute($verb, true);
if (!$result->isSuccess() || strpos($result->getCommand(), $argv[1]) === false) {
    fwrite(STDERR, "Assimp import did not succeed on the supplied path\n");
    exit(1);
}

$output = implode("\n", $result->getOutput());
$values = [];
foreach (['Meshes' => 'meshes', 'Vertices' => 'vertices', 'Faces' => 'faces'] as $label => $key) {
    if (!preg_match('/^\s*' . $label . ':\s*(\d+)\s*$/m', $output, $match)) {
        fwrite(STDERR, "Missing parsed $label field\n");
        exit(1);
    }
    $values[$key] = (int) $match[1];
}
echo json_encode($values, JSON_THROW_ON_ERROR), "\n";
