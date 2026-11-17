#!/opt/php/bin/php
<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

// Parse-time target: the documented sql_parse() (pg_query_parse_protobuf plus the google/protobuf decode into the
// package AST classes). The Traverser summary walk and the JSON output of harness.php are skipped. Executable
// through its #! line so that afl-showmap can start it as a single program with the input path as the argument.
$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
try {
    parsarium_sql_parse($bytes);
} catch (Flow\PostgreSql\Exception\ParserException) {
    // Parser::parse() reports rejected SQL as a ParserException.
}
