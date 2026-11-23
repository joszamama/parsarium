<?php
declare(strict_types=1);
$CoreLoaded = true;
$Verbose = false;
$Lol = "\n";
$Lolol = "\n\n";
$StopCounter = 2;
$SleepTimer = 0;
$UsePyMeshLab = true;
$InstLoc = '/work/parser';
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


require_once __DIR__ . '/parser/Resources/Pipelines/Model/pipeline.php';
function parsarium_parse_ply(string $input): array|false {
    global $stageMarkers, $observedCommands, $observedErrors;
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $stageMarkers = []; $observedCommands = []; $observedErrors = [];
    $seed = tempnam('/tmp', 'parsarium-ply-');
    if ($seed === false) throw new RuntimeException('No temp path');
    $inputPath = $seed . '.ply';
    $outputPath = $seed . '.obj';
    rename($seed, $inputPath);
    try {
        if (file_put_contents($inputPath, $input) !== strlen($input)) throw new RuntimeException('Could not write input');
        $result = convertModels($inputPath, $outputPath, 'obj');
        // The pipeline's own verdict: element 0 is success, element 1 the error flag,
        // with the reasons passed to errorEntry().
        if ($result[0] !== true || $result[1] !== false) {
            throw new RuntimeException('convertModels failed: ' . (implode('; ', $observedErrors) ?: 'no error entry'));
        }
        if (!is_file($outputPath)) throw new RuntimeException('convertModels reported success without writing ' . basename($outputPath));
        $obj = file_get_contents($outputPath);
        if ($obj === false) throw new RuntimeException('Could not read converted OBJ');
        // A stage (e.g. the PyMeshLab rectification) may fail while the pipeline still
        // succeeds through the next one: completed_stages counts the stages whose
        // command created its output.
        $completed = count(array_filter($stageMarkers, 'is_file'));
        preg_match_all('/^v\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)/m', $obj, $vertexRows, PREG_SET_ORDER);
        preg_match_all('/^f\s+([^\r\n]+)/m', $obj, $faceRows, PREG_SET_ORDER);
        $xSum = 0.0;
        foreach ($vertexRows as $vertex) $xSum += (float)$vertex[1];
        return ['vertices' => count($vertexRows), 'faces' => count($faceRows),
                'x_sum' => $xSum, 'completed_stages' => $completed];
    } finally {
        foreach ($stageMarkers as $marker) if (is_file($marker)) unlink($marker);
        if (is_file($inputPath)) unlink($inputPath);
        if (is_file($outputPath)) unlink($outputPath);
        foreach (glob($seed . '*') ?: [] as $extra) if (is_file($extra)) unlink($extra);
    }
}
