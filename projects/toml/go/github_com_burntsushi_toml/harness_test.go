package tomlharness

import (
	"fmt"
	"os"
	"testing"
)

const expectedJSON = `{"database":{"limits":{"max":{"type":"integer","value":"10"},"min":{"type":"integer","value":"-2"}},"ports":[{"type":"integer","value":"8000"},{"type":"integer","value":"8001"},{"type":"integer","value":"8002"}],"ratio":{"type":"float","value":"3.25"}},"enabled":{"type":"bool","value":"true"},"owner":{"name":{"type":"string","value":"Zoë"},"since":{"type":"datetime","value":"1979-05-27T07:32:00Z"}},"products":[{"name":{"type":"string","value":"Hammer"},"sku":{"type":"integer","value":"738594937"}},{"color":{"type":"string","value":"gray"},"name":{"type":"string","value":"Nail"},"points":[{"x":{"type":"integer","value":"1"},"y":{"type":"integer","value":"2"}},{"x":{"type":"integer","value":"3"},"y":{"type":"integer","value":"4"}}]}],"retries":{"type":"integer","value":"3"},"servers":{"alpha":{"ip":{"type":"string","value":"10.0.0.1"},"tags":[{"type":"string","value":"edge"},{"type":"string","value":"eu"}]},"beta":{"enabled":{"type":"bool","value":"false"},"ip":{"type":"string","value":"10.0.0.2"}}},"title":{"type":"string","value":"Parsarium \"service\" control"}}`

const differentialJSON = `{"floats":{"exponent":{"type":"float","value":"1000.0"},"fraction":{"type":"float","value":"3.25"},"mixed":{"type":"float","value":"0.015625"},"negative":{"type":"float","value":"-0.5"}},"integers":{"binary":{"type":"integer","value":"13"},"decimal":{"type":"integer","value":"99"},"hex":{"type":"integer","value":"3735928559"},"negative":{"type":"integer","value":"-17"},"octal":{"type":"integer","value":"493"},"underscored":{"type":"integer","value":"1000000"}},"keys":{"a":{"b":{"c":{"type":"integer","value":"1"}}},"quoted key":{"type":"string","value":"q"},"site":{"example.com":{"type":"bool","value":"true"}}},"strings":{"escapes":{"type":"string","value":"tab\tquote\"backslash\\ é"},"literal":{"type":"string","value":"C:\\Users\\parsarium"},"multiline":{"type":"string","value":"first second"},"raw_multiline":{"type":"string","value":"line one\nline two"}},"times":{"local_date":{"type":"date-local","value":"1979-05-27"},"local_datetime":{"type":"datetime-local","value":"1979-05-27T07:32:00"},"local_time":{"type":"time-local","value":"00:32:00.25"},"offset":{"type":"datetime","value":"1979-05-27T07:32:00.5Z"}}}`

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

func FuzzTOML(f *testing.F) {
	f.Fuzz(func(t *testing.T, data []byte) { _, _ = Parse(data) })
}
