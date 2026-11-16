// Run a pinned Go SVG parser against the valid local two-rectangle control.
package main

import (
	"bytes"

	"encoding/json"
	"fmt"

	"os"
	"strings"
	"github.com/tdewolff/minify/v2"

	minsvg "github.com/tdewolff/minify/v2/svg"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	switch name {

	case "github.com/tdewolff/minify/v2/svg":
		var output bytes.Buffer
		if err := minsvg.Minify(minify.New(), &output, r, nil); err != nil {
			return nil, err
		}
		return map[string]any{"minified": output.String()}, nil

	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	if !strings.HasSuffix(os.Args[2], ".svg") {
		panic("expected SVG control path")
	}
	result, err := run(os.Args[1], data)
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
