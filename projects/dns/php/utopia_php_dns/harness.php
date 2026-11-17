<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Utopia\DNS\Message;
use Utopia\DNS\Message\Record;

function parsarium_absolute(string $name): string {
    $name = strtolower($name);
    return str_ends_with($name, '.') ? $name : $name . '.';
}

function parsarium_rdata(Record $record): string {
    switch ($record->type) {
        case Record::TYPE_A:
        case Record::TYPE_AAAA:
            return $record->rdata;  // inet_ntop text from Record::decode
        case Record::TYPE_CNAME:
        case Record::TYPE_NS:
        case Record::TYPE_PTR:
            return parsarium_absolute($record->rdata);
        case Record::TYPE_MX:
            // Record::decode keeps the MX preference in $priority and the exchange in $rdata.
            return $record->priority . ' ' . parsarium_absolute($record->rdata);
    }
    throw new UnexpectedValueException('record type outside the control subset: ' . $record->type);
}

function parsarium_records(array $records): array {
    return array_map(fn (Record $record): array => [
        'name' => parsarium_absolute($record->name), 'type' => $record->type, 'class' => $record->class,
        'ttl' => $record->ttl, 'rdata' => parsarium_rdata($record),
    ], $records);
}

// Utopia\DNS\Message\Header::decode keeps id, QR, opcode, aa, tc, rd, ra and rcode and
// intentionally ignores the three bits after RA (Z, AD, CD), so z is reported as 0.
function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > 65535) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $message = Message::decode($input);
    $header = $message->header;
    $questions = array_map(fn ($question): array => [
        'name' => parsarium_absolute($question->name), 'type' => $question->type, 'class' => $question->class,
    ], $message->questions);
    return [
        'id' => $header->id, 'qr' => (int) $header->isResponse, 'opcode' => $header->opcode,
        'aa' => (int) $header->authoritative, 'tc' => (int) $header->truncated,
        'rd' => (int) $header->recursionDesired, 'ra' => (int) $header->recursionAvailable,
        'z' => 0, 'rcode' => $header->responseCode,
        'qdcount' => $header->questionCount, 'ancount' => $header->answerCount,
        'nscount' => $header->authorityCount, 'arcount' => $header->additionalCount,
        'questions' => $questions, 'answers' => parsarium_records($message->answers),
        'authority' => parsarium_records($message->authority),
        'additional' => parsarium_records($message->additional),
    ];
}
