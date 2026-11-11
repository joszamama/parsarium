// Parse a valid local ASCII PPM through the pinned go-vips binding.
package main

import (
	"encoding/json"
	vips "gitee.com/shiqiyue/go-vips"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_shiqiyue CONTROL_PATH")
	}
	if err := vips.Init(); err != nil {
		panic(err)
	}
	defer vips.Shutdown()
	img, err := vips.PPMLoad(os.Args[1])
	if err != nil {
		panic(err)
	}
	defer img.Free()
	if err := json.NewEncoder(os.Stdout).Encode(map[string]any{"width": img.Width(), "height": img.Height()}); err != nil {
		panic(err)
	}
}
