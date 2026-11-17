<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use LibDNS\Decoder\DecoderFactory;
use LibDNS\Records\Resource;
use LibDNS\Records\ResourceTypes;

function parsarium_absolute(string $name): string {
    $name = strtolower($name);
    return str_ends_with($name, '.') ? $name : $name . '.';
}

function parsarium_rdata(Resource $record): string {
    $data = $record->getData();
    switch ($record->getType()) {
        case ResourceTypes::A:
        case ResourceTypes::AAAA:
            // LibDNS's own address text (IPv6Address compresses the longest zero run).
            return (string) $data->getField(0);
        case ResourceTypes::CNAME:
        case ResourceTypes::NS:
        case ResourceTypes::PTR:
            return parsarium_absolute((string) $data->getField(0));
        case ResourceTypes::MX:
            return $data->getFieldByName('preference')->getValue() . ' '
                . parsarium_absolute((string) $data->getFieldByName('exchange'));
        case ResourceTypes::TXT:
            $items = [];
            foreach ($data as $field) { $items[] = '"' . $field . '"'; }
            return implode(' ', $items);
    }
    throw new UnexpectedValueException('record type outside the control subset: ' . $record->getType());
}

function parsarium_records(iterable $records): array {
    $out = [];
    foreach ($records as $record) {
        $out[] = ['name' => parsarium_absolute((string) $record->getName()), 'type' => $record->getType(),
                  'class' => $record->getClass(), 'ttl' => $record->getTTL(), 'rdata' => parsarium_rdata($record)];
    }
    return $out;
}

// LibDNS\Messages\Message keeps id, type (QR), opcode, aa, tc, rd, ra and rcode; the decoder drops
// the three bits after RA (Z, AD, CD), so z is reported as 0. Both controls have them clear.
function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > 65535) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    // create(null, false): default type definitions, trailing data after the message rejected.
    $message = (new DecoderFactory())->create(null, false)->decode($input);
    $questions = [];
    foreach ($message->getQuestionRecords() as $question) {
        $questions[] = ['name' => parsarium_absolute((string) $question->getName()),
                        'type' => $question->getType(), 'class' => $question->getClass()];
    }
    $answers = parsarium_records($message->getAnswerRecords());
    $authority = parsarium_records($message->getAuthorityRecords());
    $additional = parsarium_records($message->getAdditionalRecords());
    return [
        'id' => $message->getID(), 'qr' => $message->getType(), 'opcode' => $message->getOpCode(),
        'aa' => (int) $message->isAuthoritative(), 'tc' => (int) $message->isTruncated(),
        'rd' => (int) $message->isRecursionDesired(), 'ra' => (int) $message->isRecursionAvailable(),
        'z' => 0, 'rcode' => $message->getResponseCode(),
        'qdcount' => count($questions), 'ancount' => count($answers),
        'nscount' => count($authority), 'arcount' => count($additional),
        'questions' => $questions, 'answers' => $answers, 'authority' => $authority,
        'additional' => $additional,
    ];
}
