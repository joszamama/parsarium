/* tree-sitter-sql: ts_parser_parse_string with tree_sitter_sql() builds the concrete syntax tree
 * of local SQL text. The replay rejects trees with ERROR or MISSING nodes and prints the named
 * nodes as JSON (type, field name, and source text for nodes without named children);
 * summarize.py reads the oracle fields from that tree. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <tree_sitter/api.h>

const TSLanguage *tree_sitter_sql(void);

/* Copies local bytes into a NUL-terminated string; rejects embedded NULs and oversize input. */
static char *text_from(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20) || memchr(data, 0, size)) return NULL;
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size);
    text[size] = '\0';
    return text;
}

static TSTree *parse_text(TSParser *parser, const char *text, size_t size) {
    if (!ts_parser_set_language(parser, tree_sitter_sql())) return NULL;
    return ts_parser_parse_string(parser, NULL, text, (uint32_t)size);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char *text = text_from(data, size);
    if (!text) return 0;
    TSParser *parser = ts_parser_new();
    TSTree *tree = parse_text(parser, text, size);
    if (tree) ts_tree_delete(tree);
    ts_parser_delete(parser);
    free(text);
    return 0;
}

#ifndef PARSARIUM_FUZZER
static void print_string(const char *start, size_t length) {
    fputc('"', stdout);
    for (size_t i = 0; i < length; i++) {
        unsigned char c = (unsigned char)start[i];
        if (c == '"' || c == '\\') { fputc('\\', stdout); fputc(c, stdout); }
        else if (c < 0x20) printf("\\u%04x", c);
        else fputc(c, stdout);
    }
    fputc('"', stdout);
}

/* Prints the named node under the cursor and, recursively, its named descendants. */
static void print_node(TSTreeCursor *cursor, const char *text) {
    TSNode node = ts_tree_cursor_current_node(cursor);
    const char *field = ts_tree_cursor_current_field_name(cursor);
    printf("{\"type\":\"%s\",\"field\":", ts_node_type(node));
    if (field) printf("\"%s\"", field); else fputs("null", stdout);
    if (ts_node_named_child_count(node) == 0) {
        uint32_t start = ts_node_start_byte(node), end = ts_node_end_byte(node);
        fputs(",\"text\":", stdout);
        print_string(text + start, end - start);
    }
    fputs(",\"children\":[", stdout);
    int first = 1;
    if (ts_tree_cursor_goto_first_child(cursor)) {
        do {
            if (!ts_node_is_named(ts_tree_cursor_current_node(cursor))) continue;
            if (!first) fputc(',', stdout);
            first = 0;
            print_node(cursor, text);
        } while (ts_tree_cursor_goto_next_sibling(cursor));
        ts_tree_cursor_goto_parent(cursor);
    }
    fputs("]}", stdout);
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc((1u << 20) + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, (1u << 20) + 1, file);
    fclose(file);
    char *text = text_from(data, size);
    free(data);
    if (!text) return 4;
    TSParser *parser = ts_parser_new();
    TSTree *tree = parse_text(parser, text, size);
    if (!tree) { ts_parser_delete(parser); free(text); return 5; }
    TSNode root = ts_tree_root_node(tree);
    int status = 0;
    if (ts_node_has_error(root)) {
        fputs("parse error: tree contains ERROR or MISSING nodes\n", stderr);
        status = 5;
    } else {
        TSTreeCursor cursor = ts_tree_cursor_new(root);
        print_node(&cursor, text);
        fputc('\n', stdout);
        ts_tree_cursor_delete(&cursor);
    }
    ts_tree_delete(tree);
    ts_parser_delete(parser);
    free(text);
    return status;
}
#endif
