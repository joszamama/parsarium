// Parse a valid local ASCII PNM through the pinned gmagick GraphicsMagick binding.
package main

import (
	"encoding/json"
	"os"

	"github.com/gographics/gmagick"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_gmagick CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	gmagick.Initialize()
	defer gmagick.Terminate()
	wand := gmagick.NewMagickWand()
	defer wand.Destroy()
	if err := wand.ReadImageBlob(data); err != nil {
		panic(err)
	}
	result := map[string]any{"width": wand.GetImageWidth(), "height": wand.GetImageHeight(),
		"format": wand.GetImageFormat(), "colors": wand.GetImageColors()}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
