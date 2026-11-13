#include <gio/gio.h>
#include <stdio.h>

/*
 * Papers 51.1 exposes these symbols in its documented 4.0 C API. Its umbrella
 * header requires a macro claiming author contact. These signatures mirror
 * the pinned upstream headers so the adapter makes no such claim.
 */
typedef struct _PpsDocument PpsDocument;
gboolean pps_init(void);
void pps_shutdown(void);
PpsDocument *pps_document_factory_get_document(const char *uri, GError **error);
gboolean pps_document_load(PpsDocument *document, const char *uri, GError **error);
gint pps_document_get_n_pages(PpsDocument *document);

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!pps_init()) return 1;

    GError *error = NULL;
    char *uri = g_filename_to_uri(argv[1], NULL, &error);
    if (uri == NULL) {
        fprintf(stderr, "Papers URI: %s\n", error ? error->message : "unknown error");
        g_clear_error(&error);
        pps_shutdown();
        return 1;
    }

    PpsDocument *document = pps_document_factory_get_document(uri, &error);
    if (document == NULL) {
        fprintf(stderr, "Papers document factory: %s\n", error ? error->message : "unknown error");
        g_clear_error(&error);
        g_free(uri);
        pps_shutdown();
        return 1;
    }
    if (!pps_document_load(document, uri, &error)) {
        fprintf(stderr, "Papers PDF parse: %s\n", error ? error->message : "unknown error");
        g_clear_error(&error);
        g_object_unref(document);
        g_free(uri);
        pps_shutdown();
        return 1;
    }
    int pages = pps_document_get_n_pages(document);
    g_object_unref(document);
    g_free(uri);
    pps_shutdown();
    if (pages < 1) return 1;
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
