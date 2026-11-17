package gmagickpnm

import (
	"os"
	"testing"
)

var controls = []struct{ file, want string }{
	{"controls/red-green.ppm", `{"width":2,"height":1,"format":"PPM","colors":2}`},
	{"controls/black-white.pgm", `{"width":2,"height":1,"format":"PGM","colors":2}`},
}

func TestControls(t *testing.T) {
	for _, control := range controls {
		t.Run(control.file, func(t *testing.T) {
			input, err := os.ReadFile(control.file)
			if err != nil {
				t.Fatal(err)
			}
			got, err := Parse(input)
			if err != nil {
				t.Fatal(err)
			}
			if Encode(got) != control.want {
				t.Fatalf("got %s\nwant %s", Encode(got), control.want)
			}
			t.Log("OBSERVED_JSON:" + Encode(got))
		})
	}
	if status := FlushNativeCoverage(); status != 0 {
		t.Fatalf("native coverage flush: %d", status)
	}
}

func FuzzParser(f *testing.F) {
	for _, control := range controls {
		input, err := os.ReadFile("/work/" + control.file)
		if err != nil {
			f.Fatal(err)
		}
		f.Add(input)
	}
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 || len(data) > (1<<20) {
			return
		}
		_, _ = Parse(data)
	})
}
