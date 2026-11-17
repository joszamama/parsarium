<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

function parsarium_absolute(string $name): string {
    $name = strtolower($name);
    return str_ends_with($name, '.') ? $name : $name . '.';
}

function parsarium_rdata(\NetDNS2\RR $record): string {
    // NetDNS2 decodes rdata into typed fields, readable through RR::__get.
    switch ($record->type->value) {
        case 1:
            return strval($record->address);
        case 28:
            // RFC 5952 text from NetDNS2's expanded IPv6 address (inet_pton/inet_ntop only reformat it).
            return inet_ntop(inet_pton(strval($record->address)));
        case 5:
            return parsarium_absolute(strval($record->cname));
        case 15:
            return $record->preference . ' ' . parsarium_absolute(strval($record->exchange));
    }
    throw new UnexpectedValueException('record type outside the control subset: ' . $record->type->value);
}

function parsarium_records(array $records): array {
    return array_map(fn (\NetDNS2\RR $record): array => [
        'name' => parsarium_absolute(strval($record->name)), 'type' => $record->type->value,
        'class' => $record->class->value, 'ttl' => $record->ttl, 'rdata' => parsarium_rdata($record),
    ], $records);
}

// NetDNS2\Packet\Response(string, int) decodes the header (including Z, AD and CD) and all sections.
function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > 65535) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $packet = new \NetDNS2\Packet\Response($input, strlen($input));
    $header = $packet->header;
    $questions = array_map(fn (\NetDNS2\Question $question): array => [
        'name' => parsarium_absolute(strval($question->qname)), 'type' => $question->qtype->value,
        'class' => $question->qclass->value,
    ], $packet->question);
    $answers = parsarium_records($packet->answer);
    $authority = parsarium_records($packet->authority);
    $additional = parsarium_records($packet->additional);
    return [
        'id' => $header->id, 'qr' => $header->qr, 'opcode' => $header->opcode->value,
        'aa' => $header->aa, 'tc' => $header->tc, 'rd' => $header->rd, 'ra' => $header->ra,
        'z' => ($header->z << 2) | ($header->ad << 1) | $header->cd, 'rcode' => $header->rcode->value,
        'qdcount' => count($questions), 'ancount' => count($answers),
        'nscount' => count($authority), 'arcount' => count($additional),
        'questions' => $questions, 'answers' => $answers, 'authority' => $authority,
        'additional' => $additional,
    ];
}
