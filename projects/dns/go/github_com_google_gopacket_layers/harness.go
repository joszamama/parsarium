package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
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

func absolute(name []byte) string {
	text := strings.ToLower(string(name))
	if !strings.HasSuffix(text, ".") {
		text += "."
	}
	return text
}

func rdata(rr layers.DNSResourceRecord) (string, error) {
	switch rr.Type {
	case layers.DNSTypeA, layers.DNSTypeAAAA:
		return rr.IP.String(), nil
	case layers.DNSTypeCNAME:
		return absolute(rr.CNAME), nil
	case layers.DNSTypeNS:
		return absolute(rr.NS), nil
	case layers.DNSTypePTR:
		return absolute(rr.PTR), nil
	case layers.DNSTypeMX:
		return fmt.Sprintf("%d %s", rr.MX.Preference, absolute(rr.MX.Name)), nil
	case layers.DNSTypeTXT:
		quoted := make([]string, len(rr.TXTs))
		for index, item := range rr.TXTs {
			quoted[index] = `"` + string(item) + `"`
		}
		return strings.Join(quoted, " "), nil
	}
	return "", fmt.Errorf("record type %d is outside the control subset", rr.Type)
}

func records(list []layers.DNSResourceRecord) ([]record, error) {
	out := []record{}
	for _, rr := range list {
		text, err := rdata(rr)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(rr.Name), uint16(rr.Type), uint16(rr.Class), rr.TTL, text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes with (*layers.DNS).DecodeFromBytes.
// gopacket keeps the 3-bit Z field (Z, AD, CD) as layers.DNS.Z.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	message := &layers.DNS{}
	if err := message.DecodeFromBytes(data, gopacket.NilDecodeFeedback); err != nil {
		return nil, err
	}
	summary := &Summary{
		ID: message.ID, QR: bit(message.QR), Opcode: int(message.OpCode),
		AA: bit(message.AA), TC: bit(message.TC), RD: bit(message.RD), RA: bit(message.RA),
		Z: int(message.Z), Rcode: int(message.ResponseCode), Questions: []question{},
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
