// Run a pinned Go PNG parser against a local, valid PNG control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"os"

	fumin "github.com/fumin/png"
)

func pixels(img image.Image) map[string]any {
	b := img.Bounds()
	values := make([]int, 0, b.Dx()*b.Dy()*4)
	for y := b.Min.Y; y < b.Max.Y; y++ {
		for x := b.Min.X; x < b.Max.X; x++ {
			c := color.NRGBAModel.Convert(img.At(x, y)).(color.NRGBA)
			values = append(values, int(c.R), int(c.G), int(c.B), int(c.A))
		}
	}
	return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgba": values}
}

func run(name, path string) (map[string]any, error) {
	var img image.Image
	var err error
	switch name {

	case "github.com/fumin/png":
		data, readErr := os.ReadFile(path)
		if readErr != nil {
			return nil, readErr
		}
		r := bytes.NewReader(data)
		switch name {

		case "github.com/fumin/png":
			var decoder *fumin.Decoder
			decoder, err = fumin.NewDecoder(r)
			if err != nil {
				return nil, err
			}
			defer decoder.Close()
			b := decoder.Bounds()
			if b.Dx() != 2 || b.Dy() != 1 {
				return nil, fmt.Errorf("unexpected bounds: %v", b)
			}
			row, decodeErr := decoder.DecodeRow()
			if decodeErr != nil {
				return nil, decodeErr
			}
			values := make([]int, len(row))
			for i, v := range row {
				values[i] = int(v)
			}
			return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgba": values}, nil

		}

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
	result, err := run(os.Args[1], os.Args[2])
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
