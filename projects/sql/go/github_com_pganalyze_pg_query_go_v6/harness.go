package sqlharness

import (
	"encoding/json"
	"fmt"
	"sort"
	"strconv"
	"strings"

	pg_query "github.com/pganalyze/pg_query_go/v6"
	"google.golang.org/protobuf/reflect/protoreflect"
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
	joins             int
}

// visit walks every populated message field of the libpg_query protobuf parse tree.
func (c *collector) visit(message protoreflect.Message) {
	switch node := message.Interface().(type) {
	case *pg_query.RangeVar:
		c.tables = append(c.tables, strings.ToLower(node.GetRelname()))
	case *pg_query.JoinExpr:
		c.joins++
	case *pg_query.FuncCall:
		// The last name part is the function name (an optional schema comes first).
		if names := node.GetFuncname(); len(names) > 0 {
			c.functions = append(c.functions, strings.ToLower(names[len(names)-1].GetString_().GetSval()))
		}
	case *pg_query.A_Const:
		switch {
		case node.GetIval() != nil:
			c.literals = append(c.literals, literal{"number", strconv.FormatInt(int64(node.GetIval().GetIval()), 10)})
		case node.GetFval() != nil:
			c.literals = append(c.literals, literal{"number", node.GetFval().GetFval()})
		case node.GetSval() != nil:
			c.literals = append(c.literals, literal{"string", node.GetSval().GetSval()})
		}
	}
	message.Range(func(field protoreflect.FieldDescriptor, value protoreflect.Value) bool {
		if field.Kind() != protoreflect.MessageKind && field.Kind() != protoreflect.GroupKind {
			return true
		}
		switch {
		case field.IsList():
			list := value.List()
			for index := 0; index < list.Len(); index++ {
				c.visit(list.Get(index).Message())
			}
		case field.IsMap():
		default:
			c.visit(value.Message())
		}
		return true
	})
}

func summarize(statement *pg_query.Node) map[string]any {
	c := &collector{literals: []literal{}}
	c.visit(statement.ProtoReflect())
	sort.Slice(c.literals, func(i, j int) bool {
		if c.literals[i][0] != c.literals[j][0] {
			return c.literals[i][0] < c.literals[j][0]
		}
		return c.literals[i][1] < c.literals[j][1]
	})
	if s := statement.GetSelectStmt(); s != nil {
		return map[string]any{"kind": "select", "tables": sortedUnique(c.tables), "select_items": len(s.GetTargetList()),
			"joins": c.joins, "where": s.GetWhereClause() != nil, "group_by": len(s.GetGroupClause()),
			"order_by": len(s.GetSortClause()), "functions": sortedUnique(c.functions), "literals": c.literals}
	}
	if s := statement.GetInsertStmt(); s != nil {
		rows := 0
		if values := s.GetSelectStmt().GetSelectStmt(); values != nil {
			rows = len(values.GetValuesLists())
		}
		return map[string]any{"kind": "insert", "tables": sortedUnique(c.tables), "columns": len(s.GetCols()),
			"rows": rows, "literals": c.literals}
	}
	return map[string]any{"kind": strings.ToLower(fmt.Sprintf("%T", statement.GetNode()))}
}

// Parse runs the documented pg_query.Parse (libpg_query, PostgreSQL grammar) on local SQL text.
func Parse(data []byte) (map[string]any, error) {
	if len(data) == 0 || len(data) > (1<<20) {
		return nil, fmt.Errorf("input outside harness limit")
	}
	tree, err := pg_query.Parse(string(data))
	if err != nil {
		return nil, err
	}
	summaries := []map[string]any{}
	for _, raw := range tree.GetStmts() {
		summaries = append(summaries, summarize(raw.GetStmt()))
	}
	return map[string]any{"statement_count": len(summaries), "statements": summaries}, nil
}

// Encode gives the summary as compact JSON with sorted object keys.
func Encode(value map[string]any) string {
	data, _ := json.Marshal(value)
	return string(data)
}
