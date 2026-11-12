#include <mupdf/fitz.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    fz_context* context = fz_new_context(nullptr, nullptr, FZ_STORE_UNLIMITED);
    if (!context) return 2;
    fz_register_document_handlers(context);
    fz_document* pdf = fz_open_document(context, argv[1]);
    if (!pdf) return 3;
    const int pages = fz_count_pages(context, pdf);
    std::cout << "{\"pages\":" << pages << "}\n";
    fz_drop_document(context, pdf);
    fz_drop_context(context);
}
