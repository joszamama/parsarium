/* Parser-only probe: ts_parser_parse_string with tree_sitter_sql() on the local bytes, then free;
 * no printing. Exit status 1 when the tree contains ERROR or MISSING nodes. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <tree_sitter/api.h>

const TSLanguage *tree_sitter_sql(void);

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[(1u << 20) + 1];
    size_t size = fread(data, 1, 1u << 20, file);
    fclose(file);
    if (size == 0 || size == (1u << 20) || memchr(data, 0, size)) return 2;
    data[size] = '\0';
    TSParser *parser = ts_parser_new();
    if (!ts_parser_set_language(parser, tree_sitter_sql())) { ts_parser_delete(parser); return 2; }
    TSTree *tree = ts_parser_parse_string(parser, NULL, data, (uint32_t)size);
    int status = !tree || ts_node_has_error(ts_tree_root_node(tree)) ? 1 : 0;
    if (tree) ts_tree_delete(tree);
    ts_parser_delete(parser);
    return status;
}
