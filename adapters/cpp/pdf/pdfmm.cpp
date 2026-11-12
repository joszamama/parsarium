#include <pdfmm/base/PdfMemDocument.h>
#include <iostream>
int main(int argc, char** argv) {
    if (argc != 2) return 1;
    mm::PdfMemDocument doc;
    doc.Load(argv[1]);
    unsigned pages = doc.GetPages().GetCount();
    if (pages == 0) return 2;
    std::cout << "{\"pages\":" << pages << "}\n";
}
