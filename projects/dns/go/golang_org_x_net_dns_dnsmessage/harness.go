package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	"net/netip"
	
	"golang.org/x/net/dns/dnsmessage"
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

// rdata formats the decoded resource bodies. A and AAAA bodies are fixed byte arrays in
// dnsmessage; the harness prints them with net/netip (dotted quad, RFC 5952).
func rdata(body dnsmessage.ResourceBody) (string, error) {
	switch value := body.(type) {
	case *dnsmessage.AResource:
		return netip.AddrFrom4(value.A).String(), nil
	case *dnsmessage.AAAAResource:
		return netip.AddrFrom16(value.AAAA).String(), nil
	case *dnsmessage.CNAMEResource:
		return absolute(value.CNAME.String()), nil
	case *dnsmessage.NSResource:
		return absolute(value.NS.String()), nil
	case *dnsmessage.PTRResource:
		return absolute(value.PTR.String()), nil
	case *dnsmessage.MXResource:
		return fmt.Sprintf("%d %s", value.Pref, absolute(value.MX.String())), nil
	case *dnsmessage.TXTResource:
		quoted := make([]string, len(value.TXT))
		for index, item := range value.TXT {
			quoted[index] = `"` + item + `"`
		}
		return strings.Join(quoted, " "), nil
	}
	return "", fmt.Errorf("record body %T is outside the control subset", body)
}

func records(list []dnsmessage.Resource) ([]record, error) {
	out := []record{}
	for _, rr := range list {
		text, err := rdata(rr.Body)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(rr.Header.Name.String()), uint16(rr.Header.Type), uint16(rr.Header.Class), rr.Header.TTL, text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes with (*dnsmessage.Message).Unpack.
// dnsmessage.Header keeps AD and CD but not the reserved Z bit.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var message dnsmessage.Message
	if err := message.Unpack(data); err != nil {
		return nil, err
	}
	header := message.Header
	summary := &Summary{
		ID: header.ID, QR: bit(header.Response), Opcode: int(header.OpCode),
		AA: bit(header.Authoritative), TC: bit(header.Truncated), RD: bit(header.RecursionDesired),
		RA: bit(header.RecursionAvailable),
		Z:     bit(header.AuthenticData)<<1 | bit(header.CheckingDisabled),
		Rcode: int(header.RCode), Questions: []question{},
	}
	for _, item := range message.Questions {
		summary.Questions = append(summary.Questions, question{absolute(item.Name.String()), uint16(item.Type), uint16(item.Class)})
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
