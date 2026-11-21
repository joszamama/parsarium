// Run one pinned Go ASCII PNM decoder against a valid local P1, P2, or P3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"os"

	hexaflex "github.com/hexaflex/pnm"
)

func pixels(img image.Image) map[string]any {
	b := img.Bounds()
	rgb := func(x, y int) []int {
		c := color.NRGBAModel.Convert(img.At(x, y)).(color.NRGBA)
		return []int{int(c.R), int(c.G), int(c.B)}
	}
	// The second pixel is the next one in raster order; nil for a one-pixel image.
	var second []int
	if b.Dx() > 1 {
		second = rgb(b.Min.X+1, b.Min.Y)
	} else if b.Dy() > 1 {
		second = rgb(b.Min.X, b.Min.Y+1)
	}
	return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgb0": rgb(b.Min.X, b.Min.Y), "rgb1": second}
}

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	var img image.Image
	var err error
	switch name {

	case "github.com/hexaflex/pnm":
		img, err = hexaflex.Decode(r)

	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
	if err != nil {
		return nil, err
	}
	return pixels(img), nil
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	result, err := run(os.Args[1], data)
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
