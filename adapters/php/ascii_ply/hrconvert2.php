<?php
declare(strict_types=1);

if ($argc !== 4) exit(2);
[$script, $pipeline, $input, $output] = $argv;

// The released conversion function calls these host-application services.
// Keep its parsing and conversion code intact; only supply standalone hosts.
$CoreLoaded = true;
$Verbose = false;
$Lol = "\n";
$Lolol = "\n\n";
$StopCounter = 2;
$SleepTimer = 0;
$UsePyMeshLab = true;
$InstLoc = dirname($pipeline, 4);
$DirSep = DIRECTORY_SEPARATOR;
$EnableMemoryProtection = false;
$observedCommands = [];
$observedErrors = [];
$stageMarkers = [];

function verifiedToolPath(string $name): string|false {
    if ($name === 'Assimp') return getenv('PARSARIUM_ASSIMP') ?: false;
    return false;
}
function locateDependency(string $name): string {
    if ($name === 'python3.14') return '';
    if ($name === 'python3') return getenv('PARSARIUM_PYTHON') ?: '';
    return '';
}
function sandboxCommand(string $command, ...$arguments): array {
    global $observedCommands, $stageMarkers;
    $observedCommands[] = $command;
    $stageOutput = $arguments[1];
    $marker = $stageOutput . '.parsarium-stage-ok';
    $stageMarkers[] = $marker;
    // Observe whether the real command created its output; this host stub
    // supplies no sandbox policy and never substitutes parser output.
    $observedCommand = '(' . $command . ') && test -s ' . escapeshellarg($stageOutput)
        . ' && touch ' . escapeshellarg($marker);
    return [true, $observedCommand];
}
function warningEntry(string $message): void { fwrite(STDERR, "warning: $message\n"); }
function errorEntry(string $message, ...$arguments): void {
    global $observedErrors;
    $observedErrors[] = $message;
}
function logEntry(string $message): void { fwrite(STDERR, "log: $message\n"); }
function purgeSensitiveMemory(...$arguments): void {}

require $pipeline;
$result = convertModels($input, $output, 'obj');
if ($result[0] !== true || $result[1] !== false || !is_file($output)) {
    fwrite(STDERR, json_encode(['result' => $result, 'errors' => $observedErrors]) . "\n");
    exit(3);
}
if (count($stageMarkers) !== 2 || !is_file($stageMarkers[0]) || !is_file($stageMarkers[1])) {
    fwrite(STDERR, "Both real conversion stages must produce output.\n");
    exit(5);
}
$obj = file_get_contents($output);
if ($obj === false) exit(4);
preg_match_all('/^v\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)/m', $obj, $vertexRows, PREG_SET_ORDER);
preg_match_all('/^f\s+([^\r\n]+)/m', $obj, $faceRows, PREG_SET_ORDER);
$xSum = 0.0;
foreach ($vertexRows as $vertex) $xSum += (float)$vertex[1];

echo json_encode([
    'vertices' => count($vertexRows),
    'faces' => count($faceRows),
    'x_sum' => $xSum,
    'completed_stages' => count($stageMarkers),
], JSON_THROW_ON_ERROR), "\n";
