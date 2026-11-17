package dnsharness

import (
	"fmt"
	"os"
	"testing"
)

const expectedJSON = `{"id":43981,"qr":1,"opcode":0,"aa":0,"tc":0,"rd":1,"ra":1,"z":0,"rcode":0,"qdcount":1,"ancount":4,"nscount":0,"arcount":0,"questions":[{"name":"www.example.test.","type":1,"class":1}],"answers":[{"name":"www.example.test.","type":5,"class":1,"ttl":3600,"rdata":"example.test."},{"name":"example.test.","type":1,"class":1,"ttl":300,"rdata":"192.0.2.10"},{"name":"example.test.","type":28,"class":1,"ttl":600,"rdata":"2001:db8::10"},{"name":"example.test.","type":15,"class":1,"ttl":7200,"rdata":"10 mail.example.test."}],"authority":[],"additional":[]}`

func TestControl(t *testing.T) {
	data, err := os.ReadFile("/input/control")
	if err != nil {
		t.Fatal(err)
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	encoded := Encode(got)
	if encoded != expectedJSON {
		t.Fatalf("control mismatch: %s", encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

// TestReplay prints the summary of /input/case for the differential checker.
func TestReplay(t *testing.T) {
	data, err := os.ReadFile("/input/case")
	if err != nil {
		t.Skip("no /input/case")
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", Encode(got))
}

func FuzzDNS(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
