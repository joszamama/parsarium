package main

import (
	"encoding/json"
	"fmt"
	"os"
	"testing"
)

func TestProbe(t *testing.T) {
	got, err := parse(os.Getenv("PROBE_INPUT"))
	if err != nil {
		t.Fatal(err)
	}
	encoded, err := json.Marshal(got)
	if err != nil {
		t.Fatal(err)
	}
	fmt.Printf("OBSERVED_JSON:%s\n", encoded)
}
