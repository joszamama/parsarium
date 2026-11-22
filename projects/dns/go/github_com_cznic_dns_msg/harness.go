package dnsharness

import (
	"encoding/json"
	"fmt"
	"strings"
	"time"

	
	"github.com/cznic/dns/msg"
	"github.com/cznic/dns/rr"
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

// msg's package init starts a goroutine that reseeds its message-ID generator and
// then sleeps for ten minutes. Whether its first loop body runs before a short process
// exits depends on scheduling, which made the Go coverage blocks of msg/message.go
// lines 35-41 vary between identical runs. The harness waits briefly once at start-up so
// that the first reseed always completes; parsing is unchanged.
func init() {
	time.Sleep(50 * time.Millisecond)
}

// quoted joins TXT character-strings as "<string>" separated by spaces, the form the
// other DNS harnesses print.
func quoted(items []string) string {
	out := make([]string, len(items))
	for index, item := range items {
		out[index] = `"` + item + `"`
	}
	return strings.Join(out, " ")
}

func rdata(data interface{}) (string, error) {
	switch value := data.(type) {
	case *rr.A:
		return value.Address.String(), nil
	case *rr.AAAA:
		return value.Address.String(), nil
	case *rr.CNAME:
		return absolute(value.Name), nil
	case *rr.NS:
		return absolute(value.NSDName), nil
	case *rr.PTR:
		return absolute(value.PTRDName), nil
	case *rr.MX:
		return fmt.Sprintf("%d %s", value.Preference, absolute(value.Exchange)), nil
	case *rr.TXT:
		return quoted(value.S), nil
	}
	return "", fmt.Errorf("record data %T is outside the control subset", data)
}

func records(list rr.RRs) ([]record, error) {
	out := []record{}
	for _, item := range list {
		text, err := rdata(item.RData)
		if err != nil {
			return nil, err
		}
		out = append(out, record{absolute(item.Name), uint16(item.Type), uint16(item.Class), uint32(item.TTL), text})
	}
	return out, nil
}

// Parse decodes one DNS message from local bytes with (*msg.Message).Decode, starting
// at offset 0 with no decode sniffer. The header keeps the Z, AD and CD bits.
func Parse(data []byte) (*Summary, error) {
	if len(data) == 0 || len(data) > 65535 {
		return nil, fmt.Errorf("input outside harness limit")
	}
	message := &msg.Message{}
	position := 0
	if err := message.Decode(data, &position, nil); err != nil {
		return nil, err
	}
	header := message.Header
	summary := &Summary{
		ID: header.ID, QR: bit(header.QR), Opcode: int(header.Opcode),
		AA: bit(header.AA), TC: bit(header.TC), RD: bit(header.RD), RA: bit(header.RA),
		Z:     bit(header.Z)<<2 | bit(header.AD)<<1 | bit(header.CD),
		Rcode: int(header.RCODE), Questions: []question{},
	}
	for _, item := range message.Question {
		summary.Questions = append(summary.Questions, question{absolute(item.QNAME), uint16(item.QTYPE), uint16(item.QCLASS)})
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
