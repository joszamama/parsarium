#include <gsf/gsf.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    gsf_init();
    GError *error = NULL;
    GsfInput *input = gsf_input_stdio_new(argv[1], &error);
    if (!input) { if (error) g_error_free(error); gsf_shutdown(); return 1; }
    GsfInfile *archive = gsf_infile_zip_new(input, &error);
    if (!archive) {
        if (error) g_error_free(error);
        g_object_unref(input); gsf_shutdown(); return 1;
    }
    int entries = gsf_infile_num_children(archive);
    const char *name = entries > 0 ? gsf_infile_name_by_index(archive, 0) : NULL;
    GsfInput *entry = entries > 0 ? gsf_infile_child_by_index(archive, 0) : NULL;
    if (!name || !entry || gsf_input_size(entry) > 4096) {
        if (entry) g_object_unref(entry);
        g_object_unref(archive); g_object_unref(input); gsf_shutdown(); return 1;
    }
    size_t size = (size_t) gsf_input_size(entry);
    const unsigned char *contents = gsf_input_read(entry, size, NULL);
    if (!contents) { g_object_unref(entry); g_object_unref(archive); g_object_unref(input); gsf_shutdown(); return 1; }
    zip_report((size_t) entries, name, contents, size);
    g_object_unref(entry);
    g_object_unref(archive);
    g_object_unref(input);
    gsf_shutdown();
    return 0;
}
