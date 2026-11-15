package pnmharness

import (
	"bytes"
	"image/color"

	pnm "github.com/jbuchbinder/gopnm"
)

type Result struct {
	Width  int   `json:"width"`
	Height int   `json:"height"`
	RGB0   []int `json:"rgb0"`
	RGB1   []int `json:"rgb1"`
}

func Parse(data []byte) (Result, error) {
	img, err := pnm.Decode(bytes.NewReader(data))
	if err != nil {
		return Result{}, err
	}
	bounds := img.Bounds()
	result := Result{Width: bounds.Dx(), Height: bounds.Dy()}
	if result.Width >= 2 && result.Height >= 1 {
		first := color.NRGBAModel.Convert(img.At(bounds.Min.X, bounds.Min.Y)).(color.NRGBA)
		second := color.NRGBAModel.Convert(img.At(bounds.Min.X+1, bounds.Min.Y)).(color.NRGBA)
		result.RGB0 = []int{int(first.R), int(first.G), int(first.B)}
		result.RGB1 = []int{int(second.R), int(second.G), int(second.B)}
	}
	return result, nil
}
