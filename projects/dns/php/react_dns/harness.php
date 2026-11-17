<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use React\Dns\Model\Message;
use React\Dns\Model\Record;
use React\Dns\Protocol\Parser;

function parsarium_absolute(string $name): string {
    $name = strtolower($name);
    return str_ends_with($name, '.') ? $name : $name . '.';
}

function parsarium_rdata(Record $record): string {
    switch ($record->type) {
        case Message::TYPE_A:
        case Message::TYPE_AAAA:
            return (string) $record->data;  // inet_ntop text from the parser
        case Message::TYPE_CNAME:
        case Message::TYPE_NS:
        case Message::TYPE_PTR:
            return parsarium_absolute((string) $record->data);
        case Message::TYPE_MX:
            return $record->data['priority'] . ' ' . parsarium_absolute($record->data['target']);
        case Message::TYPE_TXT:
            return implode(' ', array_map(fn (string $item): string => '"' . $item . '"', $record->data));
    }
    throw new UnexpectedValueException('record type outside the control subset: ' . $record->type);
}

function parsarium_records(array $records): array {
    return array_map(fn (Record $record): array => [
        'name' => parsarium_absolute($record->name), 'type' => $record->type, 'class' => $record->class,
        'ttl' => $record->ttl, 'rdata' => parsarium_rdata($record),
    ], $records);
}

// React\Dns\Protocol\Parser::parseMessage keeps id, qr, opcode, aa, tc, rd, ra and rcode;
// it drops the three bits after RA (Z, AD, CD), so z is reported as 0.
function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > 65535) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $message = (new Parser())->parseMessage($input);
    $questions = array_map(fn ($query): array => [
        'name' => parsarium_absolute($query->name), 'type' => $query->type, 'class' => $query->class,
    ], $message->questions);
    $answers = parsarium_records($message->answers);
    $authority = parsarium_records($message->authority);
    $additional = parsarium_records($message->additional);
    return [
        'id' => $message->id, 'qr' => (int) $message->qr, 'opcode' => $message->opcode,
        'aa' => (int) $message->aa, 'tc' => (int) $message->tc, 'rd' => (int) $message->rd,
        'ra' => (int) $message->ra, 'z' => 0, 'rcode' => $message->rcode,
        'qdcount' => count($questions), 'ancount' => count($answers),
        'nscount' => count($authority), 'arcount' => count($additional),
        'questions' => $questions, 'answers' => $answers, 'authority' => $authority,
        'additional' => $additional,
    ];
}
