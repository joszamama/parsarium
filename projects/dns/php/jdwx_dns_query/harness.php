<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use JDWX\DNSQuery\Lookups;
use JDWX\DNSQuery\Packet\ResponsePacket;
use JDWX\DNSQuery\RR\RR;

function parsarium_absolute(string $name): string {
    $name = strtolower($name);
    return str_ends_with($name, '.') ? $name : $name . '.';
}

function parsarium_rdata(RR $record): string {
    switch ($record->type) {
        case 'A':
            return $record->address;  // inet_ntop text from A::rrSet
        case 'AAAA':
            // AAAA::rrSet formats the 16 decoded bytes as eight uncompressed hex groups;
            // the harness only compresses that text to RFC 5952 form.
            return inet_ntop(inet_pton($record->address));
        case 'CNAME':
            return parsarium_absolute($record->cname);
        case 'NS':
            return parsarium_absolute($record->nsdName);
        case 'PTR':
            return parsarium_absolute($record->ptrDName);
        case 'MX':
            return $record->preference . ' ' . parsarium_absolute($record->exchange);
    }
    throw new UnexpectedValueException('record type outside the control subset: ' . $record->type);
}

// The decoder stores type and class mnemonics; Lookups holds the library's own number tables.
function parsarium_records(array $records): array {
    return array_map(fn (RR $record): array => [
        'name' => parsarium_absolute($record->name), 'type' => Lookups::$rrTypesByName[$record->type],
        'class' => Lookups::$classesByName[$record->class], 'ttl' => $record->ttl,
        'rdata' => parsarium_rdata($record),
    ], $records);
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > 65535) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $packet = new ResponsePacket($input, strlen($input));
    $header = $packet->header;
    $questions = array_map(fn ($question): array => [
        'name' => parsarium_absolute($question->qName), 'type' => Lookups::$rrTypesByName[$question->qType],
        'class' => Lookups::$classesByName[$question->qClass],
    ], $packet->question);
    // Header keeps the reserved Z bit ($zero), AD and CD separately.
    return [
        'id' => $header->id, 'qr' => $header->qr, 'opcode' => $header->opcode, 'aa' => $header->aa,
        'tc' => $header->tc, 'rd' => $header->rd, 'ra' => $header->ra,
        'z' => ($header->zero << 2) | ($header->ad << 1) | $header->cd, 'rcode' => $header->rCode,
        'qdcount' => $header->qdCount, 'ancount' => $header->anCount,
        'nscount' => $header->nsCount, 'arcount' => $header->arCount,
        'questions' => $questions, 'answers' => parsarium_records($packet->answer),
        'authority' => parsarium_records($packet->authority),
        'additional' => parsarium_records($packet->additional),
    ];
}
