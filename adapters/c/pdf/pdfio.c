#include <pdfio.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    pdfio_file_t *pdf = pdfioFileOpen(argv[1], NULL, NULL, NULL, NULL);
    if (pdf == NULL) return 2;
    size_t pages = pdfioFileGetNumPages(pdf);
    if (pages == 0 || pdfioFileGetPage(pdf, 0) == NULL) {
        pdfioFileClose(pdf);
        return 3;
    }
    pdfioFileClose(pdf);
    printf("{\"pages\":%zu}\n", pages);
    return 0;
}
