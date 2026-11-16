// Run a pinned Go SVG parser against the valid local two-rectangle control.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"

	"os"
	"strings"

	sfomuseum "github.com/sfomuseum/go-svg"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	switch name {

	case "github.com/sfomuseum/go-svg":
		img, err := sfomuseum.Rasterize(context.Background(), r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"width": img.Bounds().Dx(), "height": img.Bounds().Dy()}, nil

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
