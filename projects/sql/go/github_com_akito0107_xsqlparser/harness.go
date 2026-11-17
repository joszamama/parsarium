package sqlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/akito0107/xsqlparser"
	"github.com/akito0107/xsqlparser/dialect"
	"github.com/akito0107/xsqlparser/sqlast"
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

func lastIdent(name *sqlast.ObjectName) string {
	if name == nil || len(name.Idents) == 0 {
		return ""
	}
	return strings.ToLower(name.Idents[len(name.Idents)-1].Value)
}

func summarize(statement sqlast.Stmt) map[string]any {
	tables, functions := []string{}, []string{}
	literals := []literal{}
	joins := 0
	sqlast.Inspect(statement, func(node sqlast.Node) bool {
		switch n := node.(type) {
		case *sqlast.Table:
			tables = append(tables, lastIdent(n.Name))
		case *sqlast.QualifiedJoin, *sqlast.NaturalJoin, *sqlast.CrossJoin:
			joins++
		case *sqlast.Function:
			functions = append(functions, lastIdent(n.Name))
		case *sqlast.LongValue:
			// The parser stores numbers as int64/float64; formatted back they equal the control text.
			literals = append(literals, literal{"number", strconv.FormatInt(n.Long, 10)})
		case *sqlast.DoubleValue:
			literals = append(literals, literal{"number", strconv.FormatFloat(n.Double, 'f', -1, 64)})
		case *sqlast.SingleQuotedString:
			literals = append(literals, literal{"string", n.String})
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
	case *sqlast.QueryStmt:
		if body, ok := s.Body.(*sqlast.SQLSelect); ok {
			return map[string]any{"kind": "select", "tables": sortedUnique(tables), "select_items": len(body.Projection),
				"joins": joins, "where": body.WhereClause != nil, "group_by": len(body.GroupByClause),
				"order_by": len(s.OrderBy), "functions": sortedUnique(functions), "literals": literals}
		}
	case *sqlast.InsertStmt:
		// The insert target is an ObjectName field, not a Table node.
		tables = append(tables, lastIdent(s.TableName))
		rows := 0
		if source, ok := s.Source.(*sqlast.ConstructorSource); ok {
			rows = len(source.Rows)
		}
		return map[string]any{"kind": "insert", "tables": sortedUnique(tables), "columns": len(s.Columns),
			"rows": rows, "literals": literals}
	}
	return map[string]any{"kind": strings.ToLower(strings.TrimPrefix(fmt.Sprintf("%T", statement), "*sqlast."))}
}

// Parse runs the documented xsqlparser.NewParser(reader, &dialect.GenericSQLDialect{}).ParseSQL on local SQL text.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	parser, err := xsqlparser.NewParser(bytes.NewReader(data), &dialect.GenericSQLDialect{})
	if err != nil {
		return nil, err
	}
	statements, err := parser.ParseSQL()
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
