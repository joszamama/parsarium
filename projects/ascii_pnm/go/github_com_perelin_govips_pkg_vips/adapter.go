// Parse a valid local ASCII PPM through the pinned perelin libvips binding.
package main

import (
	"encoding/json"
	vips "github.com/perelin/govips/pkg/vips"
	"image/color"
	"image/png"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_perelin CONTROL_PATH")
	}
	vips.Startup(nil)
	defer vips.Shutdown()
	native, err := vips.Ppmload(os.Args[1])
	if err != nil {
		panic(err)
	}
	file, err := os.CreateTemp("", "parsarium-pnm-*.png")
	if err != nil {
		panic(err)
	}
	name := file.Name()
	file.Close()
	defer os.Remove(name)
	if err := vips.Pngsave(native, name); err != nil {
		panic(err)
	}
	pngFile, err := os.Open(name)
	if err != nil {
		panic(err)
	}
	defer pngFile.Close()
	img, err := png.Decode(pngFile)
	if err != nil {
		panic(err)
	}
	first := color.NRGBAModel.Convert(img.At(0, 0)).(color.NRGBA)
	second := color.NRGBAModel.Convert(img.At(1, 0)).(color.NRGBA)
	result := map[string]any{"width": img.Bounds().Dx(), "height": img.Bounds().Dy(), "rgb0": []int{int(first.R), int(first.G), int(first.B)}, "rgb1": []int{int(second.R), int(second.G), int(second.B)}}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
