// Extract one parser branch from a verified, format-specific Go adapter.
// This keeps each container's compiler and coverage instrumentation focused on
// the selected package, while preserving the adapter's observed parse API.
package main

import (
	"bytes"
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"os"
	"path"
	"strconv"
	"strings"
)

func main() {
	if len(os.Args) == 5 && os.Args[1] == "--" { os.Args = append(os.Args[:1], os.Args[2:]...) }
	if len(os.Args) != 4 {
		panic("usage: go run slice_go_adapter.go SOURCE PACKAGE DESTINATION")
	}
	source, target, destination := os.Args[1], os.Args[2], os.Args[3]
	fset := token.NewFileSet()
	file, err := parser.ParseFile(fset, source, nil, parser.ParseComments)
	if err != nil { panic(err) }
	found := false
	hasRun := false
	for _, decl := range file.Decls {
		if fn, ok := decl.(*ast.FuncDecl); ok && fn.Name.Name == "run" { hasRun = true }
	}
	for _, decl := range file.Decls {
		fn, ok := decl.(*ast.FuncDecl)
		if !ok || (hasRun && fn.Name.Name != "run") || (!hasRun && fn.Name.Name != "main") { continue }
		ast.Inspect(fn.Body, func(node ast.Node) bool {
			sw, ok := node.(*ast.SwitchStmt)
			if !ok { return true }
			name, ok := sw.Tag.(*ast.Ident)
			if !ok || name.Name != "name" { return true }
			kept := []ast.Stmt{}
			for _, statement := range sw.Body.List {
				clause := statement.(*ast.CaseClause)
				if clause.List == nil { kept = append(kept, clause); continue }
				for _, candidate := range clause.List {
					literal, ok := candidate.(*ast.BasicLit)
					if !ok || literal.Kind != token.STRING { continue }
					value, err := strconv.Unquote(literal.Value)
					if err == nil && value == target {
						clause.List = []ast.Expr{literal}
						kept = append(kept, clause)
						found = true
						break
					}
				}
			}
			sw.Body.List = kept
			return true
		})
	}
	if !found { panic(fmt.Sprintf("no adapter case for %q", target)) }

	used := map[string]bool{}
	ast.Inspect(file, func(node ast.Node) bool {
		selector, ok := node.(*ast.SelectorExpr)
		if ok {
			if ident, ok := selector.X.(*ast.Ident); ok { used[ident.Name] = true }
		}
		return true
	})
	for _, decl := range file.Decls {
		group, ok := decl.(*ast.GenDecl)
		if !ok || group.Tok != token.IMPORT { continue }
		kept := []ast.Spec{}
		for _, spec := range group.Specs {
			item := spec.(*ast.ImportSpec)
			value, err := strconv.Unquote(item.Path.Value)
			if err != nil { panic(err) }
			name := path.Base(value)
			if item.Name != nil { name = item.Name.Name }
			if (name == "_" && value == target) || name == "." || used[name] { kept = append(kept, item) }
		}
		group.Specs = kept
	}
	var out bytes.Buffer
	if err := format.Node(&out, fset, file); err != nil { panic(err) }
	if strings.TrimSpace(out.String()) == "" { panic("empty extracted adapter") }
	if err := os.WriteFile(destination, out.Bytes(), 0644); err != nil { panic(err) }
}
