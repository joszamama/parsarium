package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	
	"codeberg.org/miekg/dns"
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

func rdata(rr dns.RR) (string, error) {
	switch value := rr.(type) {
	case *dns.A:
		return value.Addr.String(), nil
	case *dns.AAAA:
		return value.Addr.String(), nil
	case *dns.CNAME:
		return absolute(value.Target), nil
	case *dns.NS:
		return absolute(value.Ns), nil
	case *dns.PTR:
		return absolute(value.Ptr), nil
	case *dns.MX:
		return fmt.Sprintf("%d %s", value.Preference, absolute(value.Mx)), nil
	case *dns.TXT:
		quoted := make([]string, len(value.Txt))
		for index, item := range value.Txt {
			quoted[index] = `"` + item + `"`
		}
		return strings.Join(quoted, " "), nil
	}
	return "", fmt.Errorf("record type %d is outside the control subset", dns.RRToType(rr))
}

func records(list []dns.RR) ([]record, error) {
	out := []record{}
	for _, rr := range list {
		header := rr.Header()
		text, err := rdata(rr)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(header.Name), dns.RRToType(rr), header.Class, header.TTL, text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes: the bytes go in Msg.Data and
// (*dns.Msg).Unpack decodes them. miekg/dns v2 keeps the Z, AD and CD bits.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	message := new(dns.Msg)
	message.Data = data
	if err := message.Unpack(); err != nil {
		return nil, err
	}
	summary := &Summary{
		ID: message.ID, QR: bit(message.Response), Opcode: int(message.Opcode),
		AA: bit(message.Authoritative), TC: bit(message.Truncated), RD: bit(message.RecursionDesired),
		RA: bit(message.RecursionAvailable),
		Z:     bit(message.Zero)<<2 | bit(message.AuthenticatedData)<<1 | bit(message.CheckingDisabled),
		Rcode: int(message.Rcode), Questions: []question{},
	}
	for _, item := range message.Question {
		header := item.Header()
		summary.Questions = append(summary.Questions, question{absolute(header.Name), dns.RRToType(item), header.Class})
	}
	var err error
	if summary.Answers, err = records(message.Answer); err != nil {
		return nil, err
	}
	if summary.Authority, err = records(message.Ns); err != nil {
		return nil, err
	}
	if summary.Additional, err = records(message.Extra); err != nil {
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
