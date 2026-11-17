package sqlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	"vitess.io/vitess/go/vt/sqlparser"
)

// One parser with the library's default MySQL server version, created once.
var parser, parserErr = sqlparser.New(sqlparser.Options{})

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

// walkSummary collects tables, function names and literals from the vitess AST.
func walkSummary(node sqlparser.SQLNode) (tables, functions []string, literals []literal, err error) {
	err = sqlparser.Walk(func(node sqlparser.SQLNode) (bool, error) {
		switch n := node.(type) {
		case *sqlparser.AliasedTableExpr:
			// Base tables only; column qualifiers are also TableName values.
			if name, ok := n.Expr.(sqlparser.TableName); ok && !name.Name.IsEmpty() {
				tables = append(tables, strings.ToLower(name.Name.String()))
			}
		case sqlparser.AggrFunc:
			functions = append(functions, strings.ToLower(n.AggrName()))
		case *sqlparser.FuncExpr:
			functions = append(functions, n.Name.Lowered())
		case *sqlparser.Literal:
			switch n.Type {
			case sqlparser.StrVal:
				literals = append(literals, literal{"string", n.Val})
			case sqlparser.IntVal, sqlparser.DecimalVal, sqlparser.FloatVal:
				literals = append(literals, literal{"number", n.Val})
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
	return sortedUnique(tables), sortedUnique(functions), literals, err
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
		groupBy := 0
		if s.GroupBy != nil {
			groupBy = len(s.GroupBy.Exprs)
		}
		selectItems := 0
		if s.SelectExprs != nil {
			selectItems = len(s.SelectExprs.Exprs)
		}
		return map[string]any{"kind": "select", "tables": tables, "select_items": selectItems,
			"joins": countJoins(s.From), "where": s.Where != nil, "group_by": groupBy,
			"order_by": len(s.OrderBy), "functions": functions, "literals": literals}, nil
	case *sqlparser.Insert:
		rows := 0
		if values, ok := s.Rows.(sqlparser.Values); ok {
			rows = len(values)
		}
		return map[string]any{"kind": "insert", "tables": tables, "columns": len(s.Columns),
			"rows": rows, "literals": literals}, nil
	}
	return map[string]any{"kind": strings.ToLower(strings.TrimPrefix(fmt.Sprintf("%T", statement), "*sqlparser."))}, nil
}

// Parse splits local SQL text into statements with vitess's own splitter and parses each one.
func Parse(data []byte) (map[string]any, error) {
	if parserErr != nil {
		return nil, parserErr
	}
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	pieces, err := parser.SplitStatementToPieces(string(data))
	if err != nil {
		return nil, err
	}
	summaries := []map[string]any{}
	for _, piece := range pieces {
		if strings.TrimSpace(piece) == "" {
			continue
		}
		statement, err := parser.Parse(piece)
		if err != nil {
			return nil, err
		}
		summary, err := summarize(statement)
		if err != nil {
			return nil, err
		}
		summaries = append(summaries, summary)
	}
	return map[string]any{"statement_count": len(summaries), "statements": summaries}, nil
}

// Encode gives the summary as compact JSON with sorted object keys.
func Encode(value map[string]any) string {
	data, _ := json.Marshal(value)
	return string(data)
}
