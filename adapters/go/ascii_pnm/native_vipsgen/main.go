// Parse a valid local ASCII PNM through the pinned vipsgen libvips binding.
package main

import (
	"encoding/json"
	"math"
	"os"

	"github.com/cshum/vipsgen/vips"
)

func point(image *vips.Image, x int) []int {
	values, err := image.Getpoint(x, 0, nil)
	if err != nil {
		panic(err)
	}
	result := make([]int, len(values))
	for index, value := range values {
		result[index] = int(math.Round(value))
	}
	return result
}

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_vipsgen CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	vips.Startup(&vips.Config{ConcurrencyLevel: 1})
	defer vips.Shutdown()
	image, err := vips.NewPpmloadBuffer(data, nil)
	if err != nil {
		panic(err)
	}
	defer image.Close()
	result := map[string]any{"width": image.Width(), "height": image.Height(),
		"rgb0": point(image, 0), "rgb1": point(image, 1)}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
