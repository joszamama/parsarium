<?php
declare(strict_types=1);

// Summary of the SAX events XML_Parser 1.3.8 delivers to a handler object, comparable with oracle.py.
// XML_Parser::_create() calls xml_parser_create() without a namespace separator (the package has no namespace
// mode), so ext/xml reports raw qualified names (prefix:local) and passes xmlns/xmlns:* declarations as ordinary
// attributes. XML_Parser enables case folding by default ($folding = true, which upper-cases every element and
// attribute name); the documented public $folding property is set to false so names keep their case.
// - Elements and attributes are listed in document order; attributes as name=value, declarations included.
// - Character data and CDATA both arrive through cdataHandler; runs are flushed at element starts and ends and at
//   processing instructions, then trimmed of XML whitespace, and empty runs are dropped.
// - Processing instructions arrive through piHandler as "target data".
// - XML_Parser installs no comment handler and this handler object defines no defaultHandler, so comments and the
//   XML declaration are not reported.
final class ParsariumXmlParserHandler
{
    public array $elements = [];
    public array $attributes = [];
    public array $instructions = [];
    public array $segments = [];
    public string $text = '';
    public int $depth = 0;
    public int $maxDepth = 0;

    private function flush(): void
    {
        $segment = trim($this->text, " \t\n\r");
        if ($segment !== '') { $this->segments[] = $segment; }
        $this->text = '';
    }

    public function startHandler($parser, string $name, array $attributes): void
    {
        $this->flush();
        $this->elements[] = $name;
        $this->depth++;
        $this->maxDepth = max($this->maxDepth, $this->depth);
        foreach ($attributes as $key => $value) { $this->attributes[] = "$key=$value"; }
    }

    public function endHandler($parser, string $name): void
    {
        $this->flush();
        $this->depth--;
    }

    public function cdataHandler($parser, string $data): void
    {
        $this->text .= $data;
    }

    public function piHandler($parser, string $target, string $data): void
    {
        $this->flush();
        $this->instructions[] = "$target $data";
    }

    public function summary(): array
    {
        return ['attributes' => $this->attributes, 'elements' => $this->elements, 'max_depth' => $this->maxDepth,
                'processing_instructions' => $this->instructions, 'root' => $this->elements[0] ?? null,
                'text' => $this->segments];
    }
}

// Runs XML_Parser in its default "event" mode with a separate handler object (setHandlerObj), the documented
// alternative to subclassing. $input selects the documented input call: setInputString(string),
// setInputFile(path) or setInput(resource); parse() then drives xml_parse over the whole string or 4096-byte
// fread chunks of the file or stream.
function parsarium_xml_parser_summary(string $kind, $input): array
{
    $parser = new XML_Parser();
    $parser->folding = false;
    $handler = new ParsariumXmlParserHandler();
    $parser->setHandlerObj($handler);
    $set = match ($kind) {
        'string' => $parser->setInputString($input),
        'file' => $parser->setInputFile($input),
        'stream' => $parser->setInput($input),
    };
    if (PEAR::isError($set)) { throw new RuntimeException('XML_Parser input: ' . $set->getMessage()); }
    $result = $parser->parse();
    if (PEAR::isError($result)) { throw new RuntimeException('XML_Parser: ' . $result->getMessage()); }
    return $handler->summary();
}
