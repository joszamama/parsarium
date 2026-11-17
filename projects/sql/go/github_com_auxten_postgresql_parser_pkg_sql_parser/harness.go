package sqlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	"github.com/auxten/postgresql-parser/pkg/sql/parser"
	"github.com/auxten/postgresql-parser/pkg/sql/sem/tree"
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

type collector struct {
	tables, functions []string
	literals          []literal
}

// expr collects function names and literal values from one expression tree with tree.SimpleVisit.
func (c *collector) expr(expression tree.Expr) error {
	if expression == nil {
		return nil
	}
	_, err := tree.SimpleVisit(expression, func(node tree.Expr) (bool, tree.Expr, error) {
		switch n := node.(type) {
		case *tree.FuncExpr:
			c.functions = append(c.functions, strings.ToLower(n.Func.String()))
		case *tree.NumVal:
			c.literals = append(c.literals, literal{"number", n.OrigString()})
		case *tree.StrVal:
			c.literals = append(c.literals, literal{"string", n.RawString()})
		}
		return true, node, nil
	})
	return err
}

// tableName returns the base-table name of a table reference, or "" for other table expressions.
func tableName(expression tree.TableExpr) string {
	switch n := expression.(type) {
	case *tree.TableName:
		return strings.ToLower(n.Table())
	case *tree.UnresolvedObjectName:
		name := n.ToTableName()
		return strings.ToLower(name.Table())
	case *tree.AliasedTableExpr:
		return tableName(n.Expr)
	}
	return ""
}

// tableExpr records base tables, counts join operators and visits join conditions.
func (c *collector) tableExpr(expression tree.TableExpr) (int, error) {
	switch n := expression.(type) {
	case *tree.JoinTableExpr:
		left, err := c.tableExpr(n.Left)
		if err != nil {
			return 0, err
		}
		right, err := c.tableExpr(n.Right)
		if err != nil {
			return 0, err
		}
		if on, ok := n.Cond.(*tree.OnJoinCond); ok {
			if err := c.expr(on.Expr); err != nil {
				return 0, err
			}
		}
		return left + right + 1, nil
	case *tree.ParenTableExpr:
		return c.tableExpr(n.Expr)
	}
	if name := tableName(expression); name != "" {
		c.tables = append(c.tables, name)
	}
	return 0, nil
}

func (c *collector) sortedLiterals() []literal {
	sort.Slice(c.literals, func(i, j int) bool {
		if c.literals[i][0] != c.literals[j][0] {
			return c.literals[i][0] < c.literals[j][0]
		}
		return c.literals[i][1] < c.literals[j][1]
	})
	return c.literals
}

func summarize(statement tree.Statement) (map[string]any, error) {
	c := &collector{literals: []literal{}}
	switch s := statement.(type) {
	case *tree.Select:
		clause, ok := s.Select.(*tree.SelectClause)
		if !ok {
			return map[string]any{"kind": "select"}, nil
		}
		for _, item := range clause.Exprs {
			if err := c.expr(item.Expr); err != nil {
				return nil, err
			}
		}
		joins := 0
		for _, table := range clause.From.Tables {
			count, err := c.tableExpr(table)
			if err != nil {
				return nil, err
			}
			joins += count
		}
		if clause.Where != nil {
			if err := c.expr(clause.Where.Expr); err != nil {
				return nil, err
			}
		}
		for _, group := range clause.GroupBy {
			if err := c.expr(group); err != nil {
				return nil, err
			}
		}
		for _, order := range s.OrderBy {
			if err := c.expr(order.Expr); err != nil {
				return nil, err
			}
		}
		return map[string]any{"kind": "select", "tables": sortedUnique(c.tables), "select_items": len(clause.Exprs),
			"joins": joins, "where": clause.Where != nil, "group_by": len(clause.GroupBy),
			"order_by": len(s.OrderBy), "functions": sortedUnique(c.functions), "literals": c.sortedLiterals()}, nil
	case *tree.Insert:
		if name := tableName(s.Table); name != "" {
			c.tables = append(c.tables, name)
		}
		rows := 0
		if s.Rows != nil {
			if values, ok := s.Rows.Select.(*tree.ValuesClause); ok {
				rows = len(values.Rows)
				for _, row := range values.Rows {
					for _, value := range row {
						if err := c.expr(value); err != nil {
							return nil, err
						}
					}
				}
			}
		}
		return map[string]any{"kind": "insert", "tables": sortedUnique(c.tables), "columns": len(s.Columns),
			"rows": rows, "literals": c.sortedLiterals()}, nil
	}
	return map[string]any{"kind": strings.ToLower(statement.StatementTag())}, nil
}

// Parse runs the documented parser.Parse on local SQL text and summarizes each statement's AST.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	statements, err := parser.Parse(string(data))
	if err != nil {
		return nil, err
	}
	summaries := []map[string]any{}
	for _, statement := range statements {
		summary, err := summarize(statement.AST)
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
