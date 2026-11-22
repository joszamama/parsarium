package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/shadowy-pycoder/mshark/layers"
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

func absolute(name string) string {
	name = strings.ToLower(name)
	if !strings.HasSuffix(name, ".") {
		name += "."
	}
	return name
}

// rdata prints the typed RDATA value the layer decoded for the record.
// quoted joins TXT character-strings as "<string>" separated by spaces, the form the
// other DNS harnesses print.
func quoted(items []string) string {
	out := make([]string, len(items))
	for index, item := range items {
		out[index] = `"` + item + `"`
	}
	return strings.Join(out, " ")
}

func rdata(value layers.RData) (string, error) {
	switch item := value.(type) {
	case *layers.RDataA:
		return item.Address.String(), nil
	case *layers.RDataAAAA:
		// RFC 5952 text of the netip.Addr the parser built from the 16 RDATA bytes.
		return item.Address.String(), nil
	case *layers.RDataCNAME:
		return absolute(item.CName), nil
	case *layers.RDataNS:
		return absolute(item.NsdName), nil
	case *layers.RDataMX:
		return fmt.Sprintf("%d %s", item.Preference, absolute(item.Exchange)), nil
	case *layers.RDataTXT:
		// mshark keeps the whole TXT RDATA, length octets included, as one string.
		return quoted([]string{item.TxtData}), nil
	}
	return "", fmt.Errorf("record data %T is outside the control subset", value)
}

func section(items []*layers.ResourceRecord) ([]record, error) {
	out := []record{}
	for _, item := range items {
		if item.Type == nil || item.Class == nil {
			return nil, fmt.Errorf("record without type or class")
		}
		text, err := rdata(item.RData)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(item.Name), uint16(item.Type.Val), item.Class.Val, item.TTL, text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes with (*layers.DNSMessage).Parse.
// The flags come from the layer's DNSFlags fields; z is its Z, AU (AD) and NA (CD) bits.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	var message layers.DNSMessage
	if err := message.Parse(data); err != nil {
		return nil, err
	}
	flags := message.Flags
	if flags == nil || flags.QR == nil || flags.OPCode == nil || flags.RCode == nil {
		return nil, fmt.Errorf("message without decoded flags")
	}
	summary := &Summary{
		ID: message.TransactionID, QR: int(flags.QR.Val), Opcode: int(flags.OPCode.Val),
		AA: int(flags.AA), TC: int(flags.TC), RD: int(flags.RD), RA: int(flags.RA),
		Z: int(flags.Z)<<2 | int(flags.AU)<<1 | int(flags.NA), Rcode: int(flags.RCode.Val),
		QDCount: int(message.QDCount), ANCount: int(message.ANCount),
		NSCount: int(message.NSCount), ARCount: int(message.ARCount),
		Questions: []question{},
	}
	for _, item := range message.Questions {
		if item.Type == nil || item.Class == nil {
			return nil, fmt.Errorf("question without type or class")
		}
		summary.Questions = append(summary.Questions, question{absolute(item.Name), uint16(item.Type.Val), item.Class.Val})
	}
	var err error
	if summary.Answers, err = section(message.AnswerRRs); err != nil {
		return nil, err
	}
	if summary.Authority, err = section(message.AuthorityRRs); err != nil {
		return nil, err
	}
	if summary.Additional, err = section(message.AdditionalRRs); err != nil {
		return nil, err
	}
	return summary, nil
}

// Encode prints the summary as compact JSON in field order.
func Encode(summary *Summary) string {
	encoded, _ := json.Marshal(summary)
	return string(encoded)
}
