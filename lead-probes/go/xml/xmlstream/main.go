package main

import (
	"bytes"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"mellium.im/xmlstream"
)

// Each mode reads one local XML control through an xmlstream API. The
// caller-built encoding/xml.Decoder is the only tokenizer xmlstream accepts.
func main() {
	if len(os.Args) != 3 {
		panic("usage: probe readall|iter|innerreader CONTROL")
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	var result any
	switch os.Args[1] {
	case "readall":
		result, err = readAll(data)
	case "iter":
		result, err = iterate(data)
	case "innerreader":
		result, err = innerReader(data)
	default:
		err = fmt.Errorf("unknown mode %q", os.Args[1])
	}
	if err != nil {
		panic(err)
	}
	encoded, err := json.Marshal(map[string]any{
		"mode": os.Args[1], "control": filepath.Base(os.Args[2]), "result": result,
	})
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}

// readAll collects tokens with xmlstream.ReadAll(xml.NewDecoder(io.Reader)).
func readAll(data []byte) (map[string]any, error) {
	tokens, err := xmlstream.ReadAll(xml.NewDecoder(bytes.NewReader(data)))
	if err != nil {
		return nil, err
	}
	s := &summary{namespaces: map[string]bool{}}
	depth := 0
	for _, token := range tokens {
		switch t := token.(type) {
		case xml.StartElement:
			depth++
			s.start(t, depth)
		case xml.EndElement:
			depth--
			s.flush()
		case xml.CharData:
			s.run.Write(t)
		case xml.Comment, xml.ProcInst, xml.Directive:
			s.flush()
		}
	}
	s.flush()
	return s.result()
}

// iterate walks children with xmlstream.NewIter after the root start element.
func iterate(data []byte) (map[string]any, error) {
	decoder := xml.NewDecoder(bytes.NewReader(data))
	s := &summary{namespaces: map[string]bool{}}
	for {
		token, err := decoder.Token()
		if err != nil {
			return nil, err
		}
		if start, ok := token.(xml.StartElement); ok {
			s.start(start, 1)
			break
		}
	}
	if err := s.walk(decoder, 1); err != nil {
		return nil, err
	}
	s.flush()
	return s.result()
}

func (s *summary) walk(r xml.TokenReader, depth int) error {
	iter := xmlstream.NewIter(r)
	for iter.Next() {
		start, child := iter.Current()
		if start == nil {
			token, err := child.Token()
			if err != nil && err != io.EOF {
				return err
			}
			if text, ok := token.(xml.CharData); ok {
				s.run.Write(text)
			} else {
				s.flush()
			}
			continue
		}
		s.start(*start, depth+1)
		if err := s.walk(child, depth+1); err != nil {
			return err
		}
		s.flush()
	}
	if err := iter.Err(); err != nil {
		return err
	}
	return iter.Close()
}

// innerReader records the bytes xmlstream.InnerReader(io.Reader) returns.
func innerReader(data []byte) (map[string]any, error) {
	decoder := xml.NewDecoder(bytes.NewReader(data))
	offset := int64(0)
	for {
		token, err := decoder.RawToken()
		if err != nil {
			return nil, err
		}
		if _, ok := token.(xml.StartElement); ok {
			break
		}
		offset = decoder.InputOffset()
	}
	result := map[string]any{"root_offset": offset}
	for key, input := range map[string][]byte{
		"control": data[offset:],
		// InnerReader sizes the body from buffered bytes, so trailing bytes
		// after the root end tag change the result; this is a comparison only.
		"trailing_whitespace_trimmed": bytes.TrimRight(data[offset:], " \t\r\n"),
	} {
		inner, err := io.ReadAll(xmlstream.InnerReader(bytes.NewReader(input)))
		outcome := map[string]any{"inner_bytes": string(inner)}
		if err != nil {
			outcome["error"] = err.Error()
		}
		result[key] = outcome
	}
	return result, nil
}

type summary struct {
	elements     []string
	attributes   []string
	namespaces   map[string]bool
	declarations int
	maxDepth     int
	text         []string
	run          strings.Builder
}

func (s *summary) start(t xml.StartElement, depth int) {
	s.flush()
	s.elements = append(s.elements, clark(t.Name.Space, t.Name.Local))
	s.maxDepth = max(s.maxDepth, depth)
	for _, attr := range t.Attr {
		if attr.Name.Local == "xmlns" || attr.Name.Space == "xmlns" {
			s.declarations++
			if attr.Value != "" {
				s.namespaces[attr.Value] = true
			}
			continue
		}
		s.attributes = append(s.attributes, clark(attr.Name.Space, attr.Name.Local)+"="+attr.Value)
	}
}

func (s *summary) flush() {
	if segment := strings.TrimSpace(s.run.String()); segment != "" {
		s.text = append(s.text, segment)
	}
	s.run.Reset()
}

func (s *summary) result() (map[string]any, error) {
	if len(s.elements) == 0 {
		return nil, fmt.Errorf("document has no root element")
	}
	namespaces := make([]string, 0, len(s.namespaces))
	for uri := range s.namespaces {
		namespaces = append(namespaces, uri)
	}
	sort.Strings(namespaces)
	return map[string]any{
		"attributes":             append([]string{}, s.attributes...),
		"elements":               s.elements,
		"max_depth":              s.maxDepth,
		"namespace_declarations": s.declarations,
		"namespaces":             namespaces,
		"root":                   s.elements[0],
		"text":                   append([]string{}, s.text...),
	}, nil
}

func clark(space, local string) string {
	if space == "" {
		return local
	}
	return "{" + space + "}" + local
}
