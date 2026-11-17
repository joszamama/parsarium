// Go standard-library JSON/XML control adapter. Usage: go run main.go <api> <control>
package main

import (
	"bytes"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"os"
	"sort"
	"strings"
)

func main() {
	api, data := os.Args[1], must(os.ReadFile(os.Args[2]))
	var out map[string]any
	switch api {
	case "encoding/json.Unmarshal":
		var d map[string]any
		if err := json.Unmarshal(data, &d); err != nil {
			panic(err)
		}
		keys := []string{}
		for k := range d {
			keys = append(keys, k)
		}
		sort.Strings(keys)
		out = map[string]any{"keys": keys, "items": len(d["items"].([]any)), "text": d["nested"].(map[string]any)["text"], "count": d["count"]}
	case "encoding/xml.Decoder.Token":
		dec := xml.NewDecoder(bytes.NewReader(data))
		depth, children, root := 0, 0, ""
		ids, texts := []string{}, []string{}
		var cur *strings.Builder
		for {
			tok, err := dec.Token()
			if err != nil {
				if err.Error() == "EOF" {
					break
				}
				panic(err)
			}
			switch t := tok.(type) {
			case xml.StartElement:
				depth++
				if depth == 1 {
					root = "{" + t.Name.Space + "}" + t.Name.Local
				} else if depth == 2 {
					children++
					if t.Name.Local == "item" {
						for _, a := range t.Attr {
							if a.Name.Local == "id" {
								ids = append(ids, a.Value)
							}
						}
						cur = &strings.Builder{}
					}
				}
			case xml.CharData:
				if cur != nil {
					cur.Write(t)
				}
			case xml.EndElement:
				if depth == 2 && cur != nil {
					texts = append(texts, cur.String())
					cur = nil
				}
				depth--
			}
		}
		out = map[string]any{"root": root, "children": children, "ids": ids, "texts": texts}
	default:
		panic("unknown api " + api)
	}
	b := must(json.Marshal(out))
	fmt.Println(string(b))
}

func must[T any](v T, err error) T {
	if err != nil {
		panic(err)
	}
	return v
}
