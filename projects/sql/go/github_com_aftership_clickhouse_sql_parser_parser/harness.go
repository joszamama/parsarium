package sqlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	clickhouse "github.com/AfterShip/clickhouse-sql-parser/parser"
)

type literal = [2]string

func sortedUnique(values []string) []string {
	seen := map[string]bool{}
	out := []string{}
	for _, value := range values {
		if !seen[value] {
			seen[value] = true
			out = append(out, value)
		}
	}
	sort.Strings(out)
	return out
}

func summarize(statement clickhouse.Expr) map[string]any {
	tables, functions := []string{}, []string{}
	literals := []literal{}
	joins := 0
	// clickhouse.Walk visits every AST node; column references are Path/Ident nodes,
	// so TableIdentifier nodes are exactly the referenced base tables.
	clickhouse.Walk(statement, func(node clickhouse.Expr) bool {
		switch n := node.(type) {
		case *clickhouse.TableIdentifier:
			if n.Table != nil {
				tables = append(tables, strings.ToLower(n.Table.Name))
			}
		case *clickhouse.JoinExpr:
			// Each joined table carries its join operator as modifiers, e.g. ["INNER" "JOIN"].
			for _, modifier := range n.Modifiers {
				if strings.EqualFold(modifier, "JOIN") {
					joins++
					break
				}
			}
		case *clickhouse.FunctionExpr:
			if n.Name != nil {
				functions = append(functions, strings.ToLower(n.Name.Name))
			}
		case *clickhouse.NumberLiteral:
			literals = append(literals, literal{"number", n.Literal})
		case *clickhouse.StringLiteral:
			literals = append(literals, literal{"string", n.Literal})
		}
		return true
	})
	sort.Slice(literals, func(i, j int) bool {
		if literals[i][0] != literals[j][0] {
			return literals[i][0] < literals[j][0]
		}
		return literals[i][1] < literals[j][1]
	})
	switch s := statement.(type) {
	case *clickhouse.SelectQuery:
		groupBy, orderBy := 0, 0
		if s.GroupBy != nil {
			if list, ok := s.GroupBy.Expr.(*clickhouse.ColumnExprList); ok {
				groupBy = len(list.Items)
			}
		}
		if s.OrderBy != nil {
			orderBy = len(s.OrderBy.Items)
		}
		return map[string]any{"kind": "select", "tables": sortedUnique(tables), "select_items": len(s.SelectItems),
			"joins": joins, "where": s.Where != nil, "group_by": groupBy,
			"order_by": orderBy, "functions": sortedUnique(functions), "literals": literals}
	case *clickhouse.InsertStmt:
		columns := 0
		if s.ColumnNames != nil {
			columns = len(s.ColumnNames.ColumnNames)
		}
		return map[string]any{"kind": "insert", "tables": sortedUnique(tables), "columns": columns,
			"rows": len(s.Values), "literals": literals}
	}
	return map[string]any{"kind": strings.ToLower(strings.TrimPrefix(fmt.Sprintf("%T", statement), "*parser."))}
}

// Parse runs the documented clickhouse.NewParser(text).ParseStmts on local SQL text.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	statements, err := clickhouse.NewParser(string(data)).ParseStmts()
	if err != nil {
		return nil, err
	}
	summaries := []map[string]any{}
	for _, statement := range statements {
		summaries = append(summaries, summarize(statement))
	}
	return map[string]any{"statement_count": len(summaries), "statements": summaries}, nil
}

// Encode gives the summary as compact JSON with sorted object keys.
func Encode(value map[string]any) string {
	data, _ := json.Marshal(value)
	return string(data)
}
