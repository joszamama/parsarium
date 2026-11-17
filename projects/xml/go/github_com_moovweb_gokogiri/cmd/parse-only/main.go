package main

import (
	"fmt"
	"os"

	x "github.com/moovweb/gokogiri/xml"
)

// This probe stops after the native parse call. It checks that input-dependent
// AFL++ feedback is reached before the DOM traversal used by the main harness.
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	input, err := os.ReadFile(os.Args[1])
	if err != nil || len(input) == 0 || len(input) > 1<<20 {
		os.Exit(2)
	}
	document, err := x.Parse(input, x.DefaultEncodingBytes, nil,
		x.XML_PARSE_NONET|x.XML_PARSE_NOCDATA, nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	document.Free()
}
