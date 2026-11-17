package sqlharness

import (
	"bytes"
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	sql "github.com/rqlite/sql"
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

// collector is an rqlite sql.Visitor for base tables, joins, called functions and literals.
type collector struct {
	tables, functions []string
	literals          []literal
	joins             int
}

func (c *collector) Visit(node sql.Node) (sql.Visitor, sql.Node, error) {
	switch n := node.(type) {
	case *sql.QualifiedTableName:
		c.tables = append(c.tables, strings.ToLower(sql.IdentName(n.Name)))
	case *sql.JoinClause:
		// A comma between FROM sources is also a JoinClause; only JOIN keywords count.
		if n.Operator != nil && !n.Operator.Join.IsValid() {
			break
		}
		c.joins++
	case *sql.Call:
		c.functions = append(c.functions, strings.ToLower(sql.IdentName(n.Name)))
	case *sql.NumberLit:
		c.literals = append(c.literals, literal{"number", n.Value})
	case *sql.StringLit:
		c.literals = append(c.literals, literal{"string", n.Value})
	}
	return c, node, nil
}

func (c *collector) VisitEnd(node sql.Node) (sql.Node, error) { return node, nil }

func summarize(statement sql.Statement) (map[string]any, error) {
	c := &collector{literals: []literal{}}
	if _, err := sql.Walk(c, statement); err != nil {
		return nil, err
	}
	sort.Slice(c.literals, func(i, j int) bool {
		if c.literals[i][0] != c.literals[j][0] {
			return c.literals[i][0] < c.literals[j][0]
		}
		return c.literals[i][1] < c.literals[j][1]
	})
	switch s := statement.(type) {
	case *sql.SelectStatement:
		return map[string]any{"kind": "select", "tables": sortedUnique(c.tables), "select_items": len(s.Columns),
			"joins": c.joins, "where": s.WhereExpr != nil, "group_by": len(s.GroupByExprs),
			"order_by": len(s.OrderingTerms), "functions": sortedUnique(c.functions), "literals": c.literals}, nil
	case *sql.InsertStatement:
		// The insert target is an Ident field, not a QualifiedTableName node.
		tables := append(c.tables, strings.ToLower(sql.IdentName(s.Table)))
		return map[string]any{"kind": "insert", "tables": sortedUnique(tables), "columns": len(s.Columns),
			"rows": len(s.ValueLists), "literals": c.literals}, nil
	}
	return map[string]any{"kind": strings.ToLower(strings.TrimPrefix(fmt.Sprintf("%T", statement), "*sql."))}, nil
}

// Parse reads local SQL text with sql.NewParser(reader).ParseStatements and summarizes each statement.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	statements, err := sql.NewParser(bytes.NewReader(data)).ParseStatements()
	if err != nil {
		return nil, err
	}
	summaries := []map[string]any{}
	for _, statement := range statements {
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
