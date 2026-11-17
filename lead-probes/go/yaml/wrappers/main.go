// Lead probe: run one Go YAML lead's documented API on one valid control and
// print the observed result as the Parsarium typed tree where the API can
// express one. Usage: probe <lead> <control.yaml>
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	"strings"

	"cuelang.org/go/cue/ast"
	"cuelang.org/go/cue/literal"
	"cuelang.org/go/cue/token"
	cueyaml "cuelang.org/go/encoding/yaml"
	ghodss "github.com/ghodss/yaml"
	koanfyaml "github.com/knadh/koanf/parsers/yaml"
	gypsy "github.com/kylelemons/go-gypsy/yaml"
	k8syaml "k8s.io/apimachinery/pkg/util/yaml"
	kyaml "sigs.k8s.io/kustomize/kyaml/yaml"
	sigs "sigs.k8s.io/yaml"
)

// orderedJSON decodes JSON text token by token, so the typed tree keeps the
// key order of the JSON text the wrapper produced. Numbers with '.', 'e' or
// 'E' are typed float, the rest int.
func orderedJSON(text []byte) (any, error) {
	decoder := json.NewDecoder(bytes.NewReader(text))
	decoder.UseNumber()
	return jsonValue(decoder)
}

func jsonValue(decoder *json.Decoder) (any, error) {
	tok, err := decoder.Token()
	if err != nil {
		return nil, err
	}
	switch value := tok.(type) {
	case json.Delim:
		if value == '{' {
			pairs := []any{}
			for decoder.More() {
				key, err := decoder.Token()
				if err != nil {
					return nil, err
				}
				child, err := jsonValue(decoder)
				if err != nil {
					return nil, err
				}
				pairs = append(pairs, []any{key, child})
			}
			_, err = decoder.Token()
			return []any{"map", pairs}, err
		}
		items := []any{}
		for decoder.More() {
			child, err := jsonValue(decoder)
			if err != nil {
				return nil, err
			}
			items = append(items, child)
		}
		_, err = decoder.Token()
		return []any{"seq", items}, err
	case string:
		return []any{"str", value}, nil
	case bool:
		return []any{"bool", value}, nil
	case nil:
		return []any{"null"}, nil
	case json.Number:
		if strings.ContainsAny(string(value), ".eE") {
			number, err := value.Float64()
			return []any{"float", strconv.FormatFloat(number, 'g', -1, 64)}, err
		}
		return []any{"int", string(value)}, nil
	}
	return nil, fmt.Errorf("unexpected JSON token %v", tok)
}

// native types decoded Go values; Go maps have no order, so their keys are
// reported sorted.
func native(value any) any {
	switch node := value.(type) {
	case map[string]any:
		keys := make([]string, 0, len(node))
		for key := range node {
			keys = append(keys, key)
		}
		sort.Strings(keys)
		pairs := []any{}
		for _, key := range keys {
			pairs = append(pairs, []any{key, native(node[key])})
		}
		return []any{"map", pairs}
	case []any:
		items := []any{}
		for _, item := range node {
			items = append(items, native(item))
		}
		return []any{"seq", items}
	case string:
		return []any{"str", node}
	case nil:
		return []any{"null"}
	case bool:
		return []any{"bool", node}
	case int:
		return []any{"int", strconv.Itoa(node)}
	case int64:
		return []any{"int", strconv.FormatInt(node, 10)}
	case uint64:
		return []any{"int", strconv.FormatUint(node, 10)}
	case float64:
		return []any{"float", strconv.FormatFloat(node, 'g', -1, 64)}
	}
	return []any{"unsupported", fmt.Sprintf("%T", value)}
}

// gypsyTree reports go-gypsy nodes: Map is a Go map (keys sorted here), List a
// slice and Scalar an untyped string.
func gypsyTree(node gypsy.Node) any {
	switch value := node.(type) {
	case gypsy.Map:
		keys := make([]string, 0, len(value))
		for key := range value {
			keys = append(keys, key)
		}
		sort.Strings(keys)
		pairs := []any{}
		for _, key := range keys {
			pairs = append(pairs, []any{key, gypsyTree(value[key])})
		}
		return []any{"map", pairs}
	case gypsy.List:
		items := []any{}
		for _, item := range value {
			items = append(items, gypsyTree(item))
		}
		return []any{"seq", items}
	case gypsy.Scalar:
		return []any{"scalar", string(value)}
	case nil:
		return []any{"null"}
	}
	return []any{"unsupported", fmt.Sprintf("%T", node)}
}

// kyamlTree walks the yaml.Node that kyaml's RNode wraps.
func kyamlTree(node *kyaml.Node) (any, error) {
	switch node.Kind {
	case kyaml.AliasNode:
		return kyamlTree(node.Alias)
	case kyaml.DocumentNode:
		return kyamlTree(node.Content[0])
	case kyaml.MappingNode:
		pairs := []any{}
		for index := 0; index+1 < len(node.Content); index += 2 {
			child, err := kyamlTree(node.Content[index+1])
			if err != nil {
				return nil, err
			}
			pairs = append(pairs, []any{node.Content[index].Value, child})
		}
		return []any{"map", pairs}, nil
	case kyaml.SequenceNode:
		items := []any{}
		for _, item := range node.Content {
			child, err := kyamlTree(item)
			if err != nil {
				return nil, err
			}
			items = append(items, child)
		}
		return []any{"seq", items}, nil
	case kyaml.ScalarNode:
		switch node.ShortTag() {
		case "!!str":
			return []any{"str", node.Value}, nil
		case "!!null":
			return []any{"null"}, nil
		case "!!bool":
			var value bool
			err := node.Decode(&value)
			return []any{"bool", value}, err
		case "!!int":
			var value int64
			err := node.Decode(&value)
			return []any{"int", strconv.FormatInt(value, 10)}, err
		case "!!float":
			var value float64
			err := node.Decode(&value)
			return []any{"float", strconv.FormatFloat(value, 'g', -1, 64)}, err
		}
	}
	return nil, fmt.Errorf("unsupported kyaml node")
}

