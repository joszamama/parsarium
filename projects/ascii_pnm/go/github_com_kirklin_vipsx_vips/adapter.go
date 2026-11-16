// Parse a valid local ASCII PPM through the pinned vipsx binding.
package main

import (
	"encoding/json"
	vips "github.com/kirklin/vipsx/vips"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_kirklin CONTROL_PATH")
	}
	if err := vips.Startup(); err != nil {
		panic(err)
	}
	defer vips.Shutdown()
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	img, err := vips.LoadBuffer(data)
	if err != nil {
		panic(err)
	}
	defer img.Close()
	if err := json.NewEncoder(os.Stdout).Encode(map[string]any{"width": img.Width(), "height": img.Height()}); err != nil {
		panic(err)
	}
}
