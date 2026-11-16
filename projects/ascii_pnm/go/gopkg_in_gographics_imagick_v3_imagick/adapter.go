// Run one pinned Go ASCII PNM decoder against a valid local P1, P2, or P3 control.
package main

import (
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"os"

	"gopkg.in/gographics/imagick.v3/imagick"
)

func pixels(img image.Image) map[string]any {
	b := img.Bounds()
	a := color.NRGBAModel.Convert(img.At(b.Min.X, b.Min.Y)).(color.NRGBA)
	z := color.NRGBAModel.Convert(img.At(b.Min.X+1, b.Min.Y)).(color.NRGBA)
	return map[string]any{"width": b.Dx(), "height": b.Dy(), "rgb0": []int{int(a.R), int(a.G), int(a.B)}, "rgb1": []int{int(z.R), int(z.G), int(z.B)}}
}

func run(name string, data []byte) (map[string]any, error) {
	var img image.Image
	var err error
	switch name {

	case "gopkg.in/gographics/imagick.v3/imagick":
		imagick.Initialize()
		defer imagick.Terminate()
		wand := imagick.NewMagickWand()
		defer wand.Destroy()
		if readErr := wand.ReadImageBlob(data); readErr != nil {
			return nil, readErr
		}
		return map[string]any{"width": wand.GetImageWidth(), "height": wand.GetImageHeight()}, nil
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
