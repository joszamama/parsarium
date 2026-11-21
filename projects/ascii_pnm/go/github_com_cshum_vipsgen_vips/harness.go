// Package vipsgenpnm decodes one local ASCII PNM byte slice through the
// pinned vipsgen libvips binding (vips.NewPpmloadBuffer).
package vipsgenpnm

import (
	"encoding/json"
	"math"
	"sync"

	"github.com/cshum/vipsgen/vips"
)

type Summary struct {
	Width  int   `json:"width"`
	Height int   `json:"height"`
	RGB0   []int `json:"rgb0"`
	RGB1   []int `json:"rgb1"`
}

var startup sync.Once

func point(image *vips.Image, x, y int) ([]int, error) {
	values, err := image.Getpoint(x, y, nil)
	if err != nil {
		return nil, err
	}
	result := make([]int, len(values))
	for index, value := range values {
		result[index] = int(math.Round(value))
	}
	return result, nil
}

// Parse loads the bytes with libvips ppmload_buffer and reads the first pixel
// and the next one in raster order, which makes libvips decode the ASCII
// samples. RGB1 is nil for a one-pixel image.
func Parse(data []byte) (Summary, error) {
	startup.Do(func() {
		vips.Startup(&vips.Config{MaxCacheFiles: 0, MaxCacheMem: 0, MaxCacheSize: 0, ConcurrencyLevel: 1})
	})
	image, err := vips.NewPpmloadBuffer(data, nil)
	if err != nil {
		return Summary{}, err
	}
	defer image.Close()
	summary := Summary{Width: image.Width(), Height: image.Height()}
	if summary.Width < 1 || summary.Height < 1 {
		return summary, nil
	}
	if summary.RGB0, err = point(image, 0, 0); err != nil {
		return Summary{}, err
	}
	if summary.Width > 1 {
		summary.RGB1, err = point(image, 1, 0)
	} else if summary.Height > 1 {
		summary.RGB1, err = point(image, 0, 1)
	}
	if err != nil {
		return Summary{}, err
	}
	return summary, nil
}

func Encode(summary Summary) string {
	encoded, err := json.Marshal(summary)
	if err != nil {
		panic(err)
	}
	return string(encoded)
}
