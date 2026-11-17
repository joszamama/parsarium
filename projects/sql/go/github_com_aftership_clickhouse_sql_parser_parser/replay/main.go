package main

import (
	"fmt"
	"os"

	sqlharness "parsarium.local/sql-clickhouse-sql-parser-harness"
)

// Prints the AST summary of one local SQL file as JSON.
func main() {
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	summary, err := sqlharness.Parse(data)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(sqlharness.Encode(summary))
}
