package imagingharness

import (
	"bytes"
	"image/color"

	"github.com/disintegration/imaging"
)

type Result struct {
	Width  int   `json:"width"`
	Height int   `json:"height"`
	RGBA   []int `json:"rgba"`
}

// Parse passes supplied bytes to imaging.Decode, then observes every pixel.
func Parse(data []byte) (Result, error) {
	img, err := imaging.Decode(bytes.NewReader(data))
	if err != nil {
		return Result{}, err
	}
	bounds := img.Bounds()
	result := Result{Width: bounds.Dx(), Height: bounds.Dy()}
	if result.Width <= 0 || result.Height <= 0 || result.Width > 4096 || result.Height > 4096 {
		return Result{}, nil
	}
	result.RGBA = make([]int, 0, result.Width*result.Height*4)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			pixel := color.NRGBAModel.Convert(img.At(x, y)).(color.NRGBA)
			result.RGBA = append(result.RGBA, int(pixel.R), int(pixel.G), int(pixel.B), int(pixel.A))
		}
	}
	return result, nil
}
