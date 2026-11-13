#include <mupdf/fitz.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    fz_context *context = fz_new_context(NULL, NULL, FZ_STORE_UNLIMITED);
    if (context == NULL) return 1;
    fz_register_document_handlers(context);
    fz_document *document = fz_open_document(context, argv[1]);
    if (document == NULL || fz_count_pages(context, document) != 1) return 1;
    fz_page *page = fz_load_page(context, document, 0);
    if (page == NULL) return 1;
    fz_pixmap *image = fz_new_pixmap_from_page(context, page, fz_identity,
                                                fz_device_rgb(context), 0);
    if (image == NULL || image->w != 2 || image->h != 1 || image->n != 3) return 1;
    unsigned char *pixel = image->samples;
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           image->w, image->h, pixel[0], pixel[1], pixel[2],
           pixel[3], pixel[4], pixel[5]);
    fz_drop_pixmap(context, image);
    fz_drop_page(context, page);
    fz_drop_document(context, document);
    fz_drop_context(context);
    return 0;
}
