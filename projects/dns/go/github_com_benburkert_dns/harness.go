package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	"time"
	
	"github.com/benburkert/dns"
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

func rdata(record dns.Record) (string, error) {
	switch value := record.(type) {
	case *dns.A:
		return value.A.String(), nil
	case *dns.AAAA:
		return value.AAAA.String(), nil
	case *dns.CNAME:
		return absolute(value.CNAME), nil
	case *dns.NS:
		return absolute(value.NS), nil
	case *dns.PTR:
		return absolute(value.PTR), nil
	case *dns.MX:
		return fmt.Sprintf("%d %s", value.Pref, absolute(value.MX)), nil
	case *dns.TXT:
		quoted := make([]string, len(value.TXT))
		for index, item := range value.TXT {
			quoted[index] = `"` + item + `"`
		}
		return strings.Join(quoted, " "), nil
	}
	return "", fmt.Errorf("record type %d is outside the control subset", record.Type())
}

func records(list []dns.Resource) ([]record, error) {
	out := []record{}
	for _, rr := range list {
		text, err := rdata(rr.Record)
		if err != nil {
			return nil, err
		}
		// The library stores the TTL as a time.Duration of whole seconds.
		out = append(out, record{absolute(rr.Name), uint16(rr.Record.Type()), uint16(rr.Class), uint32(rr.TTL / time.Second), text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes with (*dns.Message).Unpack.
// The library decodes no Z, AD or CD bit, so z is reported as 0.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	message := new(dns.Message)
	if _, err := message.Unpack(data); err != nil {
		return nil, err
	}
	summary := &Summary{
		ID: uint16(message.ID), QR: bit(message.Response), Opcode: int(message.OpCode),
		AA: bit(message.Authoritative), TC: bit(message.Truncated), RD: bit(message.RecursionDesired),
		RA: bit(message.RecursionAvailable), Z: 0, Rcode: int(message.RCode), Questions: []question{},
	}
	for _, item := range message.Questions {
		summary.Questions = append(summary.Questions, question{absolute(item.Name), uint16(item.Type), uint16(item.Class)})
	}
	var err error
	if summary.Answers, err = records(message.Answers); err != nil {
		return nil, err
	}
	if summary.Authority, err = records(message.Authorities); err != nil {
		return nil, err
	}
	if summary.Additional, err = records(message.Additionals); err != nil {
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
