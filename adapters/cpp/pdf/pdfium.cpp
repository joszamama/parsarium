#include <fpdfview.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    FPDF_InitLibrary();
    FPDF_DOCUMENT document = FPDF_LoadDocument(argv[1], nullptr);
    if (document == nullptr) {
        FPDF_DestroyLibrary();
        return 2;
    }
    const int pages = FPDF_GetPageCount(document);
    FPDF_PAGE first_page = pages > 0 ? FPDF_LoadPage(document, 0) : nullptr;
    if (first_page == nullptr) {
        FPDF_CloseDocument(document);
        FPDF_DestroyLibrary();
        return 3;
    }
    FPDF_ClosePage(first_page);
    FPDF_CloseDocument(document);
    FPDF_DestroyLibrary();
    std::cout << "{\"pages\":" << pages << "}\n";
}
