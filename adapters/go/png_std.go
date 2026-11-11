// Verify Go's documented image/png.Decode on the shared valid PNG control.
package main

import (
	"bytes"
	"encoding/json"
	"image"
	"image/color"
	"image/png"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run adapters/go/png_std.go CONTROL_PATH")
	}
	input, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	decoded, err := png.Decode(bytes.NewReader(input))
	if err != nil {
		panic(err)
	}
	bounds := decoded.Bounds()
	values := make([]int, 0, bounds.Dx()*bounds.Dy()*4)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			pixel := color.NRGBAModel.Convert(decoded.At(x, y)).(color.NRGBA)
			values = append(values, int(pixel.R), int(pixel.G), int(pixel.B), int(pixel.A))
		}
	}
	config, err := png.DecodeConfig(bytes.NewReader(input))
	if err != nil {
		panic(err)
	}
	generic, format, err := image.Decode(bytes.NewReader(input))
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(map[string]any{
		"decode":  map[string]any{"width": bounds.Dx(), "height": bounds.Dy(), "rgba": values},
		"config":  map[string]any{"width": config.Width, "height": config.Height},
		"generic": map[string]any{"format": format, "width": generic.Bounds().Dx(), "height": generic.Bounds().Dy()},
	}); err != nil {
		panic(err)
	}
}
