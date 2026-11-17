package main

import (
	"github.com/tosone/minimp3"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(2)
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil || len(data) == 0 || len(data) > 1<<20 {
		return
	}
	decoder, _, err := minimp3.DecodeFull(data)
	if err == nil && decoder != nil {
		decoder.Close()
	}
}
