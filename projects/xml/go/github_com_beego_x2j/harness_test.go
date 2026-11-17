package xmlharness

import (
	"fmt"
	"os"
	"testing"
)

// The []byte/string path deletes whitespace before every '<', including the
// one inside the catalog control's CDATA section ("x < y" becomes "x< y").
const expectedJSON = `{"bytes":{"attributes":["catalog/-c=urn:parsarium:catalog","catalog/-version=1","catalog/-xmlns=urn:parsarium:item","catalog/item[0]/-id=a1","catalog/item[0]/-lang=es","catalog/item[1]/-id=b2"],"elements":["catalog","catalog/item[0]","catalog/item[1]","catalog/item[1]/name","catalog/item[1]/note"],"empty_elements":[],"lists":["catalog/item=2"],"max_depth":3,"root":"catalog","text":["catalog/item[0]/#text=Café & té","catalog/item[1]/name=Zürich <HQ>","catalog/item[1]/note=x< y"]},"reader":{"attributes":["catalog/-c=urn:parsarium:catalog","catalog/-version=1","catalog/-xmlns=urn:parsarium:item","catalog/item[0]/-id=a1","catalog/item[0]/-lang=es","catalog/item[1]/-id=b2"],"elements":["catalog","catalog/item[0]","catalog/item[1]","catalog/item[1]/name","catalog/item[1]/note"],"empty_elements":[],"lists":["catalog/#text=3","catalog/item=2"],"max_depth":3,"root":"catalog","text":["catalog/#text[0]=\u000a  ","catalog/#text[1]=\u000a  ","catalog/#text[2]=\u000a","catalog/item[0]/#text=Café & té","catalog/item[1]/name=Zürich <HQ>","catalog/item[1]/note=x < y"]}}`

const differentialJSON = `{"bytes":{"attributes":["order/-p=urn:parsarium:price","order/-xmlns=urn:parsarium:order","order/line[0]/-currency=EUR","order/line[0]/-n=1","order/line[1]/-n=2","order/line[1]/-note=say \"hi\"","order/line[1]/plain/-xmlns="],"elements":["order","order/line[0]","order/line[0]/amount","order/line[0]/sku","order/line[1]","order/line[1]/plain","order/line[1]/plain/leaf"],"empty_elements":["order/line[1]/plain/leaf"],"lists":["order/line=2"],"max_depth":4,"root":"order","text":["order/line[0]/amount=12.50 €","order/line[0]/sku=A-7"]},"reader":{"attributes":["order/-p=urn:parsarium:price","order/-xmlns=urn:parsarium:order","order/line[0]/-currency=EUR","order/line[0]/-n=1","order/line[1]/-n=2","order/line[1]/-note=say \"hi\"","order/line[1]/plain/-xmlns="],"elements":["order","order/line[0]","order/line[0]/amount","order/line[0]/sku","order/line[1]","order/line[1]/plain","order/line[1]/plain/leaf"],"empty_elements":["order/line[1]/plain/leaf"],"lists":["order/#text=4","order/line=2"],"max_depth":4,"root":"order","text":["order/#text[0]=\u000a  ","order/#text[1]=\u000a  ","order/#text[2]=\u000a  ","order/#text[3]=\u000a","order/line[0]/amount=12.50 €","order/line[0]/sku=A-7"]}}`

func check(t *testing.T, variable, fallback, expected, label string) {
	path := os.Getenv(variable)
	if path == "" {
		path = fallback
	}
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	got, err := Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	encoded := Encode(got)
	if encoded != expected {
		t.Fatalf("%s mismatch: %s", label, encoded)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}

func TestControl(t *testing.T) {
	check(t, "PARSARIUM_CONTROL", "/input/control", expectedJSON, "control")
}

func TestDifferential(t *testing.T) {
	check(t, "PARSARIUM_DIFFERENTIAL", "/input/differential", differentialJSON, "differential")
}

func FuzzXML(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
