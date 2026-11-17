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

func point(image *vips.Image, x int) ([]int, error) {
	values, err := image.Getpoint(x, 0, nil)
	if err != nil {
		return nil, err
	}
	result := make([]int, len(values))
	for index, value := range values {
		result[index] = int(math.Round(value))
	}
	return result, nil
}

// Parse loads the bytes with libvips ppmload_buffer and reads the first two
// pixels of row 0, which makes libvips decode the ASCII samples.
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
	if summary.Width < 2 {
		return summary, nil
	}
	if summary.RGB0, err = point(image, 0); err != nil {
		return Summary{}, err
	}
	if summary.RGB1, err = point(image, 1); err != nil {
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
