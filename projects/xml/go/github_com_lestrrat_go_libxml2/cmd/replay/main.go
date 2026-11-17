package main

import (
	"fmt"
	"os"

	harness "parsarium.local/lestrrat-libxml2-xml"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	input, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	result, err := harness.Parse(input)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(harness.Encode(result))
	if status := harness.FlushNativeCoverage(); status != 0 {
		fmt.Fprintln(os.Stderr, "native coverage flush failed")
		os.Exit(2)
	}
}
