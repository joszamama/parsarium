// Run a pinned Go SVG parser against the valid local two-rectangle control.
package main

import (
	"bytes"

	"encoding/json"
	"fmt"

	"os"
	"strings"

	"cogentcore.org/core/math32"
	cogent "cogentcore.org/core/svg"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	switch name {

	case "cogentcore.org/core/svg":
		doc := cogent.NewSVG(math32.Vector2{X: 2, Y: 1})
		err := doc.ReadXML(r)
		if err != nil {
			return nil, err
		}
		// ReadXML stores the root width and height attributes, converted to
		// dots, in PhysicalWidth and PhysicalHeight; the viewBox is the user
		// coordinate system, not the document size. An attribute the file
		// does not set leaves the value empty and the field is omitted.
		result := map[string]any{"elements": doc.Root.NumChildren()}
		if doc.PhysicalWidth.Value != 0 {
			result["width"] = doc.PhysicalWidth.Dots
		}
		if doc.PhysicalHeight.Value != 0 {
			result["height"] = doc.PhysicalHeight.Dots
		}
		return result, nil
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
