package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	"net/netip"
	
	"github.com/phuslu/fastdns"
)

type question struct {
	Name  string `json:"name"`
	Type  uint16 `json:"type"`
	Class uint16 `json:"class"`
}

type record struct {
	Name  string `json:"name"`
	Type  uint16 `json:"type"`
	Class uint16 `json:"class"`
	TTL   uint32 `json:"ttl"`
	Rdata string `json:"rdata"`
}

// Summary has the field order of controls/dns/expected.json.
type Summary struct {
	ID         uint16     `json:"id"`
	QR         int        `json:"qr"`
	Opcode     int        `json:"opcode"`
	AA         int        `json:"aa"`
	TC         int        `json:"tc"`
	RD         int        `json:"rd"`
	RA         int        `json:"ra"`
	Z          int        `json:"z"`
	Rcode      int        `json:"rcode"`
	QDCount    int        `json:"qdcount"`
	ANCount    int        `json:"ancount"`
	NSCount    int        `json:"nscount"`
	ARCount    int        `json:"arcount"`
	Questions  []question `json:"questions"`
	Answers    []record   `json:"answers"`
	Authority  []record   `json:"authority"`
	Additional []record   `json:"additional"`
}

func bit(value bool) int {
	if value {
		return 1
	}
	return 0
}

func absolute(name string) string {
	name = strings.ToLower(name)
	if !strings.HasSuffix(name, ".") {
		name += "."
	}
	return name
}

// name decodes a possibly compressed wire name through the library's DecodeName.
func name(message *fastdns.Message, wire []byte) (string, error) {
	decoded, err := message.DecodeName(nil, wire)
	if err != nil {
		return "", err
	}
	return absolute(string(decoded)), nil
}

// rdata formats one record's RDATA. fastdns hands out each record's RDATA as a byte
// slice and decodes names with DecodeName; the harness reads the A/AAAA address bytes
// (printed with net/netip) and the 16-bit MX preference from that slice.
func rdata(message *fastdns.Message, item fastdns.MessageRecord) (string, error) {
	data := item.Data
	switch item.Type {
	case fastdns.TypeA:
		if len(data) != 4 {
			return "", fmt.Errorf("bad A length")
		}
		return netip.AddrFrom4([4]byte(data)).String(), nil
	case fastdns.TypeAAAA:
		if len(data) != 16 {
			return "", fmt.Errorf("bad AAAA length")
		}
		return netip.AddrFrom16([16]byte(data)).String(), nil
	case fastdns.TypeCNAME, fastdns.TypeNS, fastdns.TypePTR:
		return name(message, data)
	case fastdns.TypeMX:
		if len(data) < 3 {
			return "", fmt.Errorf("bad MX length")
		}
		exchange, err := name(message, data[2:])
		if err != nil {
			return "", err
		}
		return fmt.Sprintf("%d %s", uint16(data[0])<<8|uint16(data[1]), exchange), nil
	}
	return "", fmt.Errorf("record type %d is outside the control subset", item.Type)
}

// Parse decodes one DNS message from local bytes with fastdns.ParseMessage and walks
// its records with (*Message).Records. The record iterator runs over all three record
// sections in wire order; the harness splits them by the parsed header counts.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	message := new(fastdns.Message)
	if err := fastdns.ParseMessage(message, data, true); err != nil {
		return nil, err
	}
	header := message.Header
	flags := header.Flags
	summary := &Summary{
		ID: header.ID, QR: int(flags.QR()), Opcode: int(flags.Opcode()),
		AA: int(flags.AA()), TC: int(flags.TC()), RD: int(flags.RD()), RA: int(flags.RA()),
		Z: int(flags.Z()), Rcode: int(flags.Rcode()),
		Questions: []question{{absolute(string(message.Domain)), uint16(message.Question.Type), uint16(message.Question.Class)}},
		Answers: []record{}, Authority: []record{}, Additional: []record{},
	}
	records := message.Records()
	index := 0
	for records.Next() {
		item := records.Item()
		owner, err := name(message, item.Name)
		if err != nil {
			return nil, err
		}
		text, err := rdata(message, item)
		if err != nil {
			return nil, err
		}
		entry := record{owner, uint16(item.Type), uint16(item.Class), item.TTL, text}
		switch {
		case index < int(header.ANCount):
			summary.Answers = append(summary.Answers, entry)
		case index < int(header.ANCount)+int(header.NSCount):
			summary.Authority = append(summary.Authority, entry)
		default:
			summary.Additional = append(summary.Additional, entry)
		}
		index++
	}
	if err := records.Err(); err != nil {
		return nil, err
	}
	summary.QDCount, summary.ANCount = len(summary.Questions), len(summary.Answers)
	summary.NSCount, summary.ARCount = len(summary.Authority), len(summary.Additional)
	return summary, nil
}

// Encode prints the summary as compact JSON in field order.
func Encode(summary *Summary) string {
	encoded, _ := json.Marshal(summary)
	return string(encoded)
}