// cueTree maps the CUE AST that encoding/yaml.Extract returns.
func cueTree(expr ast.Node) (any, error) {
	switch node := expr.(type) {
	case *ast.File:
		if len(node.Decls) == 1 {
			if embed, ok := node.Decls[0].(*ast.EmbedDecl); ok {
				return cueTree(embed.Expr)
			}
		}
		return cueFields(node.Decls)
	case *ast.StructLit:
		return cueFields(node.Elts)
	case *ast.ListLit:
		items := []any{}
		for _, item := range node.Elts {
			child, err := cueTree(item)
			if err != nil {
				return nil, err
			}
			items = append(items, child)
		}
		return []any{"seq", items}, nil
	case *ast.UnaryExpr:
		if node.Op != token.SUB {
			return nil, fmt.Errorf("unsupported unary %v", node.Op)
		}
		child, err := cueTree(node.X)
		if err != nil {
			return nil, err
		}
		pair := child.([]any)
		if pair[0] == "float" {
			return []any{"float", "-" + pair[1].(string)}, nil
		}
		return []any{pair[0], "-" + pair[1].(string)}, nil
	case *ast.BasicLit:
		switch node.Kind {
		case token.STRING:
			text, err := literal.Unquote(node.Value)
			return []any{"str", text}, err
		case token.INT:
			return []any{"int", node.Value}, nil
		case token.FLOAT:
			number, err := strconv.ParseFloat(node.Value, 64)
			return []any{"float", strconv.FormatFloat(number, 'g', -1, 64)}, err
		case token.NULL:
			return []any{"null"}, nil
		case token.TRUE:
			return []any{"bool", true}, nil
		case token.FALSE:
			return []any{"bool", false}, nil
		}
	case *ast.Ident:
		switch node.Name {
		case "true":
			return []any{"bool", true}, nil
		case "false":
			return []any{"bool", false}, nil
		case "null":
			return []any{"null"}, nil
		}
	}
	return nil, fmt.Errorf("unsupported CUE node %T", expr)
}

func cueFields(decls []ast.Decl) (any, error) {
	pairs := []any{}
	for _, decl := range decls {
		field, ok := decl.(*ast.Field)
		if !ok {
			return nil, fmt.Errorf("unsupported CUE declaration %T", decl)
		}
		name, _, err := ast.LabelName(field.Label)
		if err != nil {
			return nil, err
		}
		child, err := cueTree(field.Value)
		if err != nil {
			return nil, err
		}
		pairs = append(pairs, []any{name, child})
	}
	return []any{"map", pairs}, nil
}

func run(lead string, data []byte) (any, string, error) {
	switch lead {
	case "ghodss":
		text, err := ghodss.YAMLToJSON(data)
		if err != nil {
			return nil, "", err
		}
		tree, err := orderedJSON(text)
		return tree, string(text), err
	case "sigs":
		text, err := sigs.YAMLToJSON(data)
		if err != nil {
			return nil, "", err
		}
		tree, err := orderedJSON(text)
		return tree, string(text), err
	case "apimachinery":
		text, err := k8syaml.ToJSON(data)
		if err != nil {
			return nil, "", err
		}
		tree, err := orderedJSON(text)
		return tree, string(text), err
	case "koanf":
		value, err := koanfyaml.Parser().Unmarshal(data)
		if err != nil {
			return nil, "", err
		}
		return native(value), fmt.Sprintf("%T", value), nil
	case "gypsy":
		node, err := gypsy.Parse(io.Reader(bytes.NewReader(data)))
		if err != nil {
			return nil, "", err
		}
		return gypsyTree(node), fmt.Sprintf("%T", node), nil
	case "kyaml":
		node, err := kyaml.Parse(string(data))
		if err != nil {
			return nil, "", err
		}
		tree, err := kyamlTree(node.YNode())
		return tree, "", err
	case "cue":
		file, err := cueyaml.Extract("control.yaml", data)
		if err != nil {
			return nil, "", err
		}
		tree, err := cueTree(file)
		return tree, "", err
	}
	return nil, "", fmt.Errorf("unknown lead %s", lead)
}

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: probe <lead> <control.yaml>")
		os.Exit(2)
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	tree, raw, err := run(os.Args[1], data)
	record := map[string]any{"lead": os.Args[1], "tree": tree, "raw": raw, "error": nil}
	if err != nil {
		record["error"] = err.Error()
	}
	var buffer bytes.Buffer
	encoder := json.NewEncoder(&buffer)
	encoder.SetEscapeHTML(false)
	if err := encoder.Encode(record); err != nil {
		panic(err)
	}
	os.Stdout.Write(buffer.Bytes())
}
