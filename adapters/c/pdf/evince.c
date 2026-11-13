#include <evince-document.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!ev_init()) return 1;
    GFile *file = g_file_new_for_path(argv[1]);
    GError *error = NULL;
    EvDocument *document = ev_document_factory_get_document_for_gfile(
        file, EV_DOCUMENT_LOAD_FLAG_NONE, NULL, &error);
    g_object_unref(file);
    if (document == NULL) {
        fprintf(stderr, "Evince PDF load: %s\n", error ? error->message : "unknown error");
        g_clear_error(&error);
        ev_shutdown();
        return 1;
    }
    int pages = ev_document_get_n_pages(document);
    g_object_unref(document);
    ev_shutdown();
    if (pages < 1) return 1;
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
