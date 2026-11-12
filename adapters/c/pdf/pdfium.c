#include <fpdfview.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    FPDF_InitLibrary();
    FPDF_DOCUMENT document = FPDF_LoadDocument(argv[1], NULL);
    if (document == NULL) {
        FPDF_DestroyLibrary();
        return 2;
    }
    int pages = FPDF_GetPageCount(document);
    FPDF_PAGE first_page = pages > 0 ? FPDF_LoadPage(document, 0) : NULL;
    if (first_page == NULL) {
        FPDF_CloseDocument(document);
        FPDF_DestroyLibrary();
        return 3;
    }
    FPDF_ClosePage(first_page);
    FPDF_CloseDocument(document);
    FPDF_DestroyLibrary();
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
