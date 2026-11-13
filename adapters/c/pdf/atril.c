#include <atril-document.h>
#include <glib.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "expected one local PDF path\n");
        return 2;
    }
    GError *error = NULL;
    if (!ev_init()) {
        fprintf(stderr, "Atril document initialization failed\n");
        return 3;
    }
    gchar *uri = g_filename_to_uri(argv[1], NULL, &error);
    if (uri == NULL) {
        fprintf(stderr, "%s\n", error->message);
        g_error_free(error);
        ev_shutdown();
        return 4;
    }
    EvDocument *document = ev_document_factory_get_document(uri, &error);
    if (document == NULL) {
        fprintf(stderr, "%s\n", error != NULL ? error->message : "PDF load failed");
        if (error != NULL) g_error_free(error);
        g_free(uri);
        ev_shutdown();
        return 5;
    }
    printf("{\"pages\":%d}\n", ev_document_get_n_pages(document));
    g_object_unref(document);
    g_free(uri);
    ev_shutdown();
    return 0;
}
