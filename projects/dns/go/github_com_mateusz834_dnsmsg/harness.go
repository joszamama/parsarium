package dnsharness

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/netip"
	"strings"

	"github.com/mateusz834/dnsmsg"
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

// rdata decodes the record data with the parser method for the header's type.
func rdata(parser *dnsmsg.Parser, header dnsmsg.ResourceHeader) (string, error) {
	switch header.Type {
	case dnsmsg.TypeA:
		value, err := parser.ResourceA()
		if err != nil {
			return "", err
		}
		return netip.AddrFrom4(value.A).String(), nil
	case dnsmsg.TypeAAAA:
		value, err := parser.ResourceAAAA()
		if err != nil {
			return "", err
		}
		// RFC 5952 text of the 16 address bytes the parser returned.
		return netip.AddrFrom16(value.AAAA).String(), nil
	case dnsmsg.TypeCNAME:
		value, err := parser.ResourceCNAME()
		if err != nil {
			return "", err
		}
		return absolute(value.CNAME.String()), nil
	case dnsmsg.TypeNS:
		value, err := parser.ResourceNS()
		if err != nil {
			return "", err
		}
		return absolute(value.NS.String()), nil
	case dnsmsg.TypePTR:
		value, err := parser.ResourcePTR()
		if err != nil {
			return "", err
		}
		return absolute(value.PTR.String()), nil
	case dnsmsg.TypeMX:
		value, err := parser.ResourceMX()
		if err != nil {
			return "", err
		}
		return fmt.Sprintf("%d %s", value.Pref, absolute(value.MX.String())), nil
	}
	return "", fmt.Errorf("record type %d is outside the control subset", header.Type)
}

func section(parser *dnsmsg.Parser) ([]record, error) {
	out := []record{}
	for {
		header, err := parser.ResourceHeader()
		if errors.Is(err, dnsmsg.ErrSectionDone) {
			return out, nil
		}
		if err != nil {
			return nil, err
		}
		text, err := rdata(parser, header)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(header.Name.String()), uint16(header.Type), uint16(header.Class), header.TTL, text})
	}
}

// Parse decodes one DNS message from local bytes with dnsmsg.Parse and the incremental Parser.
// The library exposes AD and CD through Flags.Bit but defines no constant for the reserved Z bit,
// so z carries AD and CD only.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	parser, header, err := dnsmsg.Parse(data)
	if err != nil {
		return nil, err
	}
	flags := header.Flags
	summary := &Summary{
		ID: header.ID, QR: bit(flags.Response()), Opcode: int(flags.OpCode()),
		AA: bit(flags.Bit(dnsmsg.BitAA)), TC: bit(flags.Bit(dnsmsg.BitTC)), RD: bit(flags.Bit(dnsmsg.BitRD)),
		RA: bit(flags.Bit(dnsmsg.BitRA)), Z: bit(flags.Bit(dnsmsg.BitAD))<<1 | bit(flags.Bit(dnsmsg.BitCD)),
		Rcode: int(flags.RCode()), Questions: []question{},
	}
	for {
		item, err := parser.Question()
		if errors.Is(err, dnsmsg.ErrSectionDone) {
			break
		}
		if err != nil {
			return nil, err
		}
		summary.Questions = append(summary.Questions, question{absolute(item.Name.String()), uint16(item.Type), uint16(item.Class)})
	}
	if err := parser.StartAnswers(); err != nil {
		return nil, err
	}
	if summary.Answers, err = section(&parser); err != nil {
		return nil, err
	}
	if err := parser.StartAuthorities(); err != nil {
		return nil, err
	}
	if summary.Authority, err = section(&parser); err != nil {
		return nil, err
	}
	if err := parser.StartAdditionals(); err != nil {
		return nil, err
	}
	if summary.Additional, err = section(&parser); err != nil {
		return nil, err
	}
	if err := parser.End(); err != nil {
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
