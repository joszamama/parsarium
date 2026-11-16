package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"sort"
	"strconv"
	"strings"
)

const packagePrefix = "github.com/go-pdfkit/extract/"
const underlyingPrefix = "\x00"

func main() {
	if len(os.Args) == 2 && os.Args[1] == "--toolchain" {
		fmt.Println(runtime.Version())
		return
	}
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run() error {
	cmd := exec.Command("/work/harness.test", "-test.run=^TestControl$", "-test.v", "-test.coverprofile=/coverage/raw.cover")
	combined, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("control replay failed: %w: %s", err, combined)
	}
	var observed map[string]any
	for _, line := range strings.Split(string(combined), "\n") {
		if payload, ok := strings.CutPrefix(line, "OBSERVED_JSON:"); ok {
			if err := json.Unmarshal([]byte(payload), &observed); err != nil {
				return err
			}
		}
	}
	if observed == nil {
		return fmt.Errorf("control replay emitted no parsed result: %s", combined)
	}
	raw, err := os.ReadFile("/coverage/raw.cover")
	if err != nil {
		return err
	}
	files := make(map[string]map[int]bool)
	scanner := bufio.NewScanner(bytes.NewReader(raw))
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.HasPrefix(line, packagePrefix) && !strings.HasPrefix(line, underlyingPrefix) {
			continue
		}
		fields := strings.Fields(line)
		if len(fields) != 3 || fields[2] == "0" {
			continue
		}
		location := fields[0]
		colon := strings.LastIndexByte(location, ':')
		if colon < 0 {
			return fmt.Errorf("bad cover location: %s", location)
		}
		filename := location[:colon]
		span := strings.Split(location[colon+1:], ",")
		if len(span) != 2 {
			return fmt.Errorf("bad cover span: %s", location)
		}
		first, err := strconv.Atoi(strings.Split(span[0], ".")[0])
		if err != nil {
			return err
		}
		last, err := strconv.Atoi(strings.Split(span[1], ".")[0])
		if err != nil {
			return err
		}
		endParts := strings.Split(span[1], ".")
		if len(endParts) != 2 {
			return fmt.Errorf("bad cover end: %s", location)
		}
		endColumn, err := strconv.Atoi(endParts[1])
		if err != nil {
			return err
		}
		if endColumn == 1 && last > first {
			last-- // Go cover block end positions are exclusive.
		}
		if first < 1 || last < first || last-first > 10000 {
			return fmt.Errorf("invalid cover span: %s", location)
		}
		if files[filename] == nil {
			files[filename] = make(map[int]bool)
		}
		for line := first; line <= last; line++ {
			files[filename][line] = true
		}
	}
	if err := scanner.Err(); err != nil {
		return err
	}
	if len(files) == 0 {
		return fmt.Errorf("no covered imaging package source")
	}
	names := make([]string, 0, len(files))
	for name := range files {
		names = append(names, name)
	}
	sort.Strings(names)
	type fileReport struct {
		Filename      string         `json:"filename"`
		Summary       map[string]any `json:"summary"`
		ExecutedLines []int          `json:"executed_lines"`
	}
	reports := make([]fileReport, 0, len(names))
	total := 0
	packageFiles := 0
	underlyingFiles := 0
	underlyingLines := 0
	for _, name := range names {
		lines := make([]int, 0, len(files[name]))
		for line := range files[name] {
			lines = append(lines, line)
		}
		sort.Ints(lines)
		if strings.HasPrefix(name, packagePrefix) {
			packageFiles++
			total += len(lines)
		} else if strings.HasPrefix(name, underlyingPrefix) {
			underlyingFiles++
			underlyingLines += len(lines)
		}
		reports = append(reports, fileReport{
			Filename:      name,
			Summary:       map[string]any{"lines": map[string]any{"covered": len(lines)}},
			ExecutedLines: lines,
		})
	}
	coverage := map[string]any{"data": []any{map[string]any{"files": reports}}}
	if packageFiles == 0 || total == 0 {
		return fmt.Errorf("missing coverage in imaging or image/png source")
	}
	summary := map[string]any{
		"control_pass":                    true,
		"output":                          observed,
		"parser_source_files":             packageFiles,
		"parser_source_lines_covered":     total,
		"underlying_source_files":         underlyingFiles,
		"underlying_source_lines_covered": underlyingLines,
		"coverage":                        "/coverage/coverage.json",
	}
	if err := writeJSON("/coverage/coverage.json", coverage); err != nil {
		return err
	}
	if err := writeJSON("/coverage/summary.json", summary); err != nil {
		return err
	}
	encoded, _ := json.Marshal(summary)
	fmt.Println(string(encoded))
	return nil
}

func writeJSON(path string, value any) error {
	data, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, append(data, '\n'), 0644)
}
