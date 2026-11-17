package main

import (
	"fmt"
	"os"

	harness "parsarium.local/lestrrat-libxml2-xml"
)

// This probe stops after the native parse call. It checks that input-dependent
// AFL++ feedback is reached before the DOM traversal used by the main harness.
func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	input, err := os.ReadFile(os.Args[1])
	if err != nil {
		os.Exit(2)
	}
	document, err := harness.ParseDocument(input)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	document.Free()
}
