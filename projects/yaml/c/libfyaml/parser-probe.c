/* Parser-only probe: fy_document_build_from_string on the local bytes, then destroy; no traversal or printing. */
#include <stdio.h>

#include <libfyaml.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    static const struct fy_parse_cfg cfg = {
        .flags = FYPCF_QUIET | FYPCF_RESOLVE_DOCUMENT | FYPCF_DEFAULT_VERSION_1_2 | FYPCF_JSON_NONE,
    };
    struct fy_document *document = fy_document_build_from_string(&cfg, data, size);
    if (!document) return 1;
    fy_document_destroy(document);
    return 0;
}
