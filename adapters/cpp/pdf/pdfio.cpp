#include <pdfio.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    pdfio_file_t* pdf = pdfioFileOpen(argv[1], nullptr, nullptr, nullptr, nullptr);
    if (pdf == nullptr) return 2;
    const size_t pages = pdfioFileGetNumPages(pdf);
    if (pages == 0 || pdfioFileGetPage(pdf, 0) == nullptr) {
        pdfioFileClose(pdf);
        return 3;
    }
    pdfioFileClose(pdf);
    std::cout << "{\"pages\":" << pages << "}\n";
}
