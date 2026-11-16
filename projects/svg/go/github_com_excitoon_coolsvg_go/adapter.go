// Run a pinned Go SVG parser against the valid local two-rectangle control.
package main

import (
	"bytes"

	"encoding/json"
	"fmt"
	"image"
	"os"
	"strings"

	excitoon "github.com/excitoon/coolsvg-go"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	switch name {

	case "github.com/excitoon/coolsvg-go":
		icon, err := excitoon.ReadIconStream(r)
		if err != nil {
			return nil, err
		}
		img := image.NewRGBA(image.Rect(0, 0, 2, 1))
		if err := icon.Render(img); err != nil {
			return nil, err
		}
		return map[string]any{"width": icon.ViewBox.W, "red": img.RGBAAt(0, 0).R, "green": img.RGBAAt(1, 0).G}, nil

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
