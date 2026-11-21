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
	rgb := func(x, y int) []int {
		c := color.NRGBAModel.Convert(img.At(x, y)).(color.NRGBA)
		return []int{int(c.R), int(c.G), int(c.B)}
	}
	if result.Width >= 1 && result.Height >= 1 {
		result.RGB0 = rgb(bounds.Min.X, bounds.Min.Y)
	}
	// The second pixel is the next one in raster order, if the image has one.
	if result.Width > 1 {
		result.RGB1 = rgb(bounds.Min.X+1, bounds.Min.Y)
	} else if result.Width == 1 && result.Height > 1 {
		result.RGB1 = rgb(bounds.Min.X, bounds.Min.Y+1)
	}
	return result, nil
}
