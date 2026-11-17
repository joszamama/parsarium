<?php
declare(strict_types=1);
// Bare ext/xml baseline for the pear/xml_parser overlay: the same handler object as the package harness, bound
// directly with method callables to a parser from xml_parser_create() with case folding off, and the whole input
// in one final xml_parse call. No XML_Parser or PEAR code runs. build.py compares its AFL++ maps with the package
// harness to separate what libxml2/ext/xml do for any caller from what the package path adds.
require __DIR__ . '/summary.php';

$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$bytes = file_get_contents($path);
if ($bytes === false || $bytes === '') { exit(0); }
$handler = new ParsariumXmlParserHandler();
$parser = xml_parser_create();
xml_parser_set_option($parser, XML_OPTION_CASE_FOLDING, false);
xml_set_element_handler($parser, [$handler, 'startHandler'], [$handler, 'endHandler']);
xml_set_character_data_handler($parser, [$handler, 'cdataHandler']);
xml_set_processing_instruction_handler($parser, [$handler, 'piHandler']);
$ok = xml_parse($parser, $bytes, true);
// XML_Parser::parse() ends with free() -> xml_parser_free(); the baseline makes the same (PHP 8.5 deprecated, no-op)
// call so that the edge from the last parse-time block into xml.c is formed the same way on both paths.
@xml_parser_free($parser);
if ($ok !== 1) { exit(0); }
if (in_array('--print', $argv, true)) {
    echo json_encode($handler->summary(), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
}
