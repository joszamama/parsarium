package sqlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/pingcap/tidb/pkg/parser"
	"github.com/pingcap/tidb/pkg/parser/ast"
	"github.com/pingcap/tidb/pkg/parser/test_driver"
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

// collector walks the TiDB AST for base tables, called functions and literal values.
type collector struct {
	tables, functions []string
	literals          []literal
	synthetic         map[ast.Node]bool
}

func (c *collector) Enter(node ast.Node) (ast.Node, bool) {
	switch n := node.(type) {
	case *ast.TableName:
		c.tables = append(c.tables, n.Name.L)
	case *ast.AggregateFuncExpr:
		c.functions = append(c.functions, strings.ToLower(n.F))
		// parser.y turns COUNT(*) into COUNT with one synthetic ValueExpr(1) that has
		// no source position; it is not a literal of the statement text.
		if strings.EqualFold(n.F, "count") && len(n.Args) == 1 {
			if value, ok := n.Args[0].(*test_driver.ValueExpr); ok && value.OriginTextPosition() == 0 {
				c.synthetic[value] = true
			}
		}
	case *ast.FuncCallExpr:
		c.functions = append(c.functions, n.FnName.L)
	case *test_driver.ValueExpr:
		if c.synthetic[n] {
			break
		}
		switch n.Kind() {
		case test_driver.KindString:
			c.literals = append(c.literals, literal{"string", n.GetString()})
		case test_driver.KindInt64:
			c.literals = append(c.literals, literal{"number", strconv.FormatInt(n.GetInt64(), 10)})
		case test_driver.KindUint64:
			c.literals = append(c.literals, literal{"number", strconv.FormatUint(n.GetUint64(), 10)})
		case test_driver.KindMysqlDecimal:
			c.literals = append(c.literals, literal{"number", n.GetMysqlDecimal().String()})
		}
	}
	return node, false
}

func (c *collector) Leave(node ast.Node) (ast.Node, bool) { return node, true }

func countJoins(node ast.ResultSetNode) int {
	join, ok := node.(*ast.Join)
	if !ok || join == nil {
		return 0
	}
	joins := countJoins(join.Left) + countJoins(join.Right)
	if join.Right != nil {
		joins++
	}
	return joins
}

func summarize(statement ast.StmtNode) map[string]any {
	c := &collector{synthetic: map[ast.Node]bool{}}
	statement.Accept(c)
	sort.Slice(c.literals, func(i, j int) bool {
		if c.literals[i][0] != c.literals[j][0] {
			return c.literals[i][0] < c.literals[j][0]
		}
		return c.literals[i][1] < c.literals[j][1]
	})
	tables, functions := sortedUnique(c.tables), sortedUnique(c.functions)
	switch s := statement.(type) {
	case *ast.SelectStmt:
		selectItems, joins, groupBy, orderBy := 0, 0, 0, 0
		if s.Fields != nil {
			selectItems = len(s.Fields.Fields)
		}
		if s.From != nil {
			joins = countJoins(s.From.TableRefs)
		}
		if s.GroupBy != nil {
			groupBy = len(s.GroupBy.Items)
		}
		if s.OrderBy != nil {
			orderBy = len(s.OrderBy.Items)
		}
		return map[string]any{"kind": "select", "tables": tables, "select_items": selectItems,
			"joins": joins, "where": s.Where != nil, "group_by": groupBy,
			"order_by": orderBy, "functions": functions, "literals": c.literals}
	case *ast.InsertStmt:
		return map[string]any{"kind": "insert", "tables": tables, "columns": len(s.Columns),
			"rows": len(s.Lists), "literals": c.literals}
	}
	return map[string]any{"kind": strings.ToLower(strings.TrimPrefix(fmt.Sprintf("%T", statement), "*ast."))}
}

// Parse runs the documented parser.New().Parse on local SQL text (default charset and collation).
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	statements, _, err := parser.New().Parse(string(data), "", "")
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
