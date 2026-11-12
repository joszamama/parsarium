#include <poppler.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    gchar *contents = NULL;
    gsize length = 0;
    GError *error = NULL;
    if (!g_file_get_contents(argv[1], &contents, &length, &error)) {
        g_clear_error(&error);
        return 2;
    }
    GBytes *bytes = g_bytes_new_take(contents, length);
    PopplerDocument *document = poppler_document_new_from_bytes(bytes, NULL, &error);
    g_bytes_unref(bytes);
    if (document == NULL) {
        g_clear_error(&error);
        return 3;
    }
    int pages = poppler_document_get_n_pages(document);
    g_object_unref(document);
    if (pages <= 0) return 4;
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
