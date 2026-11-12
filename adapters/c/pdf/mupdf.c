#include <mupdf/fitz.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    fz_context *context = fz_new_context(NULL, NULL, FZ_STORE_UNLIMITED);
    if (context == NULL) return 2;
    fz_register_document_handlers(context);
    fz_document *document = fz_open_document(context, argv[1]);
    if (document == NULL) {
        fz_drop_context(context);
        return 3;
    }
    int pages = fz_count_pages(context, document);
    fz_drop_document(context, document);
    fz_drop_context(context);
    if (pages <= 0) return 4;
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
