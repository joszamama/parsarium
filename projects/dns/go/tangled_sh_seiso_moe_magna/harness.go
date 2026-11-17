package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	"net/netip"
	
	"tangled.sh/seiso.moe/magna"
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

// rdata formats the decoded RDATA. magna 0.0.2 has no AAAA type: RDATA of type 28 is
// kept as magna.Reserved raw bytes, which the harness prints with net/netip (disclosed).
func rdata(item magna.ResourceRecord) (string, error) {
	switch value := item.RData.(type) {
	case *magna.A:
		return value.Address.String(), nil
	case *magna.CNAME:
		return absolute(value.CName), nil
	case *magna.NS:
		return absolute(value.NSDName), nil
	case *magna.PTR:
		return absolute(value.PTRDName), nil
	case *magna.MX:
		return fmt.Sprintf("%d %s", value.Preference, absolute(value.Exchange)), nil
	case *magna.Reserved:
		if item.RType == 28 && len(value.Bytes) == 16 {
			return netip.AddrFrom16([16]byte(value.Bytes)).String(), nil
		}
	}
	return "", fmt.Errorf("record type %d is outside the control subset", item.RType)
}

func records(list []magna.ResourceRecord) ([]record, error) {
	out := []record{}
	for _, item := range list {
		text, err := rdata(item)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(item.Name), uint16(item.RType), uint16(item.RClass), item.TTL, text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes with (*magna.Message).Decode.
// The header keeps the 3-bit Z field (Z, AD, CD).
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	message := new(magna.Message)
	if err := message.Decode(data); err != nil {
		return nil, err
	}
	header := message.Header
	summary := &Summary{
		ID: header.ID, QR: bit(header.QR), Opcode: int(header.OPCode),
		AA: bit(header.AA), TC: bit(header.TC), RD: bit(header.RD), RA: bit(header.RA),
		Z: int(header.Z), Rcode: int(header.RCode), Questions: []question{},
	}
	for _, item := range message.Question {
		summary.Questions = append(summary.Questions, question{absolute(item.QName), uint16(item.QType), uint16(item.QClass)})
	}
	var err error
	if summary.Answers, err = records(message.Answer); err != nil {
		return nil, err
	}
	if summary.Authority, err = records(message.Authority); err != nil {
		return nil, err
	}
	if summary.Additional, err = records(message.Additional); err != nil {
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
