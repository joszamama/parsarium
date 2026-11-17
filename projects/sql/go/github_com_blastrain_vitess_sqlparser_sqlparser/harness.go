package sqlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	"github.com/blastrain/vitess-sqlparser/sqlparser"
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

// walkSummary collects base tables, function names and literals from the AST.
func walkSummary(node sqlparser.SQLNode) (tables, functions []string, literals []literal, err error) {
	err = sqlparser.Walk(func(node sqlparser.SQLNode) (bool, error) {
		switch n := node.(type) {
		case *sqlparser.AliasedTableExpr:
			// Base tables only; column qualifiers are also TableName values.
			if name, ok := n.Expr.(sqlparser.TableName); ok && !name.Name.IsEmpty() {
				tables = append(tables, strings.ToLower(name.Name.String()))
			}
		case *sqlparser.FuncExpr:
			functions = append(functions, n.Name.Lowered())
		case *sqlparser.SQLVal:
			switch n.Type {
			case sqlparser.StrVal:
				literals = append(literals, literal{"string", string(n.Val)})
			case sqlparser.IntVal, sqlparser.FloatVal:
				literals = append(literals, literal{"number", string(n.Val)})
			}
		}
		return true, nil
	}, node)
	sort.Slice(literals, func(i, j int) bool {
		if literals[i][0] != literals[j][0] {
			return literals[i][0] < literals[j][0]
		}
		return literals[i][1] < literals[j][1]
	})
	return tables, functions, literals, err
}

func countJoins(expressions []sqlparser.TableExpr) int {
	joins := 0
	for _, expression := range expressions {
		if join, ok := expression.(*sqlparser.JoinTableExpr); ok {
			joins += 1 + countJoins([]sqlparser.TableExpr{join.LeftExpr, join.RightExpr})
		}
	}
	return joins
}

func summarize(statement sqlparser.Statement) (map[string]any, error) {
	tables, functions, literals, err := walkSummary(statement)
	if err != nil {
		return nil, err
	}
	switch s := statement.(type) {
	case *sqlparser.Select:
		return map[string]any{"kind": "select", "tables": sortedUnique(tables), "select_items": len(s.SelectExprs),
			"joins": countJoins(s.From), "where": s.Where != nil, "group_by": len(s.GroupBy),
			"order_by": len(s.OrderBy), "functions": sortedUnique(functions), "literals": literals}, nil
	case *sqlparser.Insert:
		// The insert target is a plain TableName field in this vitess generation.
		tables = append(tables, strings.ToLower(s.Table.Name.String()))
		rows := 0
		if values, ok := s.Rows.(sqlparser.Values); ok {
			rows = len(values)
		}
		return map[string]any{"kind": "insert", "tables": sortedUnique(tables), "columns": len(s.Columns),
			"rows": rows, "literals": literals}, nil
	}
	return map[string]any{"kind": strings.ToLower(strings.TrimPrefix(fmt.Sprintf("%T", statement), "*sqlparser."))}, nil
}

// Parse passes the whole local SQL text to sqlparser.Parse, which returns one Statement
// (the package has no statement splitter; the grammar accepts the trailing semicolon).
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	statement, err := sqlparser.Parse(string(data))
	if err != nil {
		return nil, err
	}
	summary, err := summarize(statement)
	if err != nil {
		return nil, err
	}
	return map[string]any{"statement_count": 1, "statements": []map[string]any{summary}}, nil
}

// Encode gives the summary as compact JSON with sorted object keys.
func Encode(value map[string]any) string {
	data, _ := json.Marshal(value)
	return string(data)
}
